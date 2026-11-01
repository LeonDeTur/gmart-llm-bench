"""Command line entry point for standalone benchmarks."""

import argparse
import asyncio
import json
import logging
import re
import sys
from collections import Counter
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from llmbench.config import load_config
from llmbench.dataset import load_dataset, select
from llmbench.report import write_reports
from llmbench.runner import Runner

ROOT = Path(__file__).resolve().parent.parent
logger = logging.getLogger(__name__)


def _csv(value):
    return (
        [part.strip() for part in value.split(",") if part.strip()] if value else None
    )


def _parser():
    parser = argparse.ArgumentParser(description="Бенчмарк LLM-этапов gMART")
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list", help="Показать этапы и состояние запросов")
    listing.add_argument("--root", type=Path, default=ROOT)
    run = sub.add_parser("run", help="Запустить бенчмарк")
    run.add_argument("--config", required=True, type=Path)
    for name in ("profiles", "models", "stages", "cases", "tags", "label"):
        run.add_argument(f"--{name}")
    for name in ("repeat", "concurrency"):
        run.add_argument(f"--{name}", type=int)
    run.add_argument("--case-timeout", type=float, default=900)
    run.add_argument("--save-prompts", action="store_true")
    run.add_argument("--out", type=Path)
    run.add_argument("--root", type=Path, default=ROOT)
    report = sub.add_parser("report", help="Пересобрать отчёты с ручными оценками")
    report.add_argument("results_dir", type=Path)
    return parser


def _run(args):
    config = load_config(args.config)
    if args.repeat is not None:
        config.repeat = args.repeat
    if args.concurrency is not None:
        config.concurrency = args.concurrency
    config.validate()
    if args.case_timeout <= 0:
        raise ValueError("Время ожидания должно быть положительным")
    names = _csv(args.profiles)
    if args.models:
        created = config.add_single_model_profiles(_csv(args.models))
        names = (names or []) + created
    profiles = config.select_profiles(names)
    dataset = load_dataset(args.root)
    selected = select(
        dataset.cases,
        _csv(args.stages) or config.stages,
        _csv(args.cases),
        _csv(args.tags) or config.tags,
    )
    for case in selected:
        if case.status != "ok":
            logger.warning("Пропуск %s: %s", case.key, case.status)
    for orphan in dataset.orphans:
        logger.warning("Запрос без кейса: %s", orphan)
    ready = [case for case in selected if case.status == "ok"]
    if (
        not ready
        or not profiles
        or not any(p.model_for(c.stage) is not None for p in profiles for c in ready)
    ):
        logger.error("Нет кейсов для запуска")
        return 2
    started = datetime.now().astimezone()
    label = re.sub(r"[^\w.-]+", "-", args.label or "").strip(".-")
    out = (
        args.out
        if args.out is not None
        else args.root
        / "results"
        / (started.strftime("%Y%m%d-%H%M%S") + (f"-{label}" if label else ""))
    )
    out.mkdir(parents=True, exist_ok=True)
    if any((out / name).exists() for name in ("meta.json", "results.jsonl")):
        raise ValueError(f"Каталог уже содержит результаты: {out}")
    meta = dict(
        started=started.isoformat(),
        config=str(args.config.resolve()),
        profiles=[p.name for p in profiles],
        profile_models={
            p.name: {c.stage: p.model_for(c.stage) for c in ready} for p in profiles
        },
        models={name: asdict(model) for name, model in config.models.items()},
        cases=len(ready),
        repeat=config.repeat,
        dataset={
            **dataset.manifest.get("gmart", {}),
            "exported_at": dataset.manifest.get("exported_at", ""),
        },
    )
    (out / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    asyncio.run(
        Runner(config, args.case_timeout, args.save_prompts).run(
            ready, profiles, out / "results.jsonl"
        )
    )
    write_reports(out, meta)
    logger.info("Отчёты: %s", out)
    return 0


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    # httpx logs every request with the server address; progress lines are enough.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    args = _parser().parse_args(argv)
    try:
        if args.command == "report":
            meta = json.loads(
                (args.results_dir / "meta.json").read_text(encoding="utf-8")
            )
            write_reports(args.results_dir, meta)
            return 0
        if args.command == "run":
            return _run(args)
        dataset = load_dataset(args.root)
        for stage in sorted(
            {case.stage for case in dataset.cases}
            | set(dataset.manifest.get("stages", {}))
        ):
            cases = [case for case in dataset.cases if case.stage == stage]
            counts = Counter(case.status for case in cases)
            kind = dataset.manifest.get("stages", {}).get(stage, {}).get("kind", "auto")
            print(
                f"{stage} [{kind}]: кейсов {len(cases)} · "
                + " · ".join(
                    f"{s}={counts[s]}" for s in ("ok", "missing", "stale", "code")
                )
            )
        print(f"Запросов без кейса: {len(dataset.orphans)}")
        for key in dataset.orphans:
            print(f"  {key}")
        return int(any(c.status in ("missing", "stale") for c in dataset.cases))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        logger.error("Ошибка: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
