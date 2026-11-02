# Бенчмарк LLM-этапов gMART — 2026-11-02T15:10:25.630286+03:00

Профили: qwen27b-all · кейсов: 2 · повторов: 3 · датасет: gMART 68534ab3 от 2026-11-02T14:56:33

## Итог по профилям (автоматически оцениваемые этапы)

| Профиль | Прогонов | Pass rate | Средний балл этапов | Ошибок | Невалидных по схеме | Суммарное время, с |
|---|---|---|---|---|---|---|
| qwen27b-all | 6 | 33% | 33% | 4 | 0 | 1046 |

## Лучший профиль по этапам

| Этап | Профиль | Модель | Pass rate | Балл | Оценка (ручн.) | Латентность, с |
|---|---|---|---|---|---|---|
| restriction.plan | qwen27b-all | qwen27b | 33% | 33% | — | 174.3 |

## Матрица этап × профиль

| Этап | Тип | Профиль | Модель | Pass | Fail | Err | Балл | Стаб. | Лат. ср/p95, с | Токены вх/вых | Вызовов | Оценка | Повторы |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| restriction.plan | auto | qwen27b-all | qwen27b | 2 | 0 | 4 | 33% | 0% | 174.3/244.7 | 1674/2997 | 1.0 | — | 0 |

## Провалы и ошибки (4)

- **restriction.plan / normgraph_named_document_among_conflicting** · qwen27b-all #2 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
- **restriction.plan / normgraph_named_document_among_conflicting** · qwen27b-all #3 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
- **restriction.plan / repeated_norm_stays_normgraph** · qwen27b-all #1 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
- **restriction.plan / repeated_norm_stays_normgraph** · qwen27b-all #2 · error — `ValueError: invalid JSON: Expecting ',' delimiter`
