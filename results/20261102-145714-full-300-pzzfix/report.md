# Бенчмарк LLM-этапов gMART — 2026-11-02T14:57:14.005731+03:00

Профили: qwen27b-all · кейсов: 300 · повторов: 1 · датасет: gMART 68534ab3 от 2026-11-02T14:56:33

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| qwen27b-all | 280 | 96% | 97% | 2 | 0 | 2680 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| chat | qwen27b-all | qwen27b | 100% | 100% | 1.00 | 4.3 |
| chat_title | qwen27b-all | qwen27b | 100% | 100% | 1.75 | 15.3 |
| compliance.mapping | qwen27b-all | qwen27b | 83% | 94% | — | 11.9 |
| compliance.mapping_reply | qwen27b-all | qwen27b | 100% | 100% | — | 2.0 |
| compliance.scope | qwen27b-all | qwen27b | 100% | 100% | — | 2.8 |
| compliance.scope_entities | qwen27b-all | qwen27b | 100% | 100% | — | 3.7 |
| dvd.planner | qwen27b-all | qwen27b | 100% | 100% | — | 14.6 |
| norms.answer | qwen27b-all | qwen27b | 100% | 100% | 1.78 | 13.9 |
| norms.planner | qwen27b-all | qwen27b | 100% | 100% | — | 6.1 |
| norms.review | qwen27b-all | qwen27b | 93% | 93% | — | 6.2 |
| orchestrator.plan | qwen27b-all | qwen27b | 96% | 96% | — | 6.1 |
| project.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 1.9 |
| provision.plan | qwen27b-all | qwen27b | 100% | 100% | — | 4.2 |
| pzz.columns | qwen27b-all | qwen27b | 100% | 100% | — | 1.7 |
| pzz.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 1.5 |
| restriction.explain | qwen27b-all | qwen27b | 100% | 100% | 2.00 | 8.3 |
| restriction.plan | qwen27b-all | qwen27b | 93% | 93% | — | 38.7 |
| scenario.candidates.assess | qwen27b-all | qwen27b | 100% | 100% | — | 16.8 |
| scenario.candidates.select | qwen27b-all | qwen27b | 100% | 100% | — | 0.8 |
| scenario.judge | qwen27b-all | qwen27b | 67% | 80% | — | 4.9 |
| scenario.request | qwen27b-all | qwen27b | 93% | 93% | — | 1.8 |
| scenario.select | qwen27b-all | qwen27b | 100% | 100% | — | 0.8 |
| scenario.summary | qwen27b-all | qwen27b | 100% | 100% | 1.67 | 6.5 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chat | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 4.3/4.3 | 56/74 | 1.0 | 1.00 (1) | 0 |
| chat_title | manual | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 15.3/29.6 | 533/223 | 1.0 | 1.75 (4) | 0 |
| compliance.mapping | auto | qwen27b-all | qwen27b | 5 | 1 | 0 | 94% | — | 11.9/23.6 | 488/166 | 1.0 | — | 0 |
| compliance.mapping_reply | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 2.0/4.7 | 300/24 | 1.0 | — | 0 |
| compliance.scope | auto | qwen27b-all | qwen27b | 13 | 0 | 0 | 100% | — | 2.8/4.0 | 546/36 | 1.0 | — | 0 |
| compliance.scope_entities | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 3.7/6.4 | 459/54 | 1.0 | — | 0 |
| dvd.planner | auto | qwen27b-all | qwen27b | 19 | 0 | 0 | 100% | — | 14.6/19.5 | 1387/259 | 1.0 | — | 0 |
| norms.answer | manual | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 13.9/26.3 | 584/210 | 1.0 | 1.78 (9) | 0 |
| norms.planner | auto | qwen27b-all | qwen27b | 16 | 0 | 0 | 100% | — | 6.1/7.0 | 752/100 | 1.0 | — | 0 |
| norms.review | auto | qwen27b-all | qwen27b | 14 | 1 | 0 | 93% | — | 6.2/8.4 | 804/78 | 1.0 | — | 0 |
| orchestrator.plan | auto | qwen27b-all | qwen27b | 50 | 2 | 0 | 96% | — | 6.1/9.8 | 3602/94 | 1.0 | — | 0 |
| project.inputs | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 1.9/2.6 | 267/38 | 1.0 | — | 0 |
| provision.plan | auto | qwen27b-all | qwen27b | 34 | 0 | 0 | 100% | — | 4.2/6.5 | 1100/58 | 1.0 | — | 0 |
| pzz.columns | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 1.7/2.9 | 172/22 | 1.0 | — | 0 |
| pzz.inputs | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 1.5/2.0 | 188/28 | 1.0 | — | 0 |
| restriction.explain | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 8.3/12.4 | 443/95 | 1.0 | 2.00 (3) | 0 |
| restriction.plan | auto | qwen27b-all | qwen27b | 26 | 0 | 2 | 93% | — | 38.7/231.9 | 1494/710 | 1.0 | — | 0 |
| scenario.candidates.assess | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 16.8/27.7 | 275/249 | 1.0 | — | 0 |
| scenario.candidates.select | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 0.8/1.9 | 321/10 | 1.0 | — | 0 |
| scenario.judge | auto | qwen27b-all | qwen27b | 10 | 5 | 0 | 80% | — | 4.9/7.0 | 400/71 | 1.0 | — | 0 |
| scenario.request | auto | qwen27b-all | qwen27b | 13 | 1 | 0 | 93% | — | 1.8/3.2 | 230/28 | 1.0 | — | 0 |
| scenario.select | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 0.8/1.2 | 281/9 | 1.0 | — | 0 |
| scenario.summary | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 6.5/8.4 | 518/87 | 1.0 | 1.67 (3) | 0 |

## Провалы и ошибки (12)

- **compliance.mapping / clear_school_high_confidence** · qwen27b-all #1 · fail
  - ✗ `items[id=2].entity ne`: ожидалось `Жилой дом`, получено `Жилой дом`
- **norms.review / insufficient_context_needs_refinement** · qwen27b-all #1 · fail
  - ✗ `satisfied eq`: ожидалось `false`, получено `true`
  - ✗ `refined_search_query null`: ожидалось `false`, получено `null`
- **orchestrator.plan / check_with_evidence_single_step** · qwen27b-all #1 · fail
  - ✗ `steps[*].agent eq`: ожидалось `["compliance"]`, получено `["compliance", "documents"]`
- **orchestrator.plan / pzz_building_files_mode** · qwen27b-all #1 · fail
  - ✗ `steps[*].agent eq`: ожидалось `["pzz"]`, получено `[]`
  - ✗ `steps.0.task contains`: ожидалось `["здани"]`, получено `null`
- **restriction.plan / normgraph_named_document_among_conflicting** · qwen27b-all #1 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
- **restriction.plan / repeated_norm_stays_normgraph** · qwen27b-all #1 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
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
