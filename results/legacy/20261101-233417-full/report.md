# Бенчмарк LLM-этапов gMART — 2026-11-01T23:34:17

Профили: qwen27b-all · кейсов: 113 · повторов: 1 · температура: 0.0

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Суммарное время, с |
|---|---|---|---|---|---|
| qwen27b-all | 105 | 90% | 89% | 4 | 851 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| compliance.mapping | qwen27b-all | qwen27b | 100% | 100% | — | 11.6 |
| compliance.mapping_reply | qwen27b-all | qwen27b | 100% | 100% | — | 1.2 |
| compliance.scope | qwen27b-all | qwen27b | 100% | 100% | — | 1.9 |
| compliance.scope_entities | qwen27b-all | qwen27b | 100% | 100% | — | 2.6 |
| dvd.planner | qwen27b-all | qwen27b | 60% | 83% | — | 1.3 |
| norms.planner | qwen27b-all | qwen27b | 100% | 100% | — | 5.6 |
| norms.review | qwen27b-all | qwen27b | 100% | 100% | — | 4.9 |
| orchestrator.plan | qwen27b-all | qwen27b | 100% | 100% | — | 4.7 |
| project.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 2.3 |
| provision.plan | qwen27b-all | qwen27b | 93% | 96% | — | 4.3 |
| pzz.columns | qwen27b-all | qwen27b | 67% | 67% | — | 1.7 |
| pzz.inputs | qwen27b-all | qwen27b | 50% | 83% | — | 1.5 |
| restriction.plan | qwen27b-all | qwen27b | 89% | 89% | — | 48.4 |
| scenario.candidates | qwen27b-all | qwen27b | 0% | 0% | — | 0.0 |
| scenario.judge | qwen27b-all | qwen27b | 75% | 88% | — | 4.9 |
| scenario.request | qwen27b-all | qwen27b | 100% | 100% | — | 1.4 |
| scenario.select | qwen27b-all | qwen27b | 100% | 100% | — | 0.7 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chat | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 4.6/4.6 | 56/78 | 1.0 | — |
| chat_title | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 20.1/20.1 | 530/372 | 1.0 | — |
| compliance.mapping | auto | qwen27b-all | qwen27b | 2 | 0 | 0 | 100% | — | 11.6/19.6 | 522/208 | 1.0 | — |
| compliance.mapping_reply | auto | qwen27b-all | qwen27b | 5 | 0 | 0 | 100% | — | 1.2/2.0 | 301/18 | 1.0 | — |
| compliance.scope | auto | qwen27b-all | qwen27b | 6 | 0 | 0 | 100% | — | 1.9/3.4 | 544/32 | 1.0 | — |
| compliance.scope_entities | auto | qwen27b-all | qwen27b | 2 | 0 | 0 | 100% | — | 2.6/2.7 | 470/37 | 1.0 | — |
| dvd.planner | auto | qwen27b-all | qwen27b | 3 | 2 | 0 | 83% | — | 1.3/1.5 | 1382/15 | 1.0 | — |
| norms.answer | manual | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 13.2/24.6 | 0/0 | 1.0 | — |
| norms.planner | auto | qwen27b-all | qwen27b | 6 | 0 | 0 | 100% | — | 5.6/6.7 | 744/101 | 1.0 | — |
| norms.review | auto | qwen27b-all | qwen27b | 5 | 0 | 0 | 100% | — | 4.9/6.9 | 835/74 | 1.0 | — |
| orchestrator.plan | auto | qwen27b-all | qwen27b | 23 | 0 | 0 | 100% | — | 4.7/7.8 | 3603/77 | 1.0 | — |
| project.inputs | auto | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 2.3/3.0 | 265/40 | 1.0 | — |
| provision.plan | auto | qwen27b-all | qwen27b | 13 | 1 | 0 | 96% | — | 4.3/6.9 | 1098/57 | 1.0 | — |
| pzz.columns | auto | qwen27b-all | qwen27b | 2 | 1 | 0 | 67% | — | 1.7/2.4 | 104/24 | 1.0 | — |
| pzz.inputs | auto | qwen27b-all | qwen27b | 2 | 2 | 0 | 83% | — | 1.5/1.9 | 115/29 | 1.0 | — |
| restriction.explain | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 3.3/3.3 | 0/0 | 1.0 | — |
| restriction.plan | auto | qwen27b-all | qwen27b | 8 | 0 | 1 | 89% | — | 48.4/227.4 | 1481/850 | 1.0 | — |
| scenario.candidates | auto | qwen27b-all | qwen27b | 0 | 0 | 3 | 0% | — | 0.0/0.0 | 0/0 | 1.0 | — |
| scenario.judge | auto | qwen27b-all | qwen27b | 3 | 1 | 0 | 88% | — | 4.9/6.5 | 404/71 | 1.0 | — |
| scenario.request | auto | qwen27b-all | qwen27b | 6 | 0 | 0 | 100% | — | 1.4/2.0 | 229/26 | 1.0 | — |
| scenario.select | auto | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 0.7/0.9 | 285/9 | 1.0 | — |
| scenario.summary | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 3.8/3.8 | 517/67 | 1.0 | — |

## Провалы и ошибки (11)

- **dvd.planner / editions_comparison** · qwen27b-all #1 · fail
  - ✗ `comparison_topic contains`: ожидалось `["парков"]`, получено `null`
- **dvd.planner / own_documents_only** · qwen27b-all #1 · fail
  - ✗ `include_shared eq`: ожидалось `false`, получено `true`
- **provision.plan / ambiguous_single_service_defaults_to_effects** · qwen27b-all #1 · fail
  - ✗ `mode eq`: ожидалось `effects`, получено `provision`
- **pzz.columns / vri_column_by_values** · qwen27b-all #1 · fail
  - ✗ `columns.cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.inputs / pzz_source_and_year** · qwen27b-all #1 · fail
  - ✗ `source eq`: ожидалось `PZZ`, получено `null`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #1 · fail
  - ✗ `mode eq`: ожидалось `scenario`, получено `building_pzz_check`
- **restriction.plan / normgraph_rule_grounded** · qwen27b-all #1 · error — `LlmResponseError: Incomplete structured answer; no context capacity for a larger output budget`
- **scenario.candidates / nothing_matches** · qwen27b-all #1 · error — `LlmResponseError: Error code: 400 - {'error': {'message': 'No user query found in messages.', 'type': 'BadRequestError', 'param': None, 'code': 400}}`
- **scenario.candidates / pick_exact_meaning_only** · qwen27b-all #1 · error — `LlmResponseError: Error code: 400 - {'error': {'message': 'No user query found in messages.', 'type': 'BadRequestError', 'param': None, 'code': 400}}`
- **scenario.candidates / two_requested_values** · qwen27b-all #1 · error — `LlmResponseError: Error code: 400 - {'error': {'message': 'No user query found in messages.', 'type': 'BadRequestError', 'param': None, 'code': 400}}`
- **scenario.judge / counts_ignored_insufficient** · qwen27b-all #1 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
