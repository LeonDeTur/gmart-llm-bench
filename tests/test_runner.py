import asyncio
import json

import httpx
import pytest

from llmbench.config import (
    BenchConfig,
    EndpointConfig,
    ModelConfig,
    ProfileConfig,
    load_config,
)
from llmbench.dataset import BenchCase
from llmbench.report import render_report, summarize, write_reports
from llmbench.runner import Runner


def make_case(name, content=None, status="ok", kind="auto"):
    return BenchCase(
        stage="s",
        id=name,
        key=f"s/{name}",
        tags=["smoke"],
        input={},
        expect=[{"path": "ok", "eq": True}],
        kind=kind,
        status=status,
        request={
            "messages": [{"role": "user", "content": content or name}],
            "options": {},
            "format": {"type": "object", "required": ["extra"]},
        },
    )


def config(repeat=1, concurrency=2):
    return BenchConfig(
        endpoints={"e": EndpointConfig("e", base_url="http://test/v1")},
        models={"m": ModelConfig("m", "e", "model")},
        profiles={"p": ProfileConfig("p", "m")},
        repeat=repeat,
        concurrency=concurrency,
    )


def install_transport(monkeypatch, handler):
    original = httpx.AsyncClient
    monkeypatch.setattr(
        "llmbench.runner.httpx.AsyncClient",
        lambda **kwargs: original(transport=httpx.MockTransport(handler), **kwargs),
    )


