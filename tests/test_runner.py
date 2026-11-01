import asyncio
import json

import httpx

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
    responses = {"pass": '{"ok":true}', "fail": '{"ok":false}', "invalid": "bad"}

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
    assert by_case["pass"]["schema_errors"]
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
    assert summary["profiles"]["p"]["schema_invalid"] == 2
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
    monkeypatch.setattr(cli, "load_config", lambda path: config())

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
