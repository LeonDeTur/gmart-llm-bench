# Бенчмарк LLM-этапов gMART — 2026-11-02T23:18:10.105999+03:00

Бенчмарк: 1bced712 · vllm-dev: 0.32.0

Профили: qwen27b-all · кейсов: 300 · повторов: 1 · датасет: gMART 3ccccfb8 от 2026-11-02T18:40:55

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| qwen27b-all | 280 | 96% | 98% | 0 | 0 | 2385 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| chat | qwen27b-all | qwen27b | 100% | 100% | 1.00 | 3.8 |
| chat_title | qwen27b-all | qwen27b | 100% | 100% | 1.75 | 14.6 |
| compliance.mapping | qwen27b-all | qwen27b | 83% | 96% | — | 10.7 |
| compliance.mapping_reply | qwen27b-all | qwen27b | 100% | 100% | — | 1.7 |
| compliance.scope | qwen27b-all | qwen27b | 100% | 100% | — | 2.8 |
| compliance.scope_entities | qwen27b-all | qwen27b | 100% | 100% | — | 4.1 |
| dvd.planner | qwen27b-all | qwen27b | 95% | 98% | — | 15.8 |
| norms.answer | qwen27b-all | qwen27b | 100% | 100% | 1.67 | 12.0 |
| norms.planner | qwen27b-all | qwen27b | 100% | 100% | — | 6.8 |
| norms.review | qwen27b-all | qwen27b | 93% | 96% | — | 5.1 |
| orchestrator.plan | qwen27b-all | qwen27b | 96% | 98% | — | 7.0 |
| project.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 2.0 |
| provision.plan | qwen27b-all | qwen27b | 100% | 100% | — | 4.4 |
| pzz.columns | qwen27b-all | qwen27b | 100% | 100% | — | 1.4 |
| pzz.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 1.8 |
| restriction.explain | qwen27b-all | qwen27b | 100% | 100% | 2.00 | 6.2 |
| restriction.plan | qwen27b-all | qwen27b | 100% | 100% | — | 27.7 |
| scenario.candidates.assess | qwen27b-all | qwen27b | 100% | 100% | — | 14.9 |
| scenario.candidates.select | qwen27b-all | qwen27b | 100% | 100% | — | 1.7 |
| scenario.judge | qwen27b-all | qwen27b | 67% | 88% | — | 4.1 |
| scenario.request | qwen27b-all | qwen27b | 93% | 96% | — | 1.8 |
| scenario.select | qwen27b-all | qwen27b | 100% | 100% | — | 0.8 |
| scenario.summary | qwen27b-all | qwen27b | 100% | 100% | 1.67 | 5.7 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chat | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 3.8/3.8 | 56/78 | 1.0 | 1.00 (1) | 0 |
| chat_title | manual | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 14.6/18.1 | 533/250 | 1.0 | 1.75 (4) | 0 |
| compliance.mapping | auto | qwen27b-all | qwen27b | 5 | 1 | 0 | 96% | — | 10.7/21.4 | 488/166 | 1.0 | — | 0 |
| compliance.mapping_reply | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 1.7/4.8 | 300/24 | 1.0 | — | 0 |
| compliance.scope | auto | qwen27b-all | qwen27b | 13 | 0 | 0 | 100% | — | 2.8/3.9 | 546/36 | 1.0 | — | 0 |
| compliance.scope_entities | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 4.1/6.4 | 459/62 | 1.0 | — | 0 |
| dvd.planner | auto | qwen27b-all | qwen27b | 18 | 1 | 0 | 98% | — | 15.8/20.7 | 1387/260 | 1.0 | — | 0 |
| norms.answer | manual | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 12.0/22.8 | 584/210 | 1.0 | 1.67 (9) | 0 |
| norms.planner | auto | qwen27b-all | qwen27b | 16 | 0 | 0 | 100% | — | 6.8/8.7 | 752/101 | 1.0 | — | 0 |
| norms.review | auto | qwen27b-all | qwen27b | 14 | 1 | 0 | 96% | — | 5.1/6.9 | 804/78 | 1.0 | — | 0 |
| orchestrator.plan | auto | qwen27b-all | qwen27b | 50 | 2 | 0 | 98% | — | 7.0/10.9 | 3602/93 | 1.0 | — | 0 |
| project.inputs | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 2.0/2.2 | 267/37 | 1.0 | — | 0 |
| provision.plan | auto | qwen27b-all | qwen27b | 34 | 0 | 0 | 100% | — | 4.4/6.5 | 1100/58 | 1.0 | — | 0 |
| pzz.columns | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 1.4/2.7 | 172/22 | 1.0 | — | 0 |
| pzz.inputs | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 1.8/2.4 | 188/28 | 1.0 | — | 0 |
| restriction.explain | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 6.2/9.6 | 443/98 | 1.0 | 2.00 (3) | 0 |
| restriction.plan | auto | qwen27b-all | qwen27b | 28 | 0 | 0 | 100% | — | 27.7/37.5 | 1462/436 | 1.0 | — | 0 |
| scenario.candidates.assess | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 14.9/24.5 | 275/247 | 1.0 | — | 0 |
| scenario.candidates.select | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 1.7/3.8 | 321/11 | 1.0 | — | 0 |
| scenario.judge | auto | qwen27b-all | qwen27b | 10 | 5 | 0 | 88% | — | 4.1/5.8 | 400/69 | 1.0 | — | 0 |
| scenario.request | auto | qwen27b-all | qwen27b | 13 | 1 | 0 | 96% | — | 1.8/3.4 | 230/28 | 1.0 | — | 0 |
| scenario.select | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 0.8/1.2 | 281/9 | 1.0 | — | 0 |
| scenario.summary | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 5.7/6.7 | 518/86 | 1.0 | 1.67 (3) | 0 |

