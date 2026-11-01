# gmart-llm-bench

Бенчмарк LLM-этапов мультиагентной системы gMART: какая модель или комбинация моделей
лучше справляется с каждым шагом агентов. Работает **без gMART и без его сервисов** — нужны
только Python 3.11+ и доступ к модели (vLLM / любой OpenAI-совместимый сервер или Ollama).

Каждый кейс — это ровно один запрос к модели в том виде, в каком его отправляет gMART
(системный промпт, данные, JSON-схема ответа, параметры), плюс детерминированные проверки
ответа. Запрос → ответ → проверки, без кода агентов между ними.

## Быстрый старт

```bash
git clone <url> gmart-llm-bench && cd gmart-llm-bench
python -m venv .venv && . .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
cp config.example.yaml config.yaml                 # адреса моделей; файл в .gitignore
llmbench list                                      # этапы, кейсы, состояние запросов
llmbench run --config config.yaml --tags smoke     # быстрый прогон
llmbench run --config config.yaml                  # все кейсы
```

Адреса можно не писать в файл: `config.example.yaml` берёт их из окружения
(`BENCH_VLLM_URL`, `BENCH_VLLM_API_KEY`, `BENCH_GPTOSS_URL`, `BENCH_OLLAMA_URL`).
Вместо `llmbench` можно писать `python -m llmbench`.

## Сравнение моделей

`config.yaml` описывает три уровня:

- **endpoints** — серверы: `backend: openai` (vLLM и др.) или `ollama`, адрес, ключ, таймаут
  и то, как серверу передаётся отключение размышлений (`think_mode`: `reasoning_effort`,
  `chat_template` — нужно qwen3 на vLLM, `off`);
- **models** — именованные модели на серверах; `options` добавляются к каждому запросу
  (например, `num_ctx` для Ollama или `temperature`);
- **profiles** — какая модель на каком этапе: `default` для всех, `stages` — переопределения
  по id или glob (`"scenario.*": qwen14b`). Сравниваются профили между собой.

```bash
llmbench run --config config.yaml --models qwen27b,gptoss20b       # по профилю на модель
llmbench run --config config.yaml --profiles mixed --stages "orchestrator.*,provision.*"
llmbench run --config config.yaml --repeat 3 --label stability     # оценка стабильности
```

Профили прогоняются по очереди (общий сервер под двумя моделями сразу исказил бы
латентность), кейсы внутри профиля — параллельно (`run.concurrency`).

## Результаты

`results/<дата-время>[-label]/`:

| Файл | Что в нём |
|---|---|
| `report.md` | итог по профилям, лучший профиль по этапам, матрица этап × профиль (pass rate, балл, латентность, токены, невалидные по схеме ответы, повторы), все проваленные проверки |
| `review.md` | ответы ручных этапов рядом по профилям — для проверки глазами |
| `grades.csv` | шаблон ручных оценок 0–2; после заполнения `llmbench report <каталог>` включает их в отчёт |
| `results.jsonl` | запись на каждый прогон кейса: сырой ответ, разобранный JSON, проверки, токены |
| `summary.json`, `meta.json` | сводка и параметры прогона, включая версию датасета |

`--save-prompts` добавляет в `results.jsonl` сам запрос.

## Этапы

`llmbench list` выводит этапы и их тип:

- **auto** — модель отвечает JSON по схеме; оценка только по проверкам. Ответ, который не
  разбирается как JSON, — ошибка кейса; JSON, нарушающий схему, считается отдельно
  («невалидных по схеме») и оценивается проверками как есть.
- **manual** — свободный текст (ответы по нормам, объяснения, сводки, названия чатов):
  формальные проверки (язык, длина, ссылки, запреты) плюс ручная оценка в `review.md`.

Оценивается **сама модель**: обработка ответа кодом gMART (канонизация названий, clamp,
repair-проходы, повторный запрос при ошибке валидации) в бенчмарк не входит. Единственное,
что раннер повторяет за gMART, — один повторный запрос с бо́льшим `max_tokens`, если
структурированный ответ на OpenAI-совместимом сервере оборвался или пуст (так делает
адаптер gMART); такие прогоны видны в колонке «Повторы».

## Кейсы и проверки

`cases/*.yaml` — по файлу на группу этапов:

```yaml
stage: provision.plan
defaults: {services_catalog: [Школа, Поликлиника]}   # подмешивается во input каждого кейса
cases:
  - id: single_service_provision
    tags: [smoke]
    input: {user_query: "Какая обеспеченность школами?"}
    expect:
      - {path: mode, eq: provision}
      - {path: service_name, eq: Школа}
    review: "что проверить глазами (для manual-этапов)"
```

Проверка — путь в ответе модели и один оператор: `eq`, `ne`, `in`, `not_in`, `set_eq`,
`contains`, `not_contains`, `contains_any`, `subset`, `len`, `min_len`, `max_len`, `null`,
`regex`, `not_regex`, `approx` (+`tol`), `gte`, `lte`. Необязательные `weight` (вес в балле
кейса) и `name` (подпись в отчёте). Строки сравниваются без учёта регистра, `ё`/`е` и лишних
пробелов.

Пути: `steps.0.agent` — элемент списка по индексу, `steps[*].agent` — поле у всех элементов,
`items[id=1].confidence` — элемент списка, у которого поле `id` равно `1`
(`selections[topic=жилой дом].entities`).

**Проверки (`expect`, `review`, `tags`) можно править свободно.** `input` — это то, из чего
gMART собрал запрос, поэтому его правка или новый кейс требуют повторного экспорта
(см. ниже); до этого `llmbench list` показывает кейс как `stale`/`missing`, а `run` его
пропускает.

## Датасет

- `data/requests.jsonl` — замороженные запросы: `stage`, `case`, `input_sha` (хэш входа кейса,
  из которого собран запрос) и `request` (`messages`, `format` — JSON-схема ответа,
  `options`, `think`, прочие параметры вызова).
- `data/manifest.json` — коммит gMART, из которого выгружен датасет, дата, типы этапов.

Запросы выгружает экспортёр в gMART (`benchmarks/` в репозитории gMART), когда меняются
промпты агентов или входы кейсов:

```bash
# в gMART, gmart-llm-bench склонирован рядом
uv run python -m benchmarks export --bench ../gmart-llm-bench
```

## Разработка

```bash
pip install -e ".[test]"
pytest
```
