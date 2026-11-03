import json
from datetime import datetime

import pytest

from llmbench.report import quality_score, render_report, summarize, write_reports


def record(**changes):
    return dict(
        profile="p", stage="s", case="x", kind="auto", model="m",
        status="pass", repeat=1, score=1, checks=[], output={"ok": True},
        latency_s=2, output_tokens=10,
    ) | changes


def check(name, passed, weight=1):
    return dict(name=name, passed=passed, weight=weight, expected=True, actual=passed)


def test_quality_excludes_schema_and_schema_only_records():
    wrong = record(status="fail", score=0.5, checks=[
        check("semantic", False), check("$ schema", True),
    ], quality_score=1)
    schema_only = record(case="schema", checks=[check("$ schema", True)])
    assert quality_score(wrong) == 0
    assert quality_score(schema_only) is None
    summary = summarize([wrong, schema_only])
    cell = summary["cells"][0]
    assert cell["mean_score"] == 0.75
    assert summarize([wrong])["cells"][0]["mean_score"] == 0.5
    assert cell["mean_quality_score"] == 0
    assert cell["pass_rate"] == 0.5
    profile = summary["profiles"]["p"]
    assert profile["mean_quality_score"] == 0
    assert profile["stage_macro_quality_score"] == 0
    assert quality_score(record(checks=[check("a", True, 3), check("b", False)])) == 0.75


def test_quality_macro_weights_stages_equally():
    records = [record(case=str(i), checks=[check("a", True)]) for i in range(3)]
    records.append(record(stage="other", status="fail", checks=[check("a", False)]))
    records.append(record(stage="schema", checks=[check("$ schema", True)]))
    profile = summarize(records)["profiles"]["p"]
    assert profile["mean_quality_score"] == 0.75
    assert profile["stage_macro_quality_score"] == 0.5


def test_repeats_and_profile_metrics():
    records = []
    for rep in range(1, 4):
        records.append(record(case="stable", repeat=rep, output=
                              {"a": 1, "b": 2} if rep == 1 else {"b": 2, "a": 1}))
        records.append(record(case="flaky", repeat=rep,
                              status="fail" if rep == 2 else "pass", output={"rep": rep}))
    summary = summarize(records)
    for data in (summary["cells"][0], summary["profiles"]["p"]):
        assert data["pass_all_rate"] == 0.5
        assert data["pass_any_rate"] == 1
        assert data["answer_agreement"] == 0.5
        assert data["stability"] == 0.5
    assert summary["cells"][0]["flaky_cases"] == ["flaky"]
    assert summary["profiles"]["p"]["flaky_cases"] == ["s/flaky"]
    text = render_report(summary, records, {})
    assert "Совпадение статусов" in text
    assert "`flaky`" in text


def test_single_repeat_is_unknown():
    summary = summarize([record()])
    for data in (summary["cells"][0], summary["profiles"]["p"]):
        for key in ("stability", "pass_all_rate", "pass_any_rate",
                    "flaky_cases", "answer_agreement"):
            assert data[key] is None


def test_missing_answers_are_unknown_but_null_outputs_compare_canonically():
    records = [record(repeat=i, output=None) for i in (1, 2)]
    assert summarize(records)["cells"][0]["answer_agreement"] == 1
    del records[0]["output"]
    assert summarize(records)["cells"][0]["answer_agreement"] is None


def test_manual_agreement_normalizes_content_and_excludes_profile_metrics():
    records = [record(kind="manual", repeat=i, content=text, output={"i": i})
               for i, text in enumerate([" ЁЖ  идёт\n", "еж идет", "ЕЖ ИДЕТ"], 1)]
    summary = summarize(records)
    assert summary["cells"][0]["answer_agreement"] == 1
    assert summary["profiles"]["p"]["answer_agreement"] is None


def test_profile_repeats_weight_cases_and_keep_stages_distinct():
    records = [record(repeat=i) for i in range(1, 4)]
    records += [record(stage="other", case=case, repeat=i, status="fail", output=i)
                for case in ("x", "y") for i in range(1, 4)]
    profile = summarize(records)["profiles"]["p"]
    assert profile["pass_all_rate"] == pytest.approx(1 / 3)
    assert profile["answer_agreement"] == pytest.approx(1 / 3)
    assert profile["stability"] == 1
    assert profile["flaky_cases"] == []