## Провалы и ошибки (11)

- **compliance.mapping / clear_school_high_confidence** · qwen27b-all #1 · fail
  - ✗ `items[id=2].entity ne`: ожидалось `Жилой дом`, получено `Жилой дом`
- **dvd.planner / table_requested** · qwen27b-all #1 · fail
  - ✗ `types null`: ожидалось `true`, получено `["table"]`
- **norms.review / insufficient_context_needs_refinement** · qwen27b-all #1 · fail
  - ✗ `satisfied eq`: ожидалось `false`, получено `true`
  - ✗ `refined_search_query null`: ожидалось `false`, получено `null`
- **orchestrator.plan / check_with_evidence_single_step** · qwen27b-all #1 · fail
  - ✗ `steps[*].agent eq`: ожидалось `["compliance"]`, получено `["compliance", "documents"]`
- **orchestrator.plan / pzz_building_files_mode** · qwen27b-all #1 · fail
  - ✗ `steps[*].agent eq`: ожидалось `["pzz"]`, получено `[]`
  - ✗ `steps.0.task contains`: ожидалось `["здани"]`, получено `null`
- **scenario.judge / counts_ignored_insufficient** · qwen27b-all #1 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
- **scenario.judge / general_scope_not_scenario** · qwen27b-all #1 · fail
  - ✗ `sufficient eq`: ожидалось `false`, получено `true`
- **scenario.judge / promise_without_data_insufficient** · qwen27b-all #1 · fail
  - ✗ `missing_code ne`: ожидалось `none`, получено `none`
- **scenario.judge / vague_words_insufficient** · qwen27b-all #1 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
- **scenario.judge / zero_without_calls_insufficient** · qwen27b-all #1 · fail
  - ✗ `missing_code ne`: ожидалось `none`, получено `none`
- **scenario.request / map_several_types_unsupported** · qwen27b-all #1 · fail
  - ✗ `operation eq`: ожидалось `unsupported`, получено `map`
