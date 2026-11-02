# Бенчмарк LLM-этапов gMART — 2026-11-02T17:49:46.329396+03:00

Профили: qwen27b-all · кейсов: 300 · повторов: 1 · датасет: gMART 68534ab3 от 2026-11-02T16:45:00

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| qwen27b-all | 280 | 96% | 97% | 0 | 0 | 2277 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| chat | qwen27b-all | qwen27b | 100% | 100% | 1.00 | 3.7 |
| chat_title | qwen27b-all | qwen27b | 100% | 100% | 1.75 | 14.9 |
| compliance.mapping | qwen27b-all | qwen27b | 83% | 94% | — | 9.5 |
| compliance.mapping_reply | qwen27b-all | qwen27b | 100% | 100% | — | 1.4 |
| compliance.scope | qwen27b-all | qwen27b | 100% | 100% | — | 3.1 |
| compliance.scope_entities | qwen27b-all | qwen27b | 100% | 100% | — | 3.3 |
| dvd.planner | qwen27b-all | qwen27b | 95% | 97% | — | 15.9 |
| norms.answer | qwen27b-all | qwen27b | 100% | 100% | 1.67 | 13.3 |
| norms.planner | qwen27b-all | qwen27b | 100% | 100% | — | 6.9 |
| norms.review | qwen27b-all | qwen27b | 93% | 93% | — | 6.2 |
| orchestrator.plan | qwen27b-all | qwen27b | 96% | 96% | — | 6.2 |
| project.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 2.1 |
| provision.plan | qwen27b-all | qwen27b | 100% | 100% | — | 4.1 |
| pzz.columns | qwen27b-all | qwen27b | 100% | 100% | — | 1.6 |
| pzz.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 1.7 |
| restriction.explain | qwen27b-all | qwen27b | 100% | 100% | 2.00 | 7.0 |
| restriction.plan | qwen27b-all | qwen27b | 100% | 100% | — | 25.1 |
| scenario.candidates.assess | qwen27b-all | qwen27b | 100% | 100% | — | 13.2 |
| scenario.candidates.select | qwen27b-all | qwen27b | 100% | 100% | — | 1.2 |
| scenario.judge | qwen27b-all | qwen27b | 67% | 80% | — | 4.5 |
| scenario.request | qwen27b-all | qwen27b | 93% | 93% | — | 1.9 |
| scenario.select | qwen27b-all | qwen27b | 100% | 100% | — | 0.7 |
| scenario.summary | qwen27b-all | qwen27b | 100% | 100% | 1.67 | 5.7 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chat | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 3.7/3.7 | 56/69 | 1.0 | 1.00 (1) | 0 |
| chat_title | manual | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 14.9/18.1 | 533/226 | 1.0 | 1.75 (4) | 0 |
| compliance.mapping | auto | qwen27b-all | qwen27b | 5 | 1 | 0 | 94% | — | 9.5/19.6 | 488/165 | 1.0 | — | 0 |
| compliance.mapping_reply | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 1.4/3.2 | 300/24 | 1.0 | — | 0 |
| compliance.scope | auto | qwen27b-all | qwen27b | 13 | 0 | 0 | 100% | — | 3.1/4.1 | 546/36 | 1.0 | — | 0 |
| compliance.scope_entities | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 3.3/5.5 | 459/54 | 1.0 | — | 0 |
| dvd.planner | auto | qwen27b-all | qwen27b | 18 | 1 | 0 | 97% | — | 15.9/21.6 | 1387/259 | 1.0 | — | 0 |
| norms.answer | manual | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 13.3/23.1 | 584/208 | 1.0 | 1.67 (9) | 0 |
| norms.planner | auto | qwen27b-all | qwen27b | 16 | 0 | 0 | 100% | — | 6.9/9.2 | 752/101 | 1.0 | — | 0 |
| norms.review | auto | qwen27b-all | qwen27b | 14 | 1 | 0 | 93% | — | 6.2/9.1 | 804/78 | 1.0 | — | 0 |
| orchestrator.plan | auto | qwen27b-all | qwen27b | 50 | 2 | 0 | 96% | — | 6.2/10.0 | 3602/91 | 1.0 | — | 0 |
| project.inputs | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 2.1/2.7 | 267/37 | 1.0 | — | 0 |
| provision.plan | auto | qwen27b-all | qwen27b | 34 | 0 | 0 | 100% | — | 4.1/5.8 | 1100/59 | 1.0 | — | 0 |
| pzz.columns | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 1.6/2.6 | 172/22 | 1.0 | — | 0 |
| pzz.inputs | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 1.7/2.5 | 188/28 | 1.0 | — | 0 |
| restriction.explain | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 7.0/9.4 | 443/102 | 1.0 | 2.00 (3) | 0 |
| restriction.plan | auto | qwen27b-all | qwen27b | 28 | 0 | 0 | 100% | — | 25.1/38.1 | 1462/433 | 1.0 | — | 0 |
| scenario.candidates.assess | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 13.2/20.7 | 275/244 | 1.0 | — | 0 |
| scenario.candidates.select | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 1.2/2.2 | 321/10 | 1.0 | — | 0 |
| scenario.judge | auto | qwen27b-all | qwen27b | 10 | 5 | 0 | 80% | — | 4.5/5.9 | 400/70 | 1.0 | — | 0 |
| scenario.request | auto | qwen27b-all | qwen27b | 13 | 1 | 0 | 93% | — | 1.9/3.1 | 230/28 | 1.0 | — | 0 |
| scenario.select | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 0.7/1.1 | 281/9 | 1.0 | — | 0 |
| scenario.summary | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 5.7/6.1 | 518/91 | 1.0 | 1.67 (3) | 0 |

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
