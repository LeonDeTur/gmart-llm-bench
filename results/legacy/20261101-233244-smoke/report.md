# Бенчмарк LLM-этапов gMART — 2026-11-01T23:32:44

Профили: qwen27b-all · кейсов: 20 · повторов: 1 · температура: 0.0

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Суммарное время, с |
|---|---|---|---|---|---|
| qwen27b-all | 19 | 84% | 84% | 1 | 118 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| compliance.mapping | qwen27b-all | qwen27b | 100% | 100% | — | 17.2 |
| compliance.scope | qwen27b-all | qwen27b | 100% | 100% | — | 2.4 |
| dvd.planner | qwen27b-all | qwen27b | 100% | 100% | — | 1.2 |
| norms.planner | qwen27b-all | qwen27b | 100% | 100% | — | 5.7 |
| norms.review | qwen27b-all | qwen27b | 100% | 100% | — | 2.4 |
| orchestrator.plan | qwen27b-all | qwen27b | 100% | 100% | — | 4.0 |
| project.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 3.1 |
| provision.plan | qwen27b-all | qwen27b | 100% | 100% | — | 3.3 |
| pzz.columns | qwen27b-all | qwen27b | 0% | 0% | — | 1.0 |
| pzz.inputs | qwen27b-all | qwen27b | 0% | 67% | — | 2.0 |
| restriction.plan | qwen27b-all | qwen27b | 100% | 100% | — | 22.4 |
| scenario.candidates | qwen27b-all | qwen27b | 0% | 0% | — | 0.0 |
| scenario.judge | qwen27b-all | qwen27b | 100% | 100% | — | 4.4 |
| scenario.request | qwen27b-all | qwen27b | 100% | 100% | — | 1.1 |
| scenario.select | qwen27b-all | qwen27b | 100% | 100% | — | 0.7 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| compliance.mapping | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 17.2/17.2 | 613/348 | 1.0 | — |
| compliance.scope | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 2.4/2.4 | 546/50 | 1.0 | — |
| dvd.planner | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 1.2/1.2 | 1374/15 | 1.0 | — |
| norms.answer | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 13.3/13.3 | 0/0 | 1.0 | — |
| norms.planner | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 5.7/5.7 | 735/95 | 1.0 | — |
| norms.review | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 2.4/2.4 | 898/33 | 1.0 | — |
| orchestrator.plan | auto | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 4.0/4.4 | 3638/74 | 1.0 | — |
| project.inputs | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 3.1/3.1 | 284/42 | 1.0 | — |
| provision.plan | auto | qwen27b-all | qwen27b | 2 | 0 | 0 | 100% | — | 3.3/3.6 | 1090/52 | 1.0 | — |
| pzz.columns | auto | qwen27b-all | qwen27b | 0 | 1 | 0 | 0% | — | 1.0/1.0 | 128/20 | 1.0 | — |
| pzz.inputs | auto | qwen27b-all | qwen27b | 0 | 1 | 0 | 67% | — | 2.0/2.0 | 118/35 | 1.0 | — |
| restriction.plan | auto | qwen27b-all | qwen27b | 2 | 0 | 0 | 100% | — | 22.4/27.3 | 1449/427 | 1.0 | — |
| scenario.candidates | auto | qwen27b-all | qwen27b | 0 | 0 | 1 | 0% | — | 0.0/0.0 | 0/0 | 1.0 | — |
| scenario.judge | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 4.4/4.4 | 427/68 | 1.0 | — |
| scenario.request | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 1.1/1.1 | 227/22 | 1.0 | — |
| scenario.select | auto | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 0.7/0.7 | 284/13 | 1.0 | — |

## Провалы и ошибки (3)

- **pzz.columns / vri_column_by_values** · qwen27b-all #1 · fail
  - ✗ `columns.cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #1 · fail
  - ✗ `mode eq`: ожидалось `scenario`, получено `building_pzz_check`
- **scenario.candidates / pick_exact_meaning_only** · qwen27b-all #1 · error — `LlmResponseError: Error code: 400 - {'error': {'message': 'No user query found in messages.', 'type': 'BadRequestError', 'param': None, 'code': 400}}`
