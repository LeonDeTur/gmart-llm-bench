import copy
import json

import httpx
import pytest

from llmbench.client import LlmError, complete
from llmbench.config import EndpointConfig, ModelConfig


def answer(content='{"ok":true}', reason="stop"):
    return {
        "choices": [
            {
                "message": {"content": content, "reasoning_content": "thought"},
                "finish_reason": reason,
            }
        ],
        "usage": {"prompt_tokens": 10, "completion_tokens": 5},
    }


async def call(endpoint, request, model_id="model", responses=None, model_options=None):
    calls = []
    responses = list(responses or [answer()])

    def handler(req):
        calls.append((req, json.loads(req.content)))
        return httpx.Response(200, json=responses.pop(0))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as http:
        result = await complete(
            endpoint,
            ModelConfig("m", endpoint.name, model_id, model_options or {}),
            request,
            http,
        )
    return result, calls


def request(**overrides):
    return {
        "api": "chat",
        "messages": [{"role": "user", "content": "Привет"}],
        "options": {
            "temperature": 0,
            "num_predict": 1024,
            "num_ctx": 16384,
            "top_p": 0.9,
        },
        "think": False,
        "format": None,
        "kwargs": {},
        **overrides,
    }


async def test_openai_chat_template_exact_body():
    ep = EndpointConfig(
        "e",
        base_url="http://test/",
        think_mode="chat_template",
        extra_body={"temperature": 9, "custom": True},
    )
    result, calls = await call(ep, request())
    req, body = calls[0]
    assert str(req.url) == "http://test/v1/chat/completions"
    assert req.headers["authorization"] == "Bearer not-needed"
    assert body == {
        "model": "model",
        "messages": [{"role": "user", "content": "Привет"}],
        "stream": False,
        "temperature": 0,
        "max_tokens": 1024,
        "top_p": 0.9,
        "chat_template_kwargs": {"enable_thinking": False},
        "custom": True,
    }
    assert result.content == '{"ok":true}' and result.thinking == "thought"
    assert result.input_tokens == 10 and result.output_tokens == 5


@pytest.mark.parametrize(
    "model_id,mode,kwargs,expected",
    [
        ("model", "reasoning_effort", {}, "none"),
        ("model", "reasoning_effort", {"reasoning_effort": "medium"}, "medium"),
        ("gpt-oss-20b", "reasoning_effort", {}, "low"),
        ("GPT-OSS-20B", "off", {"reasoning_effort": "minimal"}, "low"),
        ("gpt-oss-20b", "reasoning_effort", {"reasoning_effort": "high"}, "high"),
    ],
)
async def test_reasoning_effort(model_id, mode, kwargs, expected):
    _, calls = await call(
        EndpointConfig("e", think_mode=mode), request(kwargs=kwargs), model_id
    )
    assert calls[0][1]["reasoning_effort"] == expected


async def test_schema_and_model_options():
    schema = {"title": "plan", "type": "object"}
    original = request(format=schema, kwargs={"unused": None, "extra": 1})
    before = copy.deepcopy(original)
    _, calls = await call(
        EndpointConfig("e", base_url="http://test/v1"),
        original,
        model_options={"num_predict": 512, "temperature": 0.2},
    )
    assert original == before
    body = calls[0][1]
    assert body["response_format"] == {
        "type": "json_schema",
        "json_schema": {"name": "plan", "schema": schema, "strict": False},
    }
    assert body["max_tokens"] == 512 and body["temperature"] == 0.2
    assert "num_ctx" not in body and "unused" not in body and body["extra"] == 1


@pytest.mark.parametrize("content,reason", [("{}", "length"), (" ", "stop")])
async def test_structured_retry(content, reason):
    result, calls = await call(
        EndpointConfig("e"),
        request(format="json"),
        responses=[answer(content, reason), answer('{"ok":true}')],
    )
    assert len(calls) == 2 and result.retried
    assert calls[0][1]["max_tokens"] == 1024
    assert calls[1][1]["max_tokens"] == 4096
    assert result.content == '{"ok":true}'


async def test_retry_context_limit():
    result, calls = await call(
        EndpointConfig("e"),
        request(format="json", options={"num_ctx": 500, "num_predict": 1024}),
        responses=[answer("", "length")],
    )
    assert len(calls) == 1 and not result.retried


@pytest.mark.parametrize("api", ["chat", "generate"])
async def test_ollama(api):
    response = {
        "message": {"content": "{}", "thinking": "thought"},
        "response": "{}",
        "thinking": "thought",
        "done_reason": "stop",
        "prompt_eval_count": 7,
        "eval_count": 3,
    }
    result, calls = await call(
        EndpointConfig("e", backend="ollama"),
        request(
            api=api,
            format="json",
            kwargs={"reasoning_effort": "medium", "keep_alive": "5m"},
        ),
        responses=[response],
    )
    req, body = calls[0]
    assert str(req.url) == f"http://localhost:11434/api/{api}"
    expected = {
        "model": "model",
        "stream": False,
        "options": request()["options"],
        "think": False,
        "format": "json",
        "keep_alive": "5m",
    }
    expected.update(
        {"prompt": "Привет"}
        if api == "generate"
        else {"messages": request()["messages"]}
    )
    assert body == expected
    assert result.content == "{}" and result.thinking == "thought"
    assert result.input_tokens == 7 and result.output_tokens == 3 and not result.retried


async def test_http_error():
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(lambda req: httpx.Response(400, text="x" * 600))
    ) as http:
        with pytest.raises(LlmError, match="HTTP 400") as exc:
            await complete(
                EndpointConfig("e"), ModelConfig("m", "e", "model"), request(), http
            )
    assert len(str(exc.value)) == len("HTTP 400: ") + 500


async def test_openai_generate_is_chat():
    _, calls = await call(EndpointConfig("e"), request(api="generate"))
    assert calls[0][1]["messages"] == request()["messages"]
