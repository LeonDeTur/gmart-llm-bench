"""Run profiles sequentially and bounded case repetitions concurrently."""

import asyncio
import json
import logging
import time
from contextlib import AsyncExitStack
from pathlib import Path

import httpx

from llmbench.checks import CheckResult, evaluate_check, score
from llmbench.client import Completion, complete
from llmbench.config import BenchConfig
from llmbench.parse import schema_errors, to_output

logger = logging.getLogger(__name__)


class Runner:
    def __init__(
        self,
        config: BenchConfig,
        case_timeout_s: float = 900,
        save_prompts: bool = False,
    ):
        self.config = config
        self.case_timeout_s = case_timeout_s
        self.save_prompts = save_prompts

    async def run(self, cases, profiles, out_file):
        self.config.validate()
        cases = [case for case in cases if case.status == "ok"]
        profiles = list(profiles)
        total = len(cases) * len(profiles) * self.config.repeat
        done = 0
        records = []
        semaphore = asyncio.Semaphore(self.config.concurrency)
        out_file = Path(out_file)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        async with AsyncExitStack() as stack:
            clients = {
                name: await stack.enter_async_context(
                    httpx.AsyncClient(timeout=ep.timeout)
                )
                for name, ep in self.config.endpoints.items()
            }
            with out_file.open("a", encoding="utf-8") as handle:

                async def run_one(case, profile, rep):
                    nonlocal done
                    async with semaphore:
                        started = time.perf_counter()
                        model_name = profile.model_for(case.stage)
                        model = self.config.models.get(model_name)
                        record = dict(
                            profile=profile.name,
                            stage=case.stage,
                            case=case.id,
                            tags=case.tags,
                            repeat=rep,
                            model=model_name,
                            model_id=model.model if model else None,
                            endpoint=model.endpoint if model else None,
                            kind=case.kind,
                            input=case.input,
                            review=case.review,
                            status="skipped",
                            needs_review=case.kind == "manual",
                            score=0,
                            checks=[],
                            output=None,
                            error=None,
                            latency_s=0,
                            llm_calls=0,
                            attempts=[],
                            request_params={},
                            input_tokens=None,
                            output_tokens=None,
                            retried=False,
                            done_reason=None,
                            schema_errors=[],
                            content="",
                            thinking="",
                        )
                        if self.save_prompts:
                            record["request"] = case.request
                        if model is not None:
                            completion = Completion("", "", None, None, None, False, 0)
                            try:
                                completion = await asyncio.wait_for(
                                    complete(
                                        self.config.endpoints[model.endpoint],
                                        model,
                                        case.request,
                                        clients[model.endpoint],
                                        progress=completion,
                                    ),
                                    timeout=self.case_timeout_s,
                                )
                                for key in (
                                    "content",
                                    "thinking",
                                    "done_reason",
                                    "input_tokens",
                                    "output_tokens",
                                    "retried",
                                    "latency_s",
                                    "attempts",
                                    "request_params",
                                ):
                                    record[key] = getattr(completion, key)
                                record["llm_calls"] = completion.calls
                                output, error = to_output(case.kind, completion.content)
                                if error:
                                    raise ValueError(error)
                                record["output"] = output
                                record["schema_errors"] = schema_errors(
                                    output, case.request.get("format")
                                )
                                checks = [
                                    evaluate_check(output, check)
                                    for check in case.expect
                                ]
                                if case.kind == "auto" and isinstance(
                                    case.request.get("format"), dict
                                ):
                                    checks.append(
                                        CheckResult(
                                            name="$ schema",
                                            passed=not record["schema_errors"],
                                            weight=1,
                                            actual=record["schema_errors"],
                                            expected=[],
                                        )
                                    )
                                record.update(
                                    checks=[check.to_dict() for check in checks],
                                    score=score(checks),
                                    status=(
                                        "pass"
                                        if all(c.passed for c in checks)
                                        else "fail"
                                    ),
                                )
                            except Exception as exc:
                                for key in (
                                    "content",
                                    "thinking",
                                    "done_reason",
                                    "input_tokens",
                                    "output_tokens",
                                    "retried",
                                    "attempts",
                                    "request_params",
                                ):
                                    record[key] = getattr(completion, key)
                                record["llm_calls"] = completion.calls
                                record.update(
                                    status="error",
                                    score=0,
                                    checks=[],
                                    error=(
                                        "Превышено время ожидания"
                                        if isinstance(exc, TimeoutError)
                                        else f"{type(exc).__name__}: {exc}"
                                    ),
                                    latency_s=time.perf_counter() - started,
                                )
                        handle.write(
                            json.dumps(record, ensure_ascii=False, default=str) + "\n"
                        )
                        handle.flush()
                        records.append(record)
                        done += 1
                        logger.info(
                            "[%s/%s] %s %s #%s: %s score=%.2f %.1fs",
                            done,
                            total,
                            profile.name,
                            case.key,
                            rep,
                            record["status"],
                            record["score"],
                            record["latency_s"],
                        )

                for profile in profiles:
                    await asyncio.gather(
                        *(
                            run_one(case, profile, rep)
                            for case in cases
                            for rep in range(1, self.config.repeat + 1)
                        )
                    )
        return records
