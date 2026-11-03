# Бенчмарк LLM-этапов gMART — 2026-11-03T13:02:22.572940+03:00

Бенчмарк: b5403ca3 (есть незакоммиченные изменения) · vllm-dev: 0.32.0

Профили: qwen27b-all · кейсов: 300 · повторов: 1 · датасет: gMART 9eb3495c от 2026-11-03T13:02:16

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| qwen27b-all | 280 | 98% | 99% | 0 | 0 | 2669 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| compliance.mapping | qwen27b-all | qwen27b | 83% | 96% | — | 14.7 |
| compliance.mapping_reply | qwen27b-all | qwen27b | 100% | 100% | — | 2.1 |
| compliance.scope | qwen27b-all | qwen27b | 100% | 100% | — | 2.9 |
| compliance.scope_entities | qwen27b-all | qwen27b | 100% | 100% | — | 4.0 |
| dvd.planner | qwen27b-all | qwen27b | 100% | 100% | — | 20.2 |
| norms.planner | qwen27b-all | qwen27b | 100% | 100% | — | 7.4 |
| norms.review | qwen27b-all | qwen27b | 93% | 96% | — | 5.5 |
| orchestrator.plan | qwen27b-all | qwen27b | 96% | 98% | — | 7.1 |
| project.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 2.4 |
| provision.plan | qwen27b-all | qwen27b | 100% | 100% | — | 6.6 |
| pzz.columns | qwen27b-all | qwen27b | 100% | 100% | — | 1.9 |
| pzz.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 1.8 |
| restriction.plan | qwen27b-all | qwen27b | 100% | 100% | — | 27.0 |
| scenario.candidates.assess | qwen27b-all | qwen27b | 100% | 100% | — | 20.6 |
| scenario.candidates.select | qwen27b-all | qwen27b | 100% | 100% | — | 1.0 |
| scenario.judge | qwen27b-all | qwen27b | 100% | 100% | — | 5.1 |
| scenario.request | qwen27b-all | qwen27b | 93% | 96% | — | 2.4 |
| scenario.select | qwen27b-all | qwen27b | 100% | 100% | — | 1.0 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chat | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 4.0/4.0 | 56/78 | 1.0 | — | 0 |
| chat_title | manual | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 13.0/15.6 | 533/224 | 1.0 | — | 0 |
| compliance.mapping | auto | qwen27b-all | qwen27b | 5 | 1 | 0 | 96% | — | 14.7/24.0 | 488/165 | 1.0 | — | 0 |
| compliance.mapping_reply | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 2.1/5.8 | 300/24 | 1.0 | — | 0 |
| compliance.scope | auto | qwen27b-all | qwen27b | 13 | 0 | 0 | 100% | — | 2.9/4.2 | 546/36 | 1.0 | — | 0 |
| compliance.scope_entities | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 4.0/6.6 | 459/54 | 1.0 | — | 0 |
| dvd.planner | auto | qwen27b-all | qwen27b | 19 | 0 | 0 | 100% | — | 20.2/26.7 | 1387/259 | 1.0 | — | 0 |
| norms.answer | manual | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 15.7/35.7 | 584/217 | 1.0 | — | 0 |
| norms.planner | auto | qwen27b-all | qwen27b | 16 | 0 | 0 | 100% | — | 7.4/8.2 | 752/101 | 1.0 | — | 0 |
| norms.review | auto | qwen27b-all | qwen27b | 14 | 1 | 0 | 96% | — | 5.5/7.6 | 804/79 | 1.0 | — | 0 |
| orchestrator.plan | auto | qwen27b-all | qwen27b | 50 | 2 | 0 | 98% | — | 7.1/13.2 | 3602/93 | 1.0 | — | 0 |
| project.inputs | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 2.4/3.0 | 267/37 | 1.0 | — | 0 |
| provision.plan | auto | qwen27b-all | qwen27b | 34 | 0 | 0 | 100% | — | 6.6/17.6 | 1100/58 | 1.0 | — | 0 |
| pzz.columns | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 1.9/4.0 | 172/22 | 1.0 | — | 0 |
| pzz.inputs | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 1.8/2.3 | 188/28 | 1.0 | — | 0 |
| restriction.explain | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 6.3/8.6 | 443/93 | 1.0 | — | 0 |
| restriction.plan | auto | qwen27b-all | qwen27b | 28 | 0 | 0 | 100% | — | 27.0/36.9 | 1462/435 | 1.0 | — | 0 |
| scenario.candidates.assess | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 20.6/35.9 | 275/249 | 1.0 | — | 0 |
| scenario.candidates.select | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 1.0/1.6 | 321/11 | 1.0 | — | 0 |
| scenario.judge | auto | qwen27b-all | qwen27b | 15 | 0 | 0 | 100% | — | 5.1/8.8 | 690/68 | 1.0 | — | 0 |
| scenario.request | auto | qwen27b-all | qwen27b | 13 | 1 | 0 | 96% | — | 2.4/4.5 | 230/28 | 1.0 | — | 0 |
| scenario.select | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 1.0/1.5 | 281/9 | 1.0 | — | 0 |
| scenario.summary | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 5.9/6.9 | 518/81 | 1.0 | — | 0 |

## Провалы и ошибки (5)

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
- **scenario.request / map_several_types_unsupported** · qwen27b-all #1 · fail
  - ✗ `operation eq`: ожидалось `unsupported`, получено `map`
