"""Load and join editable cases with frozen requests."""

from __future__ import annotations

import copy
import fnmatch
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from llmbench.checks import validate_checks


def _merge(base: Any, override: Any) -> Any:
    if isinstance(base, dict) and isinstance(override, dict):
        result = copy.deepcopy(base)
        for key, value in override.items():
            result[key] = _merge(result.get(key), value)
        return result
    return copy.deepcopy(override)


def input_sha(stage: str, case_input: Any) -> str:
    payload = json.dumps(
        {"stage": stage, "input": case_input},
        ensure_ascii=False,
        sort_keys=True,
        default=str,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


@dataclass
class BenchCase:
    stage: str
    id: str
    key: str
    tags: list[str]
    input: Any
    expect: list[dict]
    review: str | None = None
    kind: str = "auto"
    request: dict | None = None
    status: str = "missing"


@dataclass
class Dataset:
    cases: list[BenchCase]
    manifest: dict
    orphans: list[str]


def load_dataset(root: str | Path) -> Dataset:
    root = Path(root)
    manifest = json.loads((root / "data/manifest.json").read_text(encoding="utf-8"))
    requests = {}
    for line in (root / "data/requests.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        key = f"{row['stage']}/{row['case']}"
        if key in requests:
            raise ValueError(f"Повтор запроса: {key}")
        requests[key] = row
    cases = []
    seen = set()
    files = sorted(
        set((root / "cases").rglob("*.yaml")) | set((root / "cases").rglob("*.yml"))
    )
    for file in files:
        raw = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
        for row in raw.get("cases", []):
            case_id = str(row["id"])
            stage = row.get("stage", raw.get("stage"))
            if not stage:
                raise ValueError(f"{file}:{case_id}: не задан этап")
            key = f"{stage}/{case_id}"
            if key in seen:
                raise ValueError(f"{file}:{case_id}: повтор ключа {key}")
            seen.add(key)
            checks = row.get("expect") or []
            try:
                validate_checks(checks)
            except (ValueError, TypeError) as exc:
                raise ValueError(f"{file}:{case_id}: {exc}") from exc
            merged = _merge(raw.get("defaults", {}), row.get("input", {}))
            frozen = requests.get(key)
            status = (
                "missing"
                if frozen is None
                else (
                    "ok"
                    if frozen.get("input_sha") == input_sha(stage, merged)
                    else "stale"
                )
            )
            if key in manifest.get("decided_by_code", []):
                status = "code"
            cases.append(
                BenchCase(
                    stage=stage,
                    id=case_id,
                    key=key,
                    tags=list(row.get("tags") or []),
                    input=merged,
                    expect=checks,
                    review=row.get("review"),
                    kind=manifest.get("stages", {}).get(stage, {}).get("kind", "auto"),
                    request=frozen["request"] if frozen else None,
                    status=status,
                )
            )
    return Dataset(cases, manifest, sorted(set(requests) - seen))


def select(
    cases: list[BenchCase],
    stages: list[str] | None = None,
    ids: list[str] | None = None,
    tags: list[str] | None = None,
    exclude_tags: list[str] | None = None,
) -> list[BenchCase]:
    return [
        case
        for case in cases
        if (not stages or any(fnmatch.fnmatchcase(case.stage, p) for p in stages))
        and (
            not ids
            or any(
                fnmatch.fnmatchcase(case.id, p) or fnmatch.fnmatchcase(case.key, p)
                for p in ids
            )
        )
        and (not tags or set(tags).intersection(case.tags))
        and not set(exclude_tags or ()).intersection(case.tags)
    ]