@pytest.mark.parametrize("meta, expected", [({}, None), ({"wall_s": 30}, 4)])
def test_wall_time(meta, expected):
    records = [record(), record(case="manual", kind="manual", output_tokens=50)]
    profile = summarize(records, meta=meta)["profiles"]["p"]
    assert profile["wall_s"] == meta.get("wall_s")
    assert profile["sum_latency_s"] == profile["total_latency_s"] == 4
    assert profile["cases_per_min"] == expected
    assert profile["output_tokens_per_s"] == (2 if expected else None)


def test_wall_time_is_shared_between_profiles():
    summary = summarize([record(), record(profile="other", output_tokens=20)],
                        meta={"wall_s": 60})
    for profile in summary["profiles"].values():
        assert profile["wall_s"] == 60
        assert profile["cases_per_min"] == 1
    assert summary["profiles"]["other"]["output_tokens_per_s"] == pytest.approx(1 / 3)


def test_best_stage_uses_pass_rate_then_quality_then_latency():
    records = [record(profile="schema", score=0.9, latency_s=1,
                      checks=[check("meaning", False), check("$ schema", True)]),
               record(profile="quality", score=0.5, latency_s=3,
                      checks=[check("meaning", True)]),
               record(profile="fast", score=0.5, latency_s=2,
                      checks=[check("meaning", True)])]
    # Equal pass rates isolate the quality and latency tie breakers.
    assert summarize(records)["best_per_stage"]["s"]["profile"] == "fast"
    records[-1]["status"] = "fail"
    assert summarize(records)["best_per_stage"]["s"]["profile"] == "quality"


def test_schema_invalid_can_be_derived_from_old_checks():
    summary = summarize([record(status="fail", checks=[check("$ schema", False)])])
    for data in (summary["cells"][0], summary["profiles"]["p"]):
        assert data["schema_invalid"] == 1
        assert data["schema_invalid_rate"] == 1


def test_write_reports_old_records(tmp_path):
    old = record(status="fail", score=0.5, checks=[
        check("semantic", False), check("$ schema", True),
    ])
    meta = {"started": "2026-01-01T00:00:00+03:00"}
    (tmp_path / "results.jsonl").write_text(json.dumps(old) + "\n", encoding="utf-8")
    summary = write_reports(tmp_path, meta)
    saved = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert saved["cells"][0]["mean_quality_score"] == 0
    assert summary["profiles"]["p"]["wall_s"] is None
    text = (tmp_path / "report.md").read_text(encoding="utf-8")
    assert "Сумма задержек" in text
    assert "| p | 2.0 | — | — | — |" in text


def test_cli_records_wall_time_after_run(tmp_path, monkeypatch):
    from types import SimpleNamespace

    from llmbench import __main__ as cli
    from llmbench.config import BenchConfig, EndpointConfig, ModelConfig, ProfileConfig

    cfg = BenchConfig(
        endpoints={"e": EndpointConfig("e")},
        models={"m": ModelConfig("m", "e", "model")},
        profiles={"p": ProfileConfig("p", "m")},
    )
    case = SimpleNamespace(status="ok", stage="s")
    monkeypatch.setattr(cli, "load_config", lambda path: cfg)
    monkeypatch.setattr(cli, "load_dataset", lambda root: SimpleNamespace(
        cases=[case], orphans=[], manifest={}))
    monkeypatch.setattr(cli, "select", lambda *args: [case])
    monkeypatch.setattr(cli, "_bench_version", lambda: {})
    monkeypatch.setattr(cli, "_server_versions", lambda endpoints: {})
    ticks = iter([100, 130])
    monkeypatch.setattr(cli.time, "perf_counter", lambda: next(ticks))

    async def run(self, cases, profiles, out_file):
        initial = json.loads((tmp_path / "meta.json").read_text(encoding="utf-8"))
        assert "finished" not in initial and "wall_s" not in initial
        out_file.write_text(json.dumps(record()) + "\n", encoding="utf-8")

    monkeypatch.setattr(cli.Runner, "run", run)
    args = cli._parser().parse_args([
        "run", "--config", str(tmp_path / "config.yaml"), "--out", str(tmp_path),
    ])
    assert cli._run(args) == 0
    meta = json.loads((tmp_path / "meta.json").read_text(encoding="utf-8"))
    assert meta["wall_s"] == 30
    assert datetime.fromisoformat(meta["finished"]) >= datetime.fromisoformat(meta["started"])
    summary = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert summary["profiles"]["p"]["cases_per_min"] == 2
