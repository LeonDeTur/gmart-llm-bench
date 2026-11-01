# Бенчмарк LLM-этапов gMART — 2026-11-01T23:48:38

Профили: qwen27b-all · кейсов: 8 · повторов: 1 · температура: 0.0

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Суммарное время, с |
|---|---|---|---|---|---|
| qwen27b-all | 8 | 0% | 17% | 3 | 8 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| dvd.planner | qwen27b-all | qwen27b | 0% | 35% | — | 1.5 |
| scenario.candidates | qwen27b-all | qwen27b | 0% | 0% | — | 0.2 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dvd.planner | auto | qwen27b-all | qwen27b | 0 | 5 | 0 | 35% | — | 1.5/1.6 | 1382/15 | 1.0 | — |
| scenario.candidates | auto | qwen27b-all | qwen27b | 0 | 0 | 3 | 0% | — | 0.2/0.2 | 0/0 | 1.0 | — |

## Провалы и ошибки (8)

- **dvd.planner / document_list_intent** · qwen27b-all #1 · fail
  - ✗ `intent eq`: ожидалось `document_list`, получено `norm`
  - ✗ `search_query contains`: ожидалось `["детск"]`, получено ``
- **dvd.planner / editions_comparison** · qwen27b-all #1 · fail
  - ✗ `intent eq`: ожидалось `document_comparison`, получено `norm`
  - ✗ `comparison_topic contains`: ожидалось `["парков"]`, получено `null`
- **dvd.planner / exact_clause_structure** · qwen27b-all #1 · fail
  - ✗ `retrieval_mode eq`: ожидалось `structure`, получено `semantic`
  - ✗ `pattern eq`: ожидалось `3.3`, получено `null`
- **dvd.planner / own_documents_only** · qwen27b-all #1 · fail
  - ✗ `include_shared eq`: ожидалось `false`, получено `true`
  - ✗ `search_query contains`: ожидалось `["озеленен"]`, получено ``
- **dvd.planner / semantic_topic** · qwen27b-all #1 · fail
  - ✗ `search_query contains`: ожидалось `["инсоляц"]`, получено ``
- **scenario.candidates / nothing_matches** · qwen27b-all #1 · error — `LlmResponseError: Error code: 400 - {'error': {'message': 'No user query found in messages.', 'type': 'BadRequestError', 'param': None, 'code': 400}}`
- **scenario.candidates / pick_exact_meaning_only** · qwen27b-all #1 · error — `LlmResponseError: Error code: 400 - {'error': {'message': 'No user query found in messages.', 'type': 'BadRequestError', 'param': None, 'code': 400}}`
- **scenario.candidates / two_requested_values** · qwen27b-all #1 · error — `LlmResponseError: Error code: 400 - {'error': {'message': 'No user query found in messages.', 'type': 'BadRequestError', 'param': None, 'code': 400}}`
