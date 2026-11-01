# Бенчмарк LLM-этапов gMART — 2026-11-02T02:20:24.270851+03:00

Профили: qwen27b-all · кейсов: 116 · повторов: 1 · датасет: gMART 0433b245 от 2026-11-02T02:17:42

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| qwen27b-all | 108 | 95% | 95% | 0 | 0 | 840 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| compliance.mapping | qwen27b-all | qwen27b | 100% | 100% | — | 11.9 |
| compliance.mapping_reply | qwen27b-all | qwen27b | 100% | 100% | — | 1.0 |
| compliance.scope | qwen27b-all | qwen27b | 100% | 100% | — | 2.4 |
| compliance.scope_entities | qwen27b-all | qwen27b | 100% | 100% | — | 4.1 |
| dvd.planner | qwen27b-all | qwen27b | 100% | 100% | — | 14.2 |
| norms.planner | qwen27b-all | qwen27b | 100% | 100% | — | 9.5 |
| norms.review | qwen27b-all | qwen27b | 100% | 100% | — | 6.0 |
| orchestrator.plan | qwen27b-all | qwen27b | 100% | 100% | — | 5.1 |
| project.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 2.2 |
| provision.plan | qwen27b-all | qwen27b | 93% | 96% | — | 4.0 |
| pzz.columns | qwen27b-all | qwen27b | 67% | 67% | — | 3.3 |
| pzz.inputs | qwen27b-all | qwen27b | 75% | 92% | — | 2.0 |
| restriction.plan | qwen27b-all | qwen27b | 100% | 100% | — | 29.0 |
| scenario.candidates.assess | qwen27b-all | qwen27b | 100% | 100% | — | 11.6 |
| scenario.candidates.select | qwen27b-all | qwen27b | 67% | 67% | — | 0.7 |
| scenario.judge | qwen27b-all | qwen27b | 75% | 88% | — | 5.2 |
| scenario.request | qwen27b-all | qwen27b | 100% | 100% | — | 1.9 |
| scenario.select | qwen27b-all | qwen27b | 100% | 100% | — | 0.6 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chat | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 4.6/4.6 | 56/70 | 1.0 | — | 0 |
| chat_title | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 38.3/38.3 | 530/610 | 1.0 | — | 0 |
| compliance.mapping | auto | qwen27b-all | qwen27b | 2 | 0 | 0 | 100% | — | 11.9/19.5 | 522/208 | 1.0 | — | 0 |
| compliance.mapping_reply | auto | qwen27b-all | qwen27b | 5 | 0 | 0 | 100% | — | 1.0/1.9 | 301/18 | 1.0 | — | 0 |
| compliance.scope | auto | qwen27b-all | qwen27b | 6 | 0 | 0 | 100% | — | 2.4/3.6 | 544/32 | 1.0 | — | 0 |
| compliance.scope_entities | auto | qwen27b-all | qwen27b | 2 | 0 | 0 | 100% | — | 4.1/4.4 | 470/37 | 1.0 | — | 0 |
| dvd.planner | auto | qwen27b-all | qwen27b | 5 | 0 | 0 | 100% | — | 14.2/18.9 | 1382/259 | 1.0 | — | 0 |
| norms.answer | manual | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 12.2/23.5 | 576/206 | 1.0 | — | 0 |
| norms.planner | auto | qwen27b-all | qwen27b | 6 | 0 | 0 | 100% | — | 9.5/14.4 | 744/101 | 1.0 | — | 0 |
| norms.review | auto | qwen27b-all | qwen27b | 5 | 0 | 0 | 100% | — | 6.0/8.8 | 835/74 | 1.0 | — | 0 |
| orchestrator.plan | auto | qwen27b-all | qwen27b | 23 | 0 | 0 | 100% | — | 5.1/8.9 | 3603/80 | 1.0 | — | 0 |
| project.inputs | auto | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 2.2/3.0 | 265/37 | 1.0 | — | 0 |
| provision.plan | auto | qwen27b-all | qwen27b | 13 | 1 | 0 | 96% | — | 4.0/6.0 | 1098/57 | 1.0 | — | 0 |
| pzz.columns | auto | qwen27b-all | qwen27b | 2 | 1 | 0 | 67% | — | 3.3/5.2 | 104/25 | 1.0 | — | 0 |
| pzz.inputs | auto | qwen27b-all | qwen27b | 3 | 1 | 0 | 92% | — | 2.0/2.3 | 116/30 | 1.0 | — | 0 |
| restriction.explain | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 2.1/2.1 | 440/41 | 1.0 | — | 0 |
| restriction.plan | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 29.0/42.8 | 1481/491 | 1.0 | — | 0 |
| scenario.candidates.assess | auto | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 11.6/15.9 | 251/200 | 1.0 | — | 0 |
| scenario.candidates.select | auto | qwen27b-all | qwen27b | 2 | 1 | 0 | 67% | — | 0.7/1.1 | 297/9 | 1.0 | — | 0 |
| scenario.judge | auto | qwen27b-all | qwen27b | 3 | 1 | 0 | 88% | — | 5.2/5.5 | 404/70 | 1.0 | — | 0 |
| scenario.request | auto | qwen27b-all | qwen27b | 6 | 0 | 0 | 100% | — | 1.9/2.6 | 229/26 | 1.0 | — | 0 |
| scenario.select | auto | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 0.6/1.1 | 285/9 | 1.0 | — | 0 |
| scenario.summary | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 3.3/3.3 | 517/67 | 1.0 | — | 0 |

## Провалы и ошибки (5)

- **provision.plan / ambiguous_single_service_defaults_to_effects** · qwen27b-all #1 · fail
  - ✗ `mode eq`: ожидалось `effects`, получено `provision`
- **pzz.columns / vri_column_by_values** · qwen27b-all #1 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #1 · fail
  - ✗ `mode eq`: ожидалось `scenario`, получено `building_pzz_check`
- **scenario.candidates.select / nothing_matches** · qwen27b-all #1 · fail
  - ✗ `candidate_ids len`: ожидалось `0`, получено `null`
- **scenario.judge / counts_ignored_insufficient** · qwen27b-all #1 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
