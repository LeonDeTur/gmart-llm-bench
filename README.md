---
pretty_name: gMART LLM stage benchmark
language:
  - ru
tags:
  - benchmark
  - llm-evaluation
  - structured-output
  - urban-planning
configs:
  - config_name: requests
    data_files: data/requests.jsonl
---

# gmart-llm-bench

**English** · [Русский](README.ru.md)

A benchmark of the LLM stages of gMART, a multi-agent system for urban planning: it shows which
model, or which combination of models, handles each step of the agents best. It runs **without
gMART or any of its services**. All you need is Python 3.11+ and access to a model (vLLM or any
other OpenAI-compatible server, or Ollama).

Each case is exactly one request to the model, in the form gMART sends it (system prompt, data,
JSON schema of the answer, parameters), plus deterministic checks of the answer. Request →
answer → checks, with no agent code in between.

The prompts, inputs and expected answers are in Russian, the language the agents work in.

## Quick start

```bash
git clone <url> gmart-llm-bench && cd gmart-llm-bench
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
cp config.example.yaml config.yaml                 # model addresses; the file is in .gitignore
llmbench list                                      # stages, cases, state of the requests
llmbench run --config config.yaml --tags smoke     # quick run
llmbench run --config config.yaml                  # all cases
```

The addresses do not have to be written into the file: `config.example.yaml` reads them from the
environment (`BENCH_VLLM_URL`, `BENCH_VLLM_API_KEY`, `BENCH_GPTOSS_URL`, `BENCH_OLLAMA_URL`).
`python -m llmbench` works in place of `llmbench`.

## Comparing models

`config.yaml` describes three levels:

- **endpoints** — servers: `backend: openai` (vLLM and others) or `ollama`, address, key, timeout,
  and how the server is told to turn reasoning off (`think_mode`: `reasoning_effort`,
  `chat_template` — needed for qwen3 on vLLM, `off`);
- **models** — named models on those servers; their `options` are added to every request
  (for example `num_ctx` for Ollama, or `temperature`);
- **profiles** — which model runs which stage: `default` for all stages, `stages` for overrides
  by id or glob (`"scenario.*": qwen14b`). Profiles are compared with each other.

```bash
llmbench run --config config.yaml --models qwen27b,gptoss20b       # one profile per model
llmbench run --config config.yaml --profiles mixed --stages "orchestrator.*,provision.*"
llmbench run --config config.yaml --repeat 3 --label stability     # measure stability
```

Profiles run one after another (two models on one shared server at once would distort latency);
cases within a profile run in parallel (`run.concurrency`).

### Holdout set

About a fifth of the cases carry the `holdout` tag. Leave them out while choosing models,
parameters or prompts, and run them only to confirm the final choice, so the score is not fitted
to the cases it is reported on:

```bash
llmbench run --config config.yaml --exclude-tags holdout --label tuning   # while tuning
llmbench run --config config.yaml --tags holdout --label final            # final check
```

`run.exclude_tags` in `config.yaml` does the same as `--exclude-tags`.

## Results

`results/<date-time>[-label]/`:

| File | Contents |
|---|---|
| `report.md` | summary per profile, best profile per stage, stage × profile matrix (pass rate, score, latency, tokens, schema-invalid answers, retries), every failed check |
| `review.md` | answers of manual stages side by side per profile, for a human to read |
| `grades.csv` | template for manual grades 0–2; once filled in, `llmbench report <dir>` folds them into the report |
| `results.jsonl` | one record per case run: raw answer, parsed JSON, checks, tokens; `request_params` stores the final request body without `messages`, with the schema replaced by its hash and title |
| `summary.json` | run summary |
| `meta.json` | dataset version, benchmark commit and tracked changes in `llmbench`/`cases`/`data`, endpoints without `api_key` or URL userinfo/query/fragment, server versions (vLLM `/version`, Ollama `/api/version`), run parameters |

`--save-prompts` also stores the request itself in `results.jsonl`.

The `results/` directory of this repository holds runs of qwen3.8-27b on vLLM;
`results/legacy/` holds earlier runs made by the previous, gMART-bound version of the runner
(a different record format).

## Stages

`llmbench list` shows the stages and their kind:

- **auto** — the model answers with JSON that follows a schema; scored by the checks. An
  answer that does not parse as JSON is a case error; JSON that violates the schema fails the
  synthetic `$ schema` check, affecting both the score and pass/fail. The "schema-invalid"
  column remains.
- **manual** — free text (answers about norms, explanations, summaries, chat titles): formal
  checks (language, length, citations, prohibitions) plus a human grade in `review.md`.

What is measured is **the model itself**: the way gMART's code post-processes the answer
(canonical names, clamping, repair passes, a repeated request after a validation error) is not
part of the benchmark. The one thing the runner repeats after gMART is a single retry with a
larger `max_tokens` when a structured answer from an OpenAI-compatible server is cut off or
empty (gMART's adapter does the same); such runs show up in the "Retries" column. In the results,
`llm_calls` is the actual number of HTTP calls; `attempts` records `done_reason`, input/output
tokens and `max_tokens` for each attempt. Token totals are summed across attempts.

## Cases and checks

`cases/*.yaml` — one file per group of stages:

```yaml
stage: provision.plan
defaults: {services_catalog: [Школа, Поликлиника]}   # merged into every case's input
cases:
  - id: single_service_provision
    tags: [smoke]
    input: {user_query: "Какая обеспеченность школами?"}
    expect:
      - {path: mode, eq: provision}
      - {path: service_name, eq: Школа}
    review: "what to look at by eye (for manual stages)"
```

A check is a path into the model's answer and one operator: `eq`, `ne`, `in`, `not_in`,
`set_eq`, `contains`, `not_contains`, `contains_any`, `subset`, `len`, `min_len`, `max_len`,
`null`, `regex`, `not_regex`, `approx` (+`tol`), `gte`, `lte`. Optional `weight` (its weight in
the case score) and `name` (its label in the report). Strings are compared ignoring case,
`ё`/`е` and extra whitespace.

Paths: `steps.0.agent` is a list element by index, `steps[*].agent` is a field of every element,
`items[id=1].confidence` is the list element whose `id` field equals `1`
(`selections[topic=жилой дом].entities`).

**Checks (`expect`, `review`, `tags`) can be edited freely.** `input` is what gMART built the
request from, so changing it or adding a case requires a new export (see below); until then
`llmbench list` shows the case as `stale`/`missing` and `run` skips it.

## Dataset

- `data/requests.jsonl` — the frozen requests: `stage`, `case`, `input_sha` (hash of the case
  input the request was built from) and `request` (`messages`, `format` — the JSON schema of the
  answer, `options`, `think`, other call parameters).
- `data/manifest.json` — the gMART commit the dataset was exported from, the date, the kinds of
  the stages.

The requests are exported by the exporter in gMART (`benchmarks/` in the
[gMART repository](https://github.com/IDUclub/gMART)) whenever the agents' prompts or the case
inputs change:

```bash
# in gMART, with gmart-llm-bench cloned next to it
uv run python -m benchmarks export --bench ../gmart-llm-bench
```

## Development

```bash
pip install -e ".[test]"
pytest
```
