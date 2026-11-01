"""Convert model content into checkable documents."""

import json
import re
from typing import Any

from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError


def to_output(kind: str, content: str) -> tuple[Any, str | None]:
    if kind == "manual":
        return {"text": content.strip()}, None
    text = re.sub(
        r"^\s*<think>.*?</think>\s*", "", content, count=1, flags=re.S
    ).strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.I)
    text = re.sub(r"\s*```$", "", text).strip()
    try:
        return json.loads(text), None
    except json.JSONDecodeError as exc:
        error = exc
    start, end = text.find("{"), text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start : end + 1]), None
        except json.JSONDecodeError as exc:
            error = exc
    return None, f"invalid JSON: {error.msg}"


def schema_errors(output: Any, schema: Any) -> list[str]:
    if not isinstance(schema, dict):
        return []
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError:
        return []
    errors = []
    for error in Draft202012Validator(schema).iter_errors(output):
        path = ".".join(map(str, error.absolute_path)) or "."
        errors.append(f"{path}: {error.message}")
        if len(errors) == 5:
            break
    return errors
