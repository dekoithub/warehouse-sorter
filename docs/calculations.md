# Performance Calculations

## Overview

Этот документ содержит расчёты производительности simulation layer проекта Warehouse Sorter.

Основная цель нагрузочного сценария:

```text
≈ 100,000 items/hour
```

при:

```text
400 sorting destinations
```

Расчёты использовались для последовательного определения bottleneck'ов и выбора конфигурации Scanner, Conveyor, Sorter и OutputBin.

---

## Target Throughput

Целевая производительность:

```text
100,000 items/hour
```

Переведём её в товары в секунду:

```text
100,000 / 3,600
≈ 27.78 items/second
```

Следовательно, средний интервал между поступлениями товаров:

```text
1 / 27.78
≈ 0.036 seconds/item
```

Поэтому в simulation config используется:

```python
item_interval_seconds=0.036
```

Теоретический поток:

```text
3,600 / 0.036
= 100,000 items/hour
```

---

## Observed Arrival Rate

В тесте продолжительностью:

```text
600 seconds
```

было создано:

```text
16,667 items
```

Фактический arrival rate:

```text
16,667 / 600
≈ 27.7783 items/second
```

Перевод в час:

```text
27.7783 × 3,600
≈ 100,002 items/hour
```

Полученный результат:

```text
arrival_rate_items_per_hour = 100,002
```

Практически полностью соответствует целевой нагрузке.

---

## Scanner Capacity

### Initial Configuration

Изначально использовалось:

```python
scan_duration_seconds=0.1
scanner_capacity=1
```

Один scanning channel способен обработать:

```text
1 / 0.1
= 10 items/second
```

или:

```text
10 × 3,600
= 36,000 items/hour
```

Это существенно меньше целевого потока:

```text
36,000 < 100,000
```

Поэтому Scanner стал первым bottleneck.

---

## Required Scanner Capacity

Для входного потока:

```text
27.78 items/second
```

при длительности сканирования:

```text
0.1 seconds
```

необходимое количество параллельных каналов:

```text
27.78 × 0.1
≈ 2.778
```

Количество channels должно быть целым числом, поэтому минимально:

```text
ceil(2.778) = 3
```

Используем:

```python
scanner_capacity=3
```

Теоретическая производительность:

```text
3 / 0.1
= 30 items/second
```

или:

```text
30 × 3,600
= 108,000 items/hour
```

Запас относительно цели:

```text
108,000 - 100,000
= 8,000 items/hour
```

---

## Conveyor Travel Time

Параметры Conveyor:

```python
conveyor_length_meters=10.0
conveyor_speed_mps=2.0
```

Время прохождения одного товара:

```text
travel_time = length / speed
```

```text
10 / 2
= 5 seconds
```

То есть каждый товар занимает место на Conveyor примерно:

```text
5 seconds
```

---

## Required Conveyor Capacity

При входном потоке:

```text
27.78 items/second
```

и времени транспортировки:

```text
5 seconds
```

количество товаров, одновременно находящихся на Conveyor:

```text
27.78 × 5
≈ 138.9
```

Минимальная теоретическая capacity:

```text
≈ 139 items
```

Для небольшого запаса используется:

```python
conveyor_capacity=150
```

---

## Conveyor Theoretical Throughput

При capacity:

```text
150 items
```

и travel time:

```text
5 seconds
```

теоретическая производительность:

```text
150 / 5
= 30 items/second
```

или:

```text
30 × 3,600
= 108,000 items/hour
```

Это выше требуемых:

```text
100,000 items/hour
```

---

## Initial Conveyor Bottleneck

До масштабирования использовалось:

```python
conveyor_capacity=10
```

При travel time:

```text
5 seconds
```

максимальный теоретический throughput:

```text
10 / 5
= 2 items/second
```

или:

```text
2 × 3,600
= 7,200 items/hour
```

Simulation показала около:

```text
6,600 sorted items/hour
```

что соответствует ожидаемому ограничению с учётом startup-периода.

---

