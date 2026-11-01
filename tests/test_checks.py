import pytest

from llmbench.checks import _MISSING, evaluate_check, resolve, score, validate_checks


def test_selectors():
    output = {
        "items": [{"id": 1, "confidence": 0.8}, {"id": 1, "confidence": 0.2}],
        "documents": [{"name": "  сп 42.13330 ", "year": 2024}],
        "selections": [{"topic": "Школа", "entities": [1, 2]}],
    }
    assert resolve(output, "items[id=1.0].confidence") == 0.8
    assert resolve(output, "documents[name=СП 42.13330].year") == 2024
    assert resolve(output, "selections[topic=школа].entities[*]") == [1, 2]
    assert resolve(output, "items[*].confidence") == [0.8, 0.2]
    assert resolve(output, "items[0].confidence") == 0.8
    assert resolve(output, "items.-1.confidence") == 0.2
    assert (
        resolve({"groups": [output, output]}, "groups[*].items[id=1][confidence=0.8]")
        == []
    )
    assert resolve(
        {"groups": [output, output]}, "groups[*].items[id=1].confidence"
    ) == [0.8, 0.8]
    assert not evaluate_check(
        output, {"path": "items[id=99].confidence", "eq": 1}
    ).passed
    assert resolve({"a": [{"k": "v"}]}, "a[k=v][*]") is _MISSING


def test_selector_boolean_is_not_numeric():
    assert not evaluate_check(
        {"a": [{"k": True}]}, {"path": "a[k=1]", "eq": {"k": True}}
    ).passed
    assert resolve({"a": [{"k": True}]}, "a[k=true].k") is True


@pytest.mark.parametrize(
    "check",
    [
        {"path": "name", "eq": "елка"},
        {"path": "name", "contains": ["ёл"]},
        {"path": "values[*]", "set_eq": [2, 1]},
        {"path": "values", "len": 2},
        {"path": "number", "approx": 1.01, "tol": 0.02},
        {"path": "number", "gte": 1},
        {"path": "absent", "null": True},
        {"path": "name", "regex": "Ёл"},
    ],
)
def test_existing_operators(check):
    result = evaluate_check({"name": "Ёлка", "values": [1, 2], "number": 1}, check)
    assert result.passed
    assert score([result]) == 1
    assert result.to_dict()["passed"] is True


def test_invalid_check():
    with pytest.raises(ValueError):
        validate_checks([{"path": "a", "eq": 1, "ne": 2}])
