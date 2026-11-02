# Бенчмарк LLM-этапов gMART — 2026-11-02T14:01:10.245541+03:00

Профили: qwen27b-all · кейсов: 300 · повторов: 1 · датасет: gMART 68534ab3 от 2026-11-02T14:00:59

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| qwen27b-all | 280 | 92% | 92% | 0 | 0 | 2444 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| chat | qwen27b-all | qwen27b | 100% | 100% | 1.00 | 7.1 |
| chat_title | qwen27b-all | qwen27b | 100% | 100% | 1.75 | 18.3 |
| compliance.mapping | qwen27b-all | qwen27b | 83% | 94% | — | 9.0 |
| compliance.mapping_reply | qwen27b-all | qwen27b | 100% | 100% | — | 1.7 |
| compliance.scope | qwen27b-all | qwen27b | 100% | 100% | — | 2.8 |
| compliance.scope_entities | qwen27b-all | qwen27b | 86% | 93% | — | 3.8 |
| dvd.planner | qwen27b-all | qwen27b | 95% | 97% | — | 16.2 |
| norms.answer | qwen27b-all | qwen27b | 89% | 94% | 1.67 | 13.6 |
| norms.planner | qwen27b-all | qwen27b | 100% | 100% | — | 6.4 |
| norms.review | qwen27b-all | qwen27b | 93% | 93% | — | 5.2 |
| orchestrator.plan | qwen27b-all | qwen27b | 96% | 96% | — | 5.7 |
| project.inputs | qwen27b-all | qwen27b | 100% | 100% | — | 2.7 |
| provision.plan | qwen27b-all | qwen27b | 100% | 100% | — | 4.6 |
| pzz.columns | qwen27b-all | qwen27b | 33% | 41% | — | 1.4 |
| pzz.inputs | qwen27b-all | qwen27b | 70% | 88% | — | 2.5 |
| restriction.explain | qwen27b-all | qwen27b | 100% | 100% | 2.00 | 5.8 |
| restriction.plan | qwen27b-all | qwen27b | 100% | 100% | — | 31.2 |
| scenario.candidates.assess | qwen27b-all | qwen27b | 100% | 100% | — | 13.4 |
| scenario.candidates.select | qwen27b-all | qwen27b | 100% | 100% | — | 0.8 |
| scenario.judge | qwen27b-all | qwen27b | 67% | 80% | — | 4.3 |
| scenario.request | qwen27b-all | qwen27b | 93% | 93% | — | 1.8 |
| scenario.select | qwen27b-all | qwen27b | 78% | 78% | — | 0.8 |
| scenario.summary | qwen27b-all | qwen27b | 67% | 89% | 1.67 | 5.5 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| chat | manual | qwen27b-all | qwen27b | 1 | 0 | 0 | 100% | — | 7.1/7.1 | 56/84 | 1.0 | 1.00 (1) | 0 |
| chat_title | manual | qwen27b-all | qwen27b | 4 | 0 | 0 | 100% | — | 18.3/36.5 | 533/288 | 1.0 | 1.75 (4) | 0 |
| compliance.mapping | auto | qwen27b-all | qwen27b | 5 | 1 | 0 | 94% | — | 9.0/18.8 | 488/166 | 1.0 | — | 0 |
| compliance.mapping_reply | auto | qwen27b-all | qwen27b | 10 | 0 | 0 | 100% | — | 1.7/5.3 | 300/24 | 1.0 | — | 0 |
| compliance.scope | auto | qwen27b-all | qwen27b | 13 | 0 | 0 | 100% | — | 2.8/3.7 | 546/36 | 1.0 | — | 0 |
| compliance.scope_entities | auto | qwen27b-all | qwen27b | 6 | 1 | 0 | 93% | — | 3.8/6.4 | 459/54 | 1.0 | — | 0 |
| dvd.planner | auto | qwen27b-all | qwen27b | 18 | 1 | 0 | 97% | — | 16.2/22.8 | 1387/260 | 1.0 | — | 0 |
| norms.answer | manual | qwen27b-all | qwen27b | 8 | 1 | 0 | 94% | — | 13.6/26.3 | 584/208 | 1.0 | 1.67 (9) | 0 |
| norms.planner | auto | qwen27b-all | qwen27b | 16 | 0 | 0 | 100% | — | 6.4/7.9 | 752/101 | 1.0 | — | 0 |
| norms.review | auto | qwen27b-all | qwen27b | 14 | 1 | 0 | 93% | — | 5.2/8.1 | 804/78 | 1.0 | — | 0 |
| orchestrator.plan | auto | qwen27b-all | qwen27b | 50 | 2 | 0 | 96% | — | 5.7/10.0 | 3602/92 | 1.0 | — | 0 |
| project.inputs | auto | qwen27b-all | qwen27b | 9 | 0 | 0 | 100% | — | 2.7/4.4 | 267/37 | 1.0 | — | 0 |
| provision.plan | auto | qwen27b-all | qwen27b | 34 | 0 | 0 | 100% | — | 4.6/6.9 | 1100/59 | 1.0 | — | 0 |
| pzz.columns | auto | qwen27b-all | qwen27b | 3 | 6 | 0 | 41% | — | 1.4/2.9 | 110/25 | 1.0 | — | 0 |
| pzz.inputs | auto | qwen27b-all | qwen27b | 7 | 3 | 0 | 88% | — | 2.5/3.9 | 118/28 | 1.0 | — | 0 |
| restriction.explain | manual | qwen27b-all | qwen27b | 3 | 0 | 0 | 100% | — | 5.8/8.2 | 443/97 | 1.0 | 2.00 (3) | 0 |
| restriction.plan | auto | qwen27b-all | qwen27b | 28 | 0 | 0 | 100% | — | 31.2/55.5 | 1494/474 | 1.0 | — | 0 |
| scenario.candidates.assess | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 13.4/19.9 | 275/254 | 1.0 | — | 0 |
| scenario.candidates.select | auto | qwen27b-all | qwen27b | 7 | 0 | 0 | 100% | — | 0.8/1.2 | 321/10 | 1.0 | — | 0 |
| scenario.judge | auto | qwen27b-all | qwen27b | 10 | 5 | 0 | 80% | — | 4.3/5.8 | 400/69 | 1.0 | — | 0 |
| scenario.request | auto | qwen27b-all | qwen27b | 13 | 1 | 0 | 93% | — | 1.8/3.5 | 230/28 | 1.0 | — | 0 |
| scenario.select | auto | qwen27b-all | qwen27b | 7 | 2 | 0 | 78% | — | 0.8/1.2 | 281/9 | 1.0 | — | 0 |
| scenario.summary | manual | qwen27b-all | qwen27b | 2 | 1 | 0 | 89% | — | 5.5/6.2 | 518/87 | 1.0 | 1.67 (3) | 0 |

## Провалы и ошибки (25)

- **compliance.mapping / clear_school_high_confidence** · qwen27b-all #1 · fail
  - ✗ `items[id=2].entity ne`: ожидалось `Жилой дом`, получено `Жилой дом`
- **compliance.scope_entities / layer_text_listing** · qwen27b-all #1 · fail
  - ✗ `selections[topic=поликлиника].entities contains`: ожидалось `["поликлиника", "амбулаторно-поликлиническое учреждение", "медицинских организаций"]`, получено `["поликлиника", "амбулаторно-поликлиническое учреждение"]`
- **dvd.planner / table_requested** · qwen27b-all #1 · fail
  - ✗ `types null`: ожидалось `true`, получено `["table"]`
- **norms.answer / abbreviation_not_expanded** · qwen27b-all #1 · fail
  - ✗ `text not_contains`: ожидалось `["санитарно-защитн"]`, получено `Размещение жилых домов в санитарно-защитной зоне (СЗЗ) запрещено.  *   **Значение:** Размещение жилой застройки в границах СЗЗ не допускается. *   **Условие пр…`
- **norms.review / insufficient_context_needs_refinement** · qwen27b-all #1 · fail
  - ✗ `satisfied eq`: ожидалось `false`, получено `true`
  - ✗ `refined_search_query null`: ожидалось `false`, получено `null`
- **orchestrator.plan / check_with_evidence_single_step** · qwen27b-all #1 · fail
  - ✗ `steps[*].agent eq`: ожидалось `["compliance"]`, получено `["compliance", "documents"]`
- **orchestrator.plan / pzz_building_files_mode** · qwen27b-all #1 · fail
  - ✗ `steps[*].agent eq`: ожидалось `["pzz"]`, получено `[]`
  - ✗ `steps.0.task contains`: ожидалось `["здани"]`, получено `null`
- **pzz.columns / code_vs_text_vri** · qwen27b-all #1 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `vri_desc`, получено `vri_code`
- **pzz.columns / russian_headers** · qwen27b-all #1 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `Разрешенное_использование`, получено `Кадастровый_номер`
- **pzz.columns / three_targets_one_layer** · qwen27b-all #1 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `purpose`, получено `cad_num`
- **pzz.columns / vri_column_by_values** · qwen27b-all #1 · fail
  - ✗ `cadastral_vri_col eq`: ожидалось `VRI_text`, получено `KN`
- **pzz.columns / zone_description_only** · qwen27b-all #1 · fail
  - ✗ `pzz_zone_name_col eq`: ожидалось `opisanie`, получено `zona`
- **pzz.columns / zone_short_label** · qwen27b-all #1 · fail
  - ✗ `pzz_zone_code_col eq`: ожидалось `zone_label`, получено `id_zone`
- **pzz.inputs / scenario_mode_with_year_and_source** · qwen27b-all #1 · fail
  - ✗ `mode not_in`: ожидалось `["pzz_check", "classify_only", "building_pzz_check"]`, получено `building_pzz_check`
- **pzz.inputs / source_without_year** · qwen27b-all #1 · fail
  - ✗ `source eq`: ожидалось `OSM`, получено `null`
- **pzz.inputs / user_zones_with_year** · qwen27b-all #1 · fail
  - ✗ `source eq`: ожидалось `User`, получено `null`
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
- **scenario.select / children_clinic_absent** · qwen27b-all #1 · fail
  - ✗ `candidate null`: ожидалось `true`, получено `s3`
- **scenario.select / narrower_type_not_generalised** · qwen27b-all #1 · fail
  - ✗ `candidate null`: ожидалось `true`, получено `p1`
- **scenario.summary / summary_nothing_changed** · qwen27b-all #1 · fail
  - ✗ `text contains_any`: ожидалось `["не измен", "без изменений", "одинаков", "совпада"]`, получено `Между базовым сценарием и вариантом 3 не зафиксировано изменений ни по одному из трех показателей. Обеспеченность школами, плотность населения и озелененность …`