## Sorter Capacity

Параметр:

```python
sorter_duration_seconds=0.1
```

Один sorting channel способен обработать:

```text
1 / 0.1
= 10 items/second
```

или:

```text
36,000 items/hour
```

Это ниже целевых:

```text
100,000 items/hour
```

Поэтому при `sorter_capacity=1` Sorter становится bottleneck.

---

## Required Sorter Capacity

Для потока:

```text
27.78 items/second
```

при:

```text
0.1 seconds/item
```

необходимая capacity:

```text
27.78 × 0.1
≈ 2.778
```

Округляем вверх:

```text
3 sorting channels
```

Используем:

```python
sorter_capacity=3
```

Теоретический throughput:

```text
3 / 0.1
= 30 items/second
```

или:

```text
108,000 items/hour
```

---

## OutputBin Capacity

В simulation OutputBin хранит уже отсортированные товары.

При тесте длительностью:

```text
600 seconds
```

и потоке около:

```text
100,000 items/hour
```

ожидаемое количество обработанных товаров:

```text
100,000 × 600 / 3,600
≈ 16,667 items
```

При одном общем направлении capacity должна была бы быть больше этого значения.

Для high-load scenario используется:

```python
output_bin_capacity=20000
```

После перехода к:

```python
destination_count=400
```

нагрузка распределяется между сотнями OutputBin.

---

## 400 Destination Distribution

В итоговом тесте было отсортировано:

```text
16,523 items
```

Количество destinations:

```text
400
```

Средняя загрузка одного OutputBin:

```text
16,523 / 400
= 41.3075 items
```

Фактическое распределение:

```text
Destinations 1–123   → 42 items
Destinations 124–400 → 41 items
```

Проверка:

```text
123 × 42 = 5,166
277 × 41 = 11,357
```

Сумма:

```text
5,166 + 11,357
= 16,523
```

Распределение полностью соответствует количеству отсортированных товаров.

---

## Simulation Startup Time

Полный минимальный путь товара включает:

```text
Scanner
+
Conveyor
+
Sorter
```

При текущей конфигурации:

```text
Scanner = 0.1 s
Conveyor = 5.0 s
Sorter = 0.1 s
```

Минимальное время прохождения:

```text
0.1 + 5.0 + 0.1
= 5.2 seconds
```

Поэтому в начале simulation некоторое время ещё нет готовых `SORTED` items.

Это влияет на средний throughput коротких тестов.

---

## 60-Second Test

При simulation duration:

```text
60 seconds
```

было получено:

```text
Generated: 1,667
Sorted:    1,523
In-flight:   144
```

Arrival rate:

```text
100,020 items/hour
```

Measured sorted throughput:

```text
91,380 items/hour
```

Разница возникает главным образом из-за startup time.

К моменту остановки simulation:

```text
144 items
```

ещё находились внутри pipeline.

---

## 600-Second Sustained Test

Чтобы уменьшить влияние startup time, simulation duration была увеличена до:

```text
600 seconds
```

Результат:

```text
Generated: 16,667
Sorted:    16,523
In-flight:    144
```

Arrival rate:

```text
100,002 items/hour
```

Sorted throughput:

```text
99,138 items/hour
```

---

## In-Flight Validation

В конце sustained test:

```text
scanner_in_use = 3
conveyor_in_use = 138
sorter_in_use = 3
```

Сумма:

```text
3 + 138 + 3
= 144
```

Отчёт:

```text
in_flight_items = 144
```

Следовательно, все незавершённые товары находятся внутри известного processing pipeline.

Потерянных товаров нет.

---

## Item Accounting

Для итогового теста:

```text
Generated = 16,667
Sorted = 16,523
In-flight = 144
Manual Processing = 0
```

Проверка:

```text
16,523 + 144
= 16,667
```

То есть:

```text
Generated
=
Sorted
+
In-flight
```

Все товары учтены.

---

## Success Rate

Формула текущего показателя:

```text
success_rate =
sorted_items / processed_items × 100
```

