import hashlib
import json

import pytest
import yaml

from llmbench.dataset import _merge, input_sha, load_dataset, select


def make_dataset(tmp_path, rows=None):
    (tmp_path / "cases").mkdir()
    (tmp_path / "data").mkdir()
    cases = rows or [
        {"id": name, "input": {"nested": {"b": 2}}, "tags": ["smoke"]}
        for name in ("ok", "stale", "missing", "code")
    ]
    raw = {
        "stage": "stage.one",
        "defaults": {"nested": {"a": 1}, "list": [1]},
        "cases": cases,
    }
    (tmp_path / "cases/test.yaml").write_text(
        yaml.safe_dump(raw, allow_unicode=True), encoding="utf-8"
    )
    frozen = [
        {
            "stage": "stage.one",
            "case": name,
            "input_sha": (
                input_sha("stage.one", {"nested": {"a": 1, "b": 2}, "list": [1]})
                if name == "ok"
                else "stale"
            ),
            "request": {"messages": []},
        }
        for name in ("ok", "stale", "orphan")
    ]
    (tmp_path / "data/requests.jsonl").write_text(
        "\n".join(json.dumps(r) for r in frozen), encoding="utf-8"
    )
    (tmp_path / "data/manifest.json").write_text(
        json.dumps(
            {
                "decided_by_code": ["stage.one/code"],
                "stages": {"stage.one": {"kind": "manual"}},
            }
        ),
        encoding="utf-8",
    )
    return tmp_path


def test_join_and_select(tmp_path):
    dataset = load_dataset(make_dataset(tmp_path))
    assert {c.id: c.status for c in dataset.cases} == {
        "ok": "ok",
        "stale": "stale",
        "missing": "missing",
        "code": "code",
    }
    assert dataset.orphans == ["stage.one/orphan"]
    case = dataset.cases[0]
    assert case.kind == "manual"
    assert case.input == {"nested": {"a": 1, "b": 2}, "list": [1]}
    assert len(select(dataset.cases, ["stage.*"], ["stage.one/ok"], ["smoke"])) == 1
    assert not select(dataset.cases, tags=["unknown"])


def test_merge_sha():
    base = {"x": {"a": 1}, "items": [1]}
    assert _merge(base, {"x": {"b": 2}, "items": []}) == {
        "x": {"a": 1, "b": 2},
        "items": [],
    }
    assert base == {"x": {"a": 1}, "items": [1]}
    expected = hashlib.sha256(
        json.dumps(
            {"stage": "этап", "input": {"я": 1}},
            ensure_ascii=False,
            sort_keys=True,
            default=str,
        ).encode()
    ).hexdigest()[:16]
    assert input_sha("этап", {"я": 1}) == expected
    assert input_sha("s", {"a": 1, "b": 2}) == input_sha("s", {"b": 2, "a": 1})


def test_duplicate_and_invalid_checks(tmp_path):
    root = make_dataset(tmp_path, [{"id": "x"}, {"id": "x"}])
    with pytest.raises(ValueError, match="повтор ключа"):
        load_dataset(root)
    (root / "cases/test.yaml").write_text(
        yaml.safe_dump({"stage": "s", "cases": [{"id": "x", "expect": [{"bad": 1}]}]}),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match=r"test.yaml:x:"):
        load_dataset(root)


def test_stage_override(tmp_path):
    root = make_dataset(
        tmp_path, [{"id": "x", "stage": "other", "input": {"list": [2]}}]
    )
    case = load_dataset(root).cases[0]
    assert case.key == "other/x" and case.kind == "auto"
    assert case.input["list"] == [2]
