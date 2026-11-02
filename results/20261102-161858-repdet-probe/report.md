# Бенчмарк LLM-этапов gMART — 2026-11-02T16:18:58.102032+03:00

Профили: base, repdet · кейсов: 28 · повторов: 1 · датасет: gMART 68534ab3 от 2026-11-02T14:56:33

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| base | 28 | 93% | 93% | 2 | 0 | 982 |
| repdet | 28 | 89% | 89% | 3 | 0 | 651 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| restriction.plan | base | base | 93% | 93% | — | 35.1 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| restriction.plan | auto | base | base | 26 | 0 | 2 | 93% | — | 35.1/188.5 | 1494/710 | 1.0 | — | 0 |
| restriction.plan | auto | repdet | repdet | 25 | 0 | 3 | 89% | — | 23.3/34.0 | 1494/428 | 1.0 | — | 0 |

## Провалы и ошибки (5)

- **restriction.plan / normgraph_named_document_among_conflicting** · base #1 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
- **restriction.plan / normgraph_named_document_among_conflicting** · repdet #1 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
- **restriction.plan / normgraph_rule_grounded** · repdet #1 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
- **restriction.plan / repeated_norm_stays_normgraph** · base #1 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
- **restriction.plan / repeated_norm_stays_normgraph** · repdet #1 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
