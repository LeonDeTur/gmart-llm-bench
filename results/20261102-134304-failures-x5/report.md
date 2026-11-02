# Бенчмарк LLM-этапов gMART — 2026-11-02T13:43:04.317283+03:00

Профили: qwen27b-all · кейсов: 4 · повторов: 5 · датасет: gMART 0433b245 от 2026-11-02T02:17:42

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| qwen27b-all | 20 | 0% | 42% | 0 | 0 | 51 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| provision.plan | qwen27b-all | qwen27b | 0% | 50% | — | 2.9 |
| pzz.columns | qwen27b-all | qwen27b | 0% | 0% | — | 1.2 |
| pzz.inputs | qwen27b-all | qwen27b | 0% | 67% | — | 2.1 |
| scenario.judge | qwen27b-all | qwen27b | 0% | 50% | — | 3.9 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| provision.plan | auto | qwen27b-all | qwen27b | 0 | 5 | 0 | 50% | 100% | 2.9/3.4 | 1092/42 | 1.0 | — | 0 |
| pzz.columns | auto | qwen27b-all | qwen27b | 0 | 5 | 0 | 0% | 100% | 1.2/1.8 | 128/20 | 1.0 | — | 0 |
| pzz.inputs | auto | qwen27b-all | qwen27b | 0 | 5 | 0 | 67% | 100% | 2.1/2.8 | 118/35 | 1.0 | — | 0 |
| scenario.judge | auto | qwen27b-all | qwen27b | 0 | 5 | 0 | 50% | 100% | 3.9/4.4 | 414/73 | 1.0 | — | 0 |

## Провалы и ошибки (20)

- **provision.plan / ambiguous_single_service_defaults_to_effects** · qwen27b-all #1 · fail
  - ✗ `mode eq`: ожидалось `effects`, получено `provision`
- **provision.plan / ambiguous_single_service_defaults_to_effects** · qwen27b-all #2 · fail
  - ✗ `mode eq`: ожидалось `effects`, получено `provision`
- **provision.plan / ambiguous_single_service_defaults_to_effects** · qwen27b-all #3 · fail
  - ✗ `mode eq`: ожидалось `effects`, получено `provision`
- **provision.plan / ambiguous_single_service_defaults_to_effects** · qwen27b-all #4 · fail
  - ✗ `mode eq`: ожидалось `effects`, получено `provision`
- **provision.plan / ambiguous_single_service_defaults_to_effects** · qwen27b-all #5 · fail
  - ✗ `mode eq`: ожидалось `effects`, получено `provision`
- **pzz.columns / vri_column_by_values** · qwen27b-all #1 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.columns / vri_column_by_values** · qwen27b-all #2 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.columns / vri_column_by_values** · qwen27b-all #3 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.columns / vri_column_by_values** · qwen27b-all #4 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.columns / vri_column_by_values** · qwen27b-all #5 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #1 · fail
  - ✗ `mode eq`: ожидалось `scenario`, получено `building_pzz_check`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #2 · fail
  - ✗ `mode eq`: ожидалось `scenario`, получено `building_pzz_check`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #3 · fail
  - ✗ `mode eq`: ожидалось `scenario`, получено `building_pzz_check`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #4 · fail
  - ✗ `mode eq`: ожидалось `scenario`, получено `building_pzz_check`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #5 · fail
  - ✗ `mode eq`: ожидалось `scenario`, получено `building_pzz_check`
- **scenario.judge / counts_ignored_insufficient** · qwen27b-all #1 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
- **scenario.judge / counts_ignored_insufficient** · qwen27b-all #2 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
- **scenario.judge / counts_ignored_insufficient** · qwen27b-all #3 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
- **scenario.judge / counts_ignored_insufficient** · qwen27b-all #4 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
- **scenario.judge / counts_ignored_insufficient** · qwen27b-all #5 · fail
  - ✗ `missing_code in`: ожидалось `["counts_missing", "answer_incomplete"]`, получено `none`