async def test_records_and_reports(tmp_path, monkeypatch):
    responses = {
        "pass": '{"ok":true,"extra":1}',
        "fail": '{"ok":false}',
        "invalid": "bad",
    }

    def handler(req):
        body = json.loads(req.content)
        content = responses[body["messages"][0]["content"]]
        return httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": content}, "finish_reason": "stop"}]
            },
        )

    install_transport(monkeypatch, handler)
    cfg = config()
    cases = [make_case(name) for name in responses] + [
        make_case("missing", status="missing")
    ]
    records = await Runner(cfg, save_prompts=True).run(
        cases, list(cfg.profiles.values()), tmp_path / "results.jsonl"
    )
    by_case = {r["case"]: r for r in records}
    assert {k: r["status"] for k, r in by_case.items()} == {
        "pass": "pass",
        "fail": "fail",
        "invalid": "error",
    }
    assert by_case["pass"]["score"] == 1 and by_case["fail"]["score"] == 0
    assert by_case["invalid"]["checks"] == [] and by_case["invalid"]["score"] == 0
    assert not by_case["pass"]["schema_errors"]
    fields = {
        "profile",
        "stage",
        "case",
        "tags",
        "repeat",
        "model",
        "model_id",
        "endpoint",
        "kind",
        "input",
        "review",
        "status",
        "needs_review",
        "score",
        "checks",
        "output",
        "error",
        "latency_s",
        "llm_calls",
        "input_tokens",
        "output_tokens",
        "retried",
        "done_reason",
        "schema_errors",
        "content",
        "thinking",
        "request",
        "attempts",
        "request_params",
    }
    assert all(fields <= r.keys() for r in records)
    assert all(r["llm_calls"] == 1 for r in records)
    lines = [
        json.loads(line)
        for line in (tmp_path / "results.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
    ]
    assert len(lines) == 3
    meta = {"dataset": {"commit": "1234567890", "exported_at": "today"}}
    summary = write_reports(tmp_path, meta)
    assert summary["profiles"]["p"]["schema_invalid"] == 1
    report = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert (
        "12345678" in report and "Невалидных по схеме" in report and "Повторы" in report
    )
    assert "схема:" in report
    assert (tmp_path / "summary.json").exists()
    # Only manual stages need a human look: an all-auto run has nothing to grade.
    assert not (tmp_path / "review.md").exists()
    assert not (tmp_path / "grades.csv").exists()


async def test_timeout_and_skipped(tmp_path, monkeypatch):
    async def handler(req):
        await asyncio.sleep(0.05)
        return httpx.Response(500)

    install_transport(monkeypatch, handler)
    cfg = config()
    profiles = [ProfileConfig("p", "m"), ProfileConfig("skip", None)]
    records = await Runner(cfg, case_timeout_s=0.001).run(
        [make_case("x")], profiles, tmp_path / "out.jsonl"
    )
    assert [r["status"] for r in records] == ["error", "skipped"]
    assert "время" in records[0]["error"]
    assert "request" not in records[0]
    assert summarize(records)["cells"][0]["runs"] == 1


async def test_profiles_sequential_bounded_concurrency(tmp_path, monkeypatch):
    active = peak = 0
    order = []

    async def handler(req):
        nonlocal active, peak
        body = json.loads(req.content)
        order.append(body["model"])
        active += 1
        peak = max(peak, active)
        await asyncio.sleep(0.001)
        active -= 1
        return httpx.Response(
            200, json={"choices": [{"message": {"content": '{"ok":true}'}}]}
        )

    install_transport(monkeypatch, handler)
    cfg = config(repeat=2, concurrency=2)
    cfg.models["m2"] = ModelConfig("m2", "e", "model2")
    records = await Runner(cfg).run(
        [make_case("a"), make_case("b")],
        [ProfileConfig("p", "m"), ProfileConfig("p2", "m2")],
        tmp_path / "out.jsonl",
    )
    assert len(records) == 8 and peak == 2
    assert order == ["model"] * 4 + ["model2"] * 4


def test_config_environment_and_profiles(tmp_path, monkeypatch):
    monkeypatch.setenv("BENCH_TEST_URL", "http://example/v1")
    monkeypatch.delenv("UNSET_BENCH_KEY", raising=False)
    file = tmp_path / "config.yaml"
    file.write_text(
        """endpoints:
  e:
    base_url: ${BENCH_TEST_URL:-http://fallback}
    api_key: ${UNSET_BENCH_KEY:-fallback-key}
models:
  m: {endpoint: e, model: model}
profiles:
  p:
    default: m
    stages: {"skip.*": null}
""",
        encoding="utf-8",
    )
    cfg = load_config(file)
    assert cfg.endpoints["e"].base_url == "http://example/v1"
    assert cfg.endpoints["e"].api_key == "fallback-key"
    assert cfg.profiles["p"].model_for("skip.x") is None
    assert cfg.add_single_model_profiles(["m"]) == ["only:m"]
    assert cfg.select_profiles(["only:m"])[0].default == "m"


def test_report_retry_count():
    record = dict(
        profile="p",
        stage="s",
        case="x",
        repeat=1,
        kind="auto",
        model="m",
        status="fail",
        retried=True,
        schema_errors=["bad schema"],
        checks=[],
    )
    summary = summarize([record])
    assert summary["cells"][0]["retried"] == 1
    assert "bad schema" in render_report(summary, [record], {})


def test_cli_list_and_nothing_to_run(tmp_path, monkeypatch, capsys):
    from llmbench import __main__ as cli
    from llmbench.dataset import Dataset

    dataset = Dataset(
        [make_case("ok"), make_case("stale", status="stale")], {}, ["s/orphan"]
    )
    monkeypatch.setattr(cli, "load_dataset", lambda root: dataset)
    assert cli.main(["list", "--root", str(tmp_path)]) == 1
    text = capsys.readouterr().out
    assert "ok=1" in text and "stale=1" in text and "s/orphan" in text
    monkeypatch.setattr(cli, "load_config", lambda path: config())
    assert cli.main(["run", "--config", "unused.yaml", "--cases", "unknown"]) == 2


def test_cli_exact_out_and_meta(tmp_path, monkeypatch):
    from llmbench import __main__ as cli
    from llmbench.dataset import Dataset

    dataset = Dataset(
        [make_case("ok")],
        {"gmart": {"commit": "123", "dirty": False}, "exported_at": "today"},
        [],
    )
    monkeypatch.setattr(cli, "load_dataset", lambda root: dataset)
    cfg = config()
    cfg.endpoints["e"] = EndpointConfig(
        "e", base_url="http://u:p@test/v1", api_key="secret",
        host="http://u:p@host:8002/v1?k=1#fragment",
        extra_body={"custom": "unchanged"},
    )
    cfg.endpoints["unused"] = EndpointConfig("unused", api_key="unused-secret")
    monkeypatch.setattr(cli, "load_config", lambda path: cfg)

    def unavailable(url, **kwargs):
        assert url == "http://u:p@test/version"
        assert kwargs["timeout"] == 2
        raise httpx.ConnectError("offline")

    monkeypatch.setattr(cli.httpx, "get", unavailable)

    async def fake_run(self, cases, profiles, out_file):
        out_file.write_text("", encoding="utf-8")
        return []

    monkeypatch.setattr(cli.Runner, "run", fake_run)
    out = tmp_path / "exact"
    arguments = ["run", "--config", "unused.yaml", "--out", str(out), "--models", "m"]
    assert cli.main(arguments) == 0
    meta = json.loads((out / "meta.json").read_text(encoding="utf-8"))
    assert meta["dataset"] == {"commit": "123", "dirty": False, "exported_at": "today"}
    assert meta["profiles"] == ["only:m"]
    assert meta["profile_models"] == {"only:m": {"s": "m"}}
    assert meta["servers"] == {"e": None}
    assert "api_key" not in meta["endpoints"]["e"]
    assert set(meta["endpoints"]) == {"e"}
    assert "secret" not in json.dumps(meta)
    assert meta["endpoints"]["e"]["base_url"] == "http://test/v1"
    assert meta["endpoints"]["e"]["host"] == "http://host:8002/v1"
    assert meta["endpoints"]["e"]["extra_body"] == {"custom": "unchanged"}
    assert meta["run"]["argv"] == arguments
    assert meta["run"]["concurrency"] == 2
    assert meta["run"]["case_timeout"] == 900
    assert set(meta["bench"]) == {"commit", "dirty"}
    assert (out / "results.jsonl").is_file()
    assert cli.main(arguments) == 1


def test_grades_are_folded_and_preserved(tmp_path):
    record = dict(
        profile="p",
        stage="s",
        case="x",
        repeat=1,
        kind="manual",
        model="m",
        status="pass",
        needs_review=True,
        output={"text": "Ответ"},
        checks=[],
    )
    (tmp_path / "results.jsonl").write_text(
        json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    write_reports(tmp_path, {})
    grades = "profile,stage,case,repeat,model,grade,comment\np,s,x,1,m,2,Проверено\n"
    (tmp_path / "grades.csv").write_text(grades, encoding="utf-8-sig")
    summary = write_reports(tmp_path, {})
    assert summary["cells"][0]["mean_grade"] == 2
    assert (tmp_path / "grades.csv").read_text(encoding="utf-8-sig") == grades


@pytest.mark.parametrize(
    "kind,content,status,expected_score",
    [
        ("auto", '{"ok":true}', "fail", 0.5),
        ("auto", '{"ok":true,"extra":1}', "pass", 1),
        ("manual", "Ответ", "pass", 1),
    ],
)
async def test_schema_scoring(tmp_path, monkeypatch, kind, content, status, expected_score):
    install_transport(monkeypatch, lambda req: httpx.Response(
        200, json={"choices": [{"message": {"content": content}, "finish_reason": "stop"}]}
    ))
    cfg = config()
    case = make_case("schema", kind=kind)
    if kind == "manual":
        case.expect = [{"path": "text", "eq": "Ответ"}]
    records = await Runner(cfg).run([case], list(cfg.profiles.values()), tmp_path / "out.jsonl")
    record = records[0]
    assert record["status"] == status
    assert record["score"] == expected_score
    schema_checks = [c for c in record["checks"] if c["name"] == "$ schema"]
    if kind == "auto":
        assert len(schema_checks) == 1
        assert schema_checks[0]["passed"] == (status == "pass")
    else:
        assert not schema_checks and record["needs_review"]


@pytest.mark.parametrize("failure", [None, "http", "timeout"])
async def test_retry_accounting(tmp_path, monkeypatch, failure):
    calls = []

    async def handler(req):
        calls.append(json.loads(req.content))
        if len(calls) == 2:
            if failure == "http":
                return httpx.Response(500, text="offline")
            if failure == "timeout":
                await asyncio.sleep(0.2)
        first = len(calls) == 1
        return httpx.Response(200, json={
            "choices": [{"message": {"content": '{"ok":true,"extra":1}'},
                         "finish_reason": "length" if first else "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
        })

    install_transport(monkeypatch, handler)
    cfg = config()
    cfg.endpoints["e"] = EndpointConfig("e", api_key="secret")
    case = make_case("retry")
    case.request["format"]["title"] = "plan"
    records = await Runner(cfg, case_timeout_s=0.05).run(
        [case], list(cfg.profiles.values()), tmp_path / "results.jsonl"
    )
    record = records[0]
    assert record["llm_calls"] == 2 and record["retried"]
    assert len(record["attempts"]) == 2
    assert record["input_tokens"] == (10 if failure else 20)
    assert record["output_tokens"] == (5 if failure else 10)
    assert record["status"] == ("error" if failure else "pass")
    params = record["request_params"]
    assert "messages" not in params and "secret" not in json.dumps(params)
    ref = params["response_format"]["json_schema"]["schema"]
    assert set(ref) == {"sha256", "title"} and ref["title"] == "plan"
    assert len(ref["sha256"]) == 12 and params["max_tokens"] == 4096
    saved = json.loads((tmp_path / "results.jsonl").read_text(encoding="utf-8"))
    assert saved == record
    cell = summarize(records)["cells"][0]
    assert cell["mean_llm_calls"] == 2 and cell["retried"] == 1


def test_cli_old_results(tmp_path):
    from llmbench.__main__ import main

    record = dict(profile="p", stage="s", case="old", kind="auto", status="pass",
                  score=1, checks=[], llm_calls=1)
    (tmp_path / "meta.json").write_text("{}", encoding="utf-8")
    (tmp_path / "results.jsonl").write_text(json.dumps(record) + "\n", encoding="utf-8")
    assert main(["report", str(tmp_path)]) == 0
    assert (tmp_path / "report.md").exists()
    assert (tmp_path / "summary.json").exists()


def test_report_provenance():
    text = render_report(summarize([]), [], {
        "bench": {"commit": "abcdef012345", "dirty": True},
        "servers": {"vllm": {"version": "0.12"}, "ollama": {"version": "0.9"}, "offline": None},
    })
    assert "abcdef01 (есть незакоммиченные изменения)" in text
    assert "vllm: 0.12" in text and "ollama: 0.9" in text


def test_bench_git_unavailable(monkeypatch):
    from llmbench import __main__ as cli

    def unavailable(*args, **kwargs):
        raise FileNotFoundError("git")

    monkeypatch.setattr(cli.subprocess, "run", unavailable)
    assert cli._bench_version() == {"commit": None, "dirty": None}


@pytest.mark.parametrize("tracked_status", ["", " M llmbench/client.py\n"])
def test_bench_dirty_ignores_untracked(monkeypatch, tracked_status):
    from llmbench import __main__ as cli

    calls = []

    def run(command, **kwargs):
        calls.append(command)
        if command == ["git", "rev-parse", "HEAD"]:
            output = "abcdef012345\n"
        else:
            assert command == [
                "git", "status", "--porcelain", "--untracked-files=no",
                "--", "llmbench", "cases", "data",
            ]
            output = tracked_status
        return cli.subprocess.CompletedProcess(command, 0, stdout=output)

    monkeypatch.setattr(cli.subprocess, "run", run)
    assert cli._bench_version() == {
        "commit": "abcdef012345", "dirty": bool(tracked_status),
    }
    assert len(calls) == 2


@pytest.mark.parametrize("value,expected", [
    (None, None),
    ("http://u:p@host:8002/v1?k=1", "http://host:8002/v1"),
    ("https://u:p@host/v1?k=1#fragment", "https://host/v1"),
    ("http://u:p@[::1]:8002/v1#fragment", "http://[::1]:8002/v1"),
    ("http://host:8002/v1", "http://host:8002/v1"),
])
def test_clean_endpoint_url(value, expected):
    from llmbench.__main__ import _clean_url

    assert _clean_url(value) == expected


def test_server_versions(monkeypatch):
    from llmbench import __main__ as cli

    urls = []

    def get(url, **kwargs):
        urls.append(url)
        return httpx.Response(200, json={"version": "test"}, request=httpx.Request("GET", url))

    monkeypatch.setattr(cli.httpx, "get", get)
    versions = cli._server_versions({
        "v": EndpointConfig("v", base_url="http://v/v1/"),
        "o": EndpointConfig("o", backend="ollama", host="http://o/"),
    })
    assert urls == ["http://v/version", "http://o/api/version"]
    assert versions == {"v": {"version": "test"}, "o": {"version": "test"}}