Для итогового теста:

```text
16,523 / 16,667 × 100
≈ 99.136%
```

Важно:

оставшиеся примерно:

```text
0.864%
```

не являются ошибками.

Это товары, которые находились внутри pipeline в момент окончания simulation.

---

## Sustained Throughput Interpretation

Measured throughput за полное 600-секундное окно:

```text
99,138 items/hour
```

Он немного ниже target arrival rate:

```text
100,002 items/hour
```

из-за начального заполнения pipeline.

При установившемся режиме система работает примерно на уровне входного потока:

```text
≈ 100,000 items/hour
```

без накопления очередей.

---

## Queue Validation

Итоговый sustained test:

```text
scanner_current_queue = 0
conveyor_current_queue = 0
sorter_current_queue = 0
buffer_current_load = 0
```

Это означает, что при целевой нагрузке система находится в стабильном режиме:

```text
arrival rate
≈
processing capacity
```

и backlog не растёт.

---

## Bottleneck Progression

Во время разработки нагрузочной модели bottleneck'и обнаруживались последовательно.

### Stage 1

```text
Scanner capacity = 1
```

Результат:

```text
Scanner queue > 1,000 items
```

Scanner не справлялся с входным потоком.

---

### Stage 2

После:

```python
scanner_capacity=3
```

Scanner queue исчезла.

Следующий bottleneck:

```text
Conveyor
```

---

### Stage 3

При:

```python
conveyor_capacity=10
```

теоретическая производительность была:

```text
≈ 7,200 items/hour
```

Buffer начал переполняться, товары уходили в Manual Processing.

---

### Stage 4

После:

```python
conveyor_capacity=150
```

ограничение Conveyor исчезло.

Следующий bottleneck:

```text
Sorter
```

---

### Stage 5

При:

```python
sorter_capacity=1
```

Sorter мог обработать только:

```text
≈ 36,000 items/hour
```

очередь перед Sorter быстро росла.

---

### Stage 6

После:

```python
sorter_capacity=3
```

Sorter queue практически исчезла.

Следующим ограничением стала capacity OutputBin.

---

### Stage 7

После увеличения:

```python
output_bin_capacity=20000
```

и распределения по:

```python
destination_count=400
```

система вышла на стабильную работу без очередей.

---

## Final High-Load Configuration

```python
SimulationConfig(
    duration_seconds=600.0,
    item_interval_seconds=0.036,
    scan_duration_seconds=0.1,
    scanner_capacity=3,
    conveyor_length_meters=10.0,
    conveyor_speed_mps=2.0,
    conveyor_capacity=150,
    buffer_capacity=100,
    buffer_retry_interval_seconds=0.05,
    default_destination=1,
    destination_count=400,
    sorter_duration_seconds=0.1,
    sorter_capacity=3,
    output_bin_capacity=20000,
    scanner_error_rate=0.0,
)
```

---

## Final Performance Result

```text
Simulation time:                  600 seconds

Generated items:                 16,667
Sorted items:                    16,523
In-flight items:                    144

Arrival rate:                   100,002 items/hour
Sorted throughput:               99,138 items/hour

Scanner queue:                        0
Conveyor queue:                       0
Sorter queue:                         0
Buffer load:                          0

Manual Processing:                    0
Scan errors:                          0
Routing errors:                       0

Sorting destinations:               400
```

---

## Conclusion

Расчёты и simulation подтверждают, что выбранная конфигурация оборудования способна моделировать стабильную работу сортировочного центра при нагрузке порядка:

```text
100,000 items/hour
```

с:

```text
400 sorting destinations
```

без роста очередей и без переполнения Buffer при штатном сценарии.

Ключевая рассчитанная capacity:

```text
Scanner:  3 parallel channels
Conveyor: 150 simultaneous items
Sorter:   3 parallel channels
Output:   400 destinations
```

Нагрузочные параметры были получены не случайным подбором, а через последовательный расчёт и проверку bottleneck'ов в SimPy.
````