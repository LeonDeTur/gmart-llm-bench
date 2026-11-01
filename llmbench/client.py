"""Non-streaming adapters for frozen OpenAI and Ollama requests."""

import copy
import json
import time
from dataclasses import dataclass

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


async def complete(
    endpoint: EndpointConfig, model: ModelConfig, request: dict, http: httpx.AsyncClient
) -> Completion:
    started = time.perf_counter()
    options = {**(request.get("options") or {}), **model.options}
    messages = copy.deepcopy(request["messages"])
    kwargs = copy.deepcopy(request.get("kwargs") or {})
    think, fmt = request.get("think"), request.get("format")

    async def post(url, body, headers=None):
        response = await http.post(url, json=body, headers=headers)
        if response.status_code >= 400:
            raise LlmError(f"HTTP {response.status_code}: {response.text[:500]}")
        return response.json()

    retried = False
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
                data = await post(url, body, headers)
                retried = True
        choice = data["choices"][0]
        message = choice["message"]
        usage = data.get("usage") or {}
        return Completion(
            message.get("content") or "",
            message.get("reasoning_content") or message.get("reasoning") or "",
            choice.get("finish_reason"),
            usage.get("prompt_tokens"),
            usage.get("completion_tokens"),
            retried,
            time.perf_counter() - started,
        )
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
    data = await post(
        (endpoint.host or "http://localhost:11434").rstrip("/") + f"/api/{api}", body
    )
    message = data if api == "generate" else data.get("message", {})
    return Completion(
        message.get("response" if api == "generate" else "content") or "",
        message.get("thinking") or "",
        data.get("done_reason"),
        data.get("prompt_eval_count"),
        data.get("eval_count"),
        False,
        time.perf_counter() - started,
    )
