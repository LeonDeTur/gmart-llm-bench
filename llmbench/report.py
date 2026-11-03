"""Summaries of a run: ``summary.json``, ``report.md``, ``review.md``, ``grades.csv``.

``report.md`` answers "which configuration is best": a stage x profile matrix of pass
rate, score, latency and tokens, the best profile per stage, and every failed check.
``review.md`` puts the free-text outputs of manual stages side by side per case;
``grades.csv`` is where a reviewer scores them (0-2). Re-running ``report`` folds the
filled grades back into the summary.
"""

from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

from llmbench.checks import normalize

GRADE_FIELDS = ["profile", "stage", "case", "repeat", "model", "grade", "comment"]


def load_results(results_dir: Path) -> list[dict[str, Any]]:
    path = results_dir / "results.jsonl"
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, round(0.95 * (len(ordered) - 1)))]


def _mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def load_grades(results_dir: Path) -> dict[tuple, float]:
    path = results_dir / "grades.csv"
    if not path.exists():
        return {}
    grades = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle):
            raw = (row.get("grade") or "").strip().replace(",", ".")
            if not raw:
                continue
            key = (row["profile"], row["stage"], row["case"], str(row["repeat"]))
            grades[key] = float(raw)
    return grades


def quality_score(record: dict[str, Any]) -> float | None:
    checks = [c for c in record.get("checks") or [] if c["name"] != "$ schema"]
    if not checks:
        return None
    total = sum(c.get("weight", 1) for c in checks)
    return (
        sum(c.get("weight", 1) for c in checks if c["passed"]) / total
        if total
        else 1.0
    )


def _quality_mean(items: list[dict]) -> float | None:
    scores = [value for item in items if (value := quality_score(item)) is not None]
    return _mean(scores) if scores else None


def _schema_invalid(item: dict) -> bool:
    return bool(item.get("schema_errors")) or any(
        c["name"] == "$ schema" and not c["passed"]
        for c in item.get("checks") or []
    )


def _repeat_metrics(items: list[dict], *, qualified: bool = False) -> dict[str, Any]:
    by_case: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for item in items:
        by_case[(item["stage"], item["case"])].append(item)
    repeated = {
        key: records
        for key, records in by_case.items()
        if len({r.get("repeat", 1) for r in records}) > 1
    }
    if not repeated:
        return dict(
            stability=None, pass_all_rate=None, pass_any_rate=None,
            flaky_cases=None, answer_agreement=None,
        )
    flaky = []
    agreements = 0
    missing_answers = False
    for (stage, case), records in sorted(repeated.items()):
        if len({r["status"] for r in records}) > 1:
            flaky.append(f"{stage}/{case}" if qualified else case)
        field = "content" if records[0].get("kind") == "manual" else "output"
        missing_answers |= any(field not in r for r in records)
        answers = [
            normalize(r.get(field))
            if field == "content"
            else json.dumps(r.get(field), sort_keys=True, ensure_ascii=False)
            for r in records
        ]
        agreements += all(answer == answers[0] for answer in answers)
    count = len(repeated)
    return dict(
        stability=1 - len(flaky) / count,
        pass_all_rate=sum(
            all(r["status"] == "pass" for r in rs) for rs in repeated.values()
        ) / count,
        pass_any_rate=sum(
            any(r["status"] == "pass" for r in rs) for rs in repeated.values()
        ) / count,
        flaky_cases=flaky,
        answer_agreement=agreements / count if not missing_answers else None,
    )


def summarize(
    results: list[dict[str, Any]],
    grades: dict[tuple, float] | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    grades = grades or {}
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for result in results:
        if result.get("status") == "skipped":
            continue
        groups[(result["profile"], result["stage"])].append(result)

    cells = []
    for (profile, stage), items in sorted(groups.items()):
        latencies = [item.get("latency_s") or 0.0 for item in items]
        graded = [
            grades[key]
            for item in items
            if (
                key := (
                    item["profile"],
                    item["stage"],
                    item["case"],
                    str(item.get("repeat", 1)),
                )
            )
            in grades
        ]
        cells.append(
            {
                "profile": profile,
                "stage": stage,
                "kind": items[0].get("kind"),
                "model": items[0].get("model"),
                "runs": len(items),
                "pass": sum(item["status"] == "pass" for item in items),
                "fail": sum(item["status"] == "fail" for item in items),
                "error": sum(item["status"] == "error" for item in items),
                "schema_invalid": sum(_schema_invalid(item) for item in items),
                "retried": sum(bool(item.get("retried")) for item in items),
                "pass_rate": sum(item["status"] == "pass" for item in items)
                / len(items),
                "mean_score": _mean([item.get("score") or 0.0 for item in items]),
                "mean_quality_score": _quality_mean(items),
                "schema_invalid_rate": sum(
                    _schema_invalid(item) for item in items
                ) / len(items),
                "mean_latency_s": _mean(latencies),
                "p95_latency_s": _p95(latencies),
                "mean_input_tokens": _mean(
                    [item.get("input_tokens") or 0 for item in items]
                ),
                "mean_output_tokens": _mean(
                    [item.get("output_tokens") or 0 for item in items]
                ),
                "mean_llm_calls": _mean([item.get("llm_calls") or 0 for item in items]),
                **_repeat_metrics(items),
                "graded": len(graded),
                "mean_grade": _mean(graded) if graded else None,
            }
        )

    profiles: dict[str, dict[str, Any]] = {}
    for profile in sorted({cell["profile"] for cell in cells}):
        auto = [c for c in cells if c["profile"] == profile and c["kind"] == "auto"]
        runs = sum(c["runs"] for c in auto)
        profile_items = [
            r for r in results
            if r["profile"] == profile and r.get("status") != "skipped"
        ]
        auto_items = [r for r in profile_items if r.get("kind") == "auto"]
        quality_cells = [
            c["mean_quality_score"] for c in auto
            if c["mean_quality_score"] is not None
        ]
        wall_s = (meta or {}).get("wall_s")
        profiles[profile] = {
            "auto_runs": runs,
            "auto_pass_rate": (sum(c["pass"] for c in auto) / runs) if runs else None,
            # Every stage weighs the same, however many cases it has.
            "stage_macro_score": (
                _mean([c["mean_score"] for c in auto]) if auto else None
            ),
            "mean_score": (
                _mean([r.get("score") or 0.0 for r in auto_items])
                if auto_items else None
            ),
            "mean_quality_score": _quality_mean(auto_items),
            "stage_macro_quality_score": _mean(quality_cells) if quality_cells else None,
            **_repeat_metrics(auto_items, qualified=True),
            "wall_s": wall_s,
            "cases_per_min": len(profile_items) * 60 / wall_s if wall_s else None,
            "output_tokens_per_s": (
                sum(r.get("output_tokens") or 0 for r in profile_items) / wall_s
                if wall_s else None
            ),
            "errors": sum(c["error"] for c in cells if c["profile"] == profile),
            "schema_invalid": sum(
                c["schema_invalid"] for c in cells if c["profile"] == profile
            ),
            "total_latency_s": sum(
                c["mean_latency_s"] * c["runs"]
                for c in cells
                if c["profile"] == profile
            ),
        }
        profiles[profile]["sum_latency_s"] = profiles[profile]["total_latency_s"]
        profiles[profile]["schema_invalid_rate"] = (
            sum(c["schema_invalid_rate"] * c["runs"] for c in cells
                if c["profile"] == profile) / len(profile_items)
        )

    best: dict[str, dict[str, Any]] = {}
    for stage in sorted({cell["stage"] for cell in cells}):
        candidates = [c for c in cells if c["stage"] == stage]
        if candidates[0]["kind"] == "manual":
            graded = [c for c in candidates if c["mean_grade"] is not None]
            if not graded:
                continue
            top = max(graded, key=lambda c: (c["mean_grade"], -c["mean_latency_s"]))
        else:
            top = max(
                candidates,
                key=lambda c: (
                    c["pass_rate"],
                    c["mean_quality_score"] if c["mean_quality_score"] is not None else -1,
                    -c["mean_latency_s"],
                ),
            )
        best[stage] = {
            "profile": top["profile"],
            "model": top["model"],
            "pass_rate": top["pass_rate"],
            "mean_score": top["mean_score"],
            "mean_quality_score": top["mean_quality_score"],
            "mean_grade": top["mean_grade"],
            "mean_latency_s": top["mean_latency_s"],
        }
    return {"cells": cells, "profiles": profiles, "best_per_stage": best}


def _pct(value: float | None) -> str:
    return "—" if value is None else f"{value * 100:.1f}%"


def _number(value: float | None) -> str:
    return "—" if value is None else f"{value:.1f}"


def _short(value: Any, limit: int = 160) -> str:
    text = (
        json.dumps(value, ensure_ascii=False) if not isinstance(value, str) else value
    )
    text = text.replace("\n", " ").replace("|", "\\|")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def render_report(
    summary: dict[str, Any], results: list[dict[str, Any]], meta: dict
) -> str:
    lines = [f"# Бенчмарк LLM-этапов gMART — {meta.get('started', '')}", ""]
    bench = meta.get("bench") or {}
    provenance = []
    if bench.get("commit"):
        commit = bench["commit"][:8]
        if bench.get("dirty"):
            commit += " (есть незакоммиченные изменения)"
        provenance.append(f"Бенчмарк: {commit}")
    for name, server in (meta.get("servers") or {}).items():
        if isinstance(server, dict) and server.get("version"):
            provenance.append(f"{name}: {server['version']}")
    if provenance:
        lines += [" · ".join(provenance), ""]
    lines += [
        f"Профили: {', '.join(meta.get('profiles', []))} · кейсов: {meta.get('cases', 0)} · "
        f"повторов: {meta.get('repeat', 1)} · датасет: gMART "
        f"{meta.get('dataset', {}).get('commit', '')[:8]} от "
        f"{meta.get('dataset', {}).get('exported_at', '')}",
        "",
        "## Итог по профилям (автоматически оцениваемые этапы)",
        "",
        "Балл качества учитывает только проверки смысла, без `$ schema`; кейсы без таких "
        "проверок исключены из среднего. Pass rate по-прежнему требует успеха всех проверок.",
        "",
        "| Профиль | Прогонов | Pass rate | Качество | Качество (среднее этапов) | Ошибок | Невалидных по схеме (доля) |",
        "|---|---|---|---|---|---|---|",
    ]
    for name, data in summary["profiles"].items():
        lines.append(
            f"| {name} | {data['auto_runs']} | {_pct(data['auto_pass_rate'])} | "
            f"{_pct(data['mean_quality_score'])} | {_pct(data['stage_macro_quality_score'])} | "
            f"{data['errors']} | {data['schema_invalid']} ({_pct(data['schema_invalid_rate'])}) |"
        )

    lines += [
        "", "## Время и пропускная способность", "",
        "Wall-clock — время всего запуска; при нескольких профилях оно общее, без деления "
        "между профилями. Пропускная способность каждого профиля рассчитана за это общее время.",
        "Латентность кейса измеряется после клиентского ограничения параллелизма: "
        "включает очередь на сервере, но не ожидание свободного клиентского слота.",
        "",
        "| Профиль | Сумма задержек, с | Wall-clock, с | Кейсов/мин | Выходных токенов/с |",
        "|---|---|---|---|---|",
    ]
    for name, data in summary["profiles"].items():
        lines.append(
            f"| {name} | {data['sum_latency_s']:.1f} | {_number(data['wall_s'])} | "
            f"{_number(data['cases_per_min'])} | {_number(data['output_tokens_per_s'])} |"
        )

    lines += ["", "## Лучший профиль по этапам", ""]
    lines += [
        "| Этап | Профиль | Модель | Pass rate | Качество | Оценка (ручн.) | Латентность, с |"
    ]
    lines += ["|---|---|---|---|---|---|---|"]
    for stage, top in summary["best_per_stage"].items():
        grade = "—" if top["mean_grade"] is None else f"{top['mean_grade']:.2f}"
        lines.append(
            f"| {stage} | {top['profile']} | {top['model']} | {_pct(top['pass_rate'])} | "
            f"{_pct(top['mean_quality_score'])} | {grade} | {top['mean_latency_s']:.1f} |"
        )

    lines += ["", "## Матрица этап × профиль", ""]
    lines += [
        "| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Качество | Невалидных по схеме (доля) | "
        "Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for cell in sorted(summary["cells"], key=lambda c: (c["stage"], c["profile"])):
        grade = (
            "—"
            if cell["mean_grade"] is None
            else f"{cell['mean_grade']:.2f} ({cell['graded']})"
        )
        lines.append(
            f"| {cell['stage']} | {cell['kind']} | {cell['profile']} | {cell['model']} | "
            f"{cell['pass']} | {cell['fail']} | {cell['error']} | {_pct(cell['mean_quality_score'])} | "
            f"{cell['schema_invalid']} ({_pct(cell['schema_invalid_rate'])}) | "
            f"{cell['mean_latency_s']:.1f}/{cell['p95_latency_s']:.1f} | "
            f"{cell['mean_input_tokens']:.0f}/{cell['mean_output_tokens']:.0f} | "
            f"{cell['mean_llm_calls']:.1f} | {grade} | {cell['retried']} |"
        )

    lines += [
        "", "## Согласованность повторов", "",
        "Итоги по профилю включают только автоматические этапы; доли рассчитаны по кейсам "
        "с несколькими наблюдаемыми повторами, а не по отдельным прогонам.", "",
        "| Профиль | Этап | Совпадение статусов | Pass^k | Pass@k | Совпадение ответов | Нестабильных кейсов |",
        "|---|---|---|---|---|---|---|",
    ]
    repeat_rows = [
        (name, "Все авто", data) for name, data in summary["profiles"].items()
    ] + [(c["profile"], c["stage"], c) for c in summary["cells"]]
    for profile, stage, data in repeat_rows:
        flaky_count = "—" if data["flaky_cases"] is None else str(len(data["flaky_cases"]))
        lines.append(
            f"| {profile} | {stage} | {_pct(data['stability'])} | "
            f"{_pct(data['pass_all_rate'])} | {_pct(data['pass_any_rate'])} | "
            f"{_pct(data['answer_agreement'])} | {flaky_count} |"
        )
    lines += ["", "### Нестабильные кейсы", ""]
    flaky_cells = [c for c in summary["cells"] if c["flaky_cases"]]
    for cell in flaky_cells:
        lines.append(
            f"- {cell['profile']} / {cell['stage']}: "
            + ", ".join(f"`{_short(case)}`" for case in cell["flaky_cases"])
        )
    if not flaky_cells:
        lines.append("—")

    failures = [r for r in results if r.get("status") in ("fail", "error")]
    lines += ["", f"## Провалы и ошибки ({len(failures)})", ""]
    for result in sorted(
        failures,
        key=lambda r: (r["stage"], r["case"], r["profile"], r.get("repeat", 1)),
    ):
        head = (
            f"- **{result['stage']} / {result['case']}** · {result['profile']} "
            f"#{result.get('repeat', 1)} · {result['status']}"
        )
        if result.get("schema_errors"):
            head += f" — схема: `{_short(result['schema_errors'][0], 300)}`"
        if result.get("error"):
            lines.append(f"{head} — `{_short(result['error'], 300)}`")
            continue
        lines.append(head)
        for check in result.get("checks") or []:
            if not check["passed"]:
                lines.append(
                    f"  - ✗ `{check['name']}`: ожидалось `{_short(check['expected'])}`, "
                    f"получено `{_short(check['actual'])}`"
                )
    lines.append("")
    return "\n".join(lines)


def render_review(results: list[dict[str, Any]]) -> str:
    manual = [r for r in results if r.get("needs_review")]
    by_case: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for result in manual:
        by_case[(result["stage"], result["case"])].append(result)
    lines = [
        "# Ручная проверка ответов",
        "",
        "Шкала (колонка `grade` в grades.csv): **2** — верно и полно, без выдумок; "
        "**1** — в целом верно, есть пропуски или стилистические нарушения правил; "
        "**0** — выдумка, ошибка по сути или нарушение запрета.",
        "",
    ]
    for (stage, case), items in sorted(by_case.items()):
        first = items[0]
        lines += [f"## {stage} / {case}", ""]
        if first.get("review"):
            lines += [f"**Что проверить:** {first['review'].strip()}", ""]
        lines += [
            "<details><summary>Вход</summary>",
            "",
            "```json",
            json.dumps(first.get("input"), ensure_ascii=False, indent=2),
            "```",
            "",
            "</details>",
            "",
        ]
        for item in sorted(items, key=lambda r: (r["profile"], r.get("repeat", 1))):
            failed = [c["name"] for c in item.get("checks") or [] if not c["passed"]]
            status = item["status"] + (
                f" (формальные: ✗ {', '.join(failed)})" if failed else ""
            )
            lines += [
                f"### {item['profile']} · {item.get('model')} · #{item.get('repeat', 1)} · {status} · "
                f"{item.get('latency_s', 0):.1f} с",
                "",
            ]
            if item.get("error"):
                lines += [f"Ошибка: `{item['error']}`", ""]
                continue
            output = item.get("output")
            text = output.get("text") if isinstance(output, dict) else None
            if isinstance(text, str):
                lines += [text.strip() or "_(пустой ответ)_", ""]
            else:
                lines += [
                    "```json",
                    json.dumps(output, ensure_ascii=False, indent=2),
                    "```",
                    "",
                ]
        lines.append("")
    return "\n".join(lines)


def write_grades_template(results_dir: Path, results: list[dict[str, Any]]) -> None:
    path = results_dir / "grades.csv"
    existing = load_grades(results_dir)
    rows = [
        {
            "profile": r["profile"],
            "stage": r["stage"],
            "case": r["case"],
            "repeat": r.get("repeat", 1),
            "model": r.get("model"),
            "grade": existing.get(
                (r["profile"], r["stage"], r["case"], str(r.get("repeat", 1))), ""
            ),
            "comment": "",
        }
        for r in sorted(
            (
                r
                for r in results
                if r.get("needs_review") and r.get("status") != "error"
            ),
            key=lambda r: (r["stage"], r["case"], r["profile"], r.get("repeat", 1)),
        )
    ]
    if not rows or (path.exists() and existing):
        # Never overwrite grades someone already entered.
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=GRADE_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_reports(results_dir: Path, meta: dict[str, Any]) -> dict[str, Any]:
    results = load_results(results_dir)
    write_grades_template(results_dir, results)
    summary = summarize(results, load_grades(results_dir), meta)
    (results_dir / "summary.json").write_text(
        json.dumps({"meta": meta, **summary}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    (results_dir / "report.md").write_text(
        render_report(summary, results, meta), encoding="utf-8"
    )
    review = render_review(results)
    if any(r.get("needs_review") for r in results):
        (results_dir / "review.md").write_text(review, encoding="utf-8")
    return summary
