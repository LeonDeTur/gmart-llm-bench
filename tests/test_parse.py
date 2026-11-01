import pytest

from llmbench.parse import schema_errors, to_output


@pytest.mark.parametrize(
    "content",
    [
        '```json\n{"a":1}\n```',
        '<think>reasoning\nmore</think>\n{"a":1}',
        'Here is the answer: {"a":1} done',
        '<think>x</think>```json\n{"a":1}\n```',
    ],
)
def test_auto(content):
    assert to_output("auto", content) == ({"a": 1}, None)


def test_invalid_and_manual():
    output, error = to_output("auto", "bad {")
    assert output is None and error.startswith("invalid JSON:")
    assert to_output("manual", "  Привет\n ") == ({"text": "Привет"}, None)
    assert to_output("auto", "[1,2]") == ([1, 2], None)


def test_schema_validation():
    schema = {
        "type": "object",
        "required": ["a"],
        "properties": {"a": {"type": "integer"}},
    }
    assert not schema_errors({"a": 1}, schema)
    assert schema_errors({"a": "x"}, schema)
    assert not schema_errors({}, {"type": "invalid"})
    assert not schema_errors({}, "json")
    assert len(schema_errors({}, {"required": list("abcdefg")})) == 5
