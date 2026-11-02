"""Non-streaming adapters for frozen OpenAI and Ollama requests."""

import copy
import hashlib
import json
import time
from dataclasses import dataclass, field

import httpx

from llmbench.config import EndpointConfig, ModelConfig


class LlmError(RuntimeError):
    """An endpoint rejected a completion request."""


@dataclass
class Completion:
    content: str
    thinking: str
    done_reason: str | None
    input_tokens: int | None
    output_tokens: int | None
    retried: bool
    latency_s: float
    calls: int = 0
    attempts: list[dict] = field(default_factory=list)
    request_params: dict = field(default_factory=dict)


def request_params(body: dict) -> dict:
    params = copy.deepcopy(body)
    params.pop("messages", None)
    params.pop("prompt", None)
    params.pop("api_key", None)

    def schema_ref(schema):
        encoded = json.dumps(schema, sort_keys=True, ensure_ascii=False).encode("utf-8")
        return {
            "sha256": hashlib.sha256(encoded).hexdigest()[:12],
            "title": schema.get("title"),
        }

    if isinstance(params.get("format"), dict):
        params["format"] = schema_ref(params["format"])
    response_format = params.get("response_format") or {}
    structured = response_format.get("json_schema") or {}
    if isinstance(structured.get("schema"), dict):
        structured["schema"] = schema_ref(structured["schema"])
    return params


async def complete(
    endpoint: EndpointConfig,
    model: ModelConfig,
    request: dict,
    http: httpx.AsyncClient,
    *,
    progress: Completion | None = None,
) -> Completion:
    """Update progress before each call so failures and cancellation retain usage."""
    started = time.perf_counter()
    progress = progress or Completion("", "", None, None, None, False, 0)
    options = {**(request.get("options") or {}), **model.options}
    messages = copy.deepcopy(request["messages"])
    kwargs = copy.deepcopy(request.get("kwargs") or {})
    think, fmt = request.get("think"), request.get("format")

    async def post(url, body, headers=None):
        progress.request_params = request_params(body)
        attempt = dict(
            done_reason=None,
            input_tokens=None,
            output_tokens=None,
            max_tokens=(
                body.get("max_tokens") if endpoint.backend == "openai"
                else body["options"].get("num_predict")
            ),
        )
        progress.attempts.append(attempt)
        progress.calls += 1
        progress.retried = progress.calls > 1
        progress.done_reason = None
        response = await http.post(url, json=body, headers=headers)
        if response.status_code >= 400:
            raise LlmError(f"HTTP {response.status_code}: {response.text[:500]}")
        data = response.json()
        if endpoint.backend == "openai":
            choice = data["choices"][0]
            message = choice["message"]
            usage = data.get("usage") or {}
            reason = choice.get("finish_reason")
            incoming = usage.get("prompt_tokens")
            outgoing = usage.get("completion_tokens")
            progress.content = message.get("content") or ""
            progress.thinking = (
                message.get("reasoning_content") or message.get("reasoning") or ""
            )
        else:
            generate = request.get("api") == "generate"
            message = data if generate else data.get("message", {})
            reason = data.get("done_reason")
            incoming, outgoing = data.get("prompt_eval_count"), data.get("eval_count")
            progress.content = message.get("response" if generate else "content") or ""
            progress.thinking = message.get("thinking") or ""
        attempt.update(done_reason=reason, input_tokens=incoming, output_tokens=outgoing)
        progress.done_reason = reason
        for key, value in (("input_tokens", incoming), ("output_tokens", outgoing)):
            if value is not None:
                setattr(progress, key, (getattr(progress, key) or 0) + value)
        progress.latency_s = time.perf_counter() - started
        return data

    if endpoint.backend == "openai":
        base = (endpoint.base_url or "http://localhost:8000").rstrip("/")
        if not base.endswith("/v1"):
            base += "/v1"
        url = base + "/chat/completions"
        headers = {"Authorization": f"Bearer {endpoint.api_key or 'not-needed'}"}
        body = {"model": model.model, "messages": messages, "stream": False}
        for source, target in (
            ("temperature", "temperature"),
            ("num_predict", "max_tokens"),
            ("top_p", "top_p"),
        ):
            if source in options:
                body[target] = options[source]
        body.update({k: v for k, v in kwargs.items() if v is not None})
        if (
            think is False
            and "gpt-oss" in model.model.lower()
            and endpoint.think_mode != "chat_template"
        ):
            effort = (
                endpoint.think_effort
                if endpoint.think_effort in {"low", "medium", "high"}
                else "low"
            )
            if body.get("reasoning_effort") in (None, "none", "minimal"):
                body["reasoning_effort"] = effort
        elif think is not None:
            if endpoint.think_mode == "reasoning_effort" and think is False:
                body.setdefault("reasoning_effort", endpoint.think_effort)
            elif endpoint.think_mode == "chat_template":
                body.setdefault("chat_template_kwargs", {}).setdefault(
                    endpoint.think_chat_template_kwarg, think
                )
        if fmt == "json":
            body["response_format"] = {"type": "json_object"}
        elif isinstance(fmt, dict):
            body["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": fmt.get("title", "response"),
                    "schema": fmt,
                    "strict": False,
                },
            }
        body = {**copy.deepcopy(endpoint.extra_body), **body}
        body["stream"] = False
        data = await post(url, body, headers)
        choice = data["choices"][0]
        content = choice["message"].get("content") or ""
        if "response_format" in body and (
            choice.get("finish_reason") == "length" or not content.strip()
        ):
            budget = body.get("max_tokens") or 2048
            retry_budget = max(budget, min(8192, max(4096, budget * 2)))
            if "num_ctx" in options:
                input_cost = sum(
                    len(str(m.get("content", "")).encode()) for m in messages
                )
                input_cost += len(json.dumps(body["response_format"]).encode())
                retry_budget = min(retry_budget, options["num_ctx"] - input_cost - 256)
            if retry_budget > budget:
                body["max_tokens"] = retry_budget
                await post(url, body, headers)
        return progress
    if endpoint.backend != "ollama":
        raise LlmError(f"Неизвестный backend: {endpoint.backend}")
    api = request.get("api", "chat")
    body = {"model": model.model, "stream": False, "options": options}
    if api == "generate":
        body["prompt"] = next(m["content"] for m in messages if m.get("role") == "user")
    else:
        body["messages"] = messages
    for key, value in (("think", think), ("format", fmt)):
        if value is not None:
            body[key] = value
    if "keep_alive" in kwargs:
        body["keep_alive"] = kwargs["keep_alive"]
    await post(
        (endpoint.host or "http://localhost:11434").rstrip("/") + f"/api/{api}", body
    )
    return progress
