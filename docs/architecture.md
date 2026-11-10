# Architecture

## Overview

Warehouse Sorter построен как многослойное backend-приложение с отдельным слоем дискретно-событийной симуляции.

Основная задача архитектуры — отделить бизнес-логику сортировочного центра от HTTP API, базы данных и механизма симуляции.

Основные слои:

- API;
- Application;
- Services;
- Domain Models;
- Infrastructure;
- Simulation.

---

## High-Level Architecture

Основной backend-поток:

```text
Client
  ↓
FastAPI
  ↓
Application Layer
  ↓
Controller / Use Cases
  ↓
Services
  ↓
Domain Models
  ↓
Infrastructure
  ↓
PostgreSQL
```

Слой симуляции использует ту же доменную и application-логику:

```text
SimPy Environment
      ↓
ItemGenerator
      ↓
ScannerStation
      ↓
Controller / Services
      ↓
ConveyorStation
      ↓
SorterStation
      ↓
OutputBin
```

Таким образом, SimPy не создаёт отдельную бизнес-логику сортировочного центра, а моделирует работу уже существующих компонентов во времени.

---

## Domain Layer

Domain Layer содержит основные сущности сортировочного центра.

Основные модели:

- `Item`
- `Scanner`
- `Conveyor`
- `Buffer`
- `Sensor`
- `Sorter`
- `OutputBin`
- `WMS`
- `Statistics`

Domain-модели отвечают за:

- состояние объектов;
- бизнес-правила;
- валидацию;
- изменение состояния оборудования;
- изменение статуса товара.

Domain Layer не должен напрямую зависеть от:

- FastAPI;
- HTTP;
- PostgreSQL;
- SQLAlchemy;
- SimPy.

---

## Item

`Item` представляет товар, проходящий через сортировочный центр.

Основные данные:

- ID;
- barcode;
- weight;
- dimensions;
- category;
- delivery type;
- flammability;
- status;
- destination;
- current location.

Статус товара изменяется на протяжении всего processing pipeline.

---

## Item Lifecycle

Основной жизненный цикл:

```text
CREATED
   ↓
SCANNING
   ↓
ROUTING
   ↓
MOVING
   ↓
SORTED
```

При временной перегрузке оборудования:

```text
MOVING
  ↓
BUFFERED
  ↓
MOVING
```

При невозможности автоматической обработки:

```text
ERROR
  ↓
MANUAL_PROCESSING
```

Используемые статусы:

```text
CREATED
SCANNING
ROUTING
MOVING
BUFFERED
SORTED
MANUAL_PROCESSING
ERROR
```

---

## Application Layer

Application Layer координирует выполнение бизнес-операций.

Основным orchestration-компонентом является:

```text
Controller
```

Controller отвечает за:

- регистрацию товара;
- определение маршрута;
- обработку ошибок маршрутизации;
- передачу товара в Buffer;
- возврат товара из Buffer;
- отправку на Manual Processing;
- обработку событий Sensor;
- работу с Sorter;
- обновление Statistics.

Controller не должен самостоятельно реализовывать всю бизнес-логику.

Для отдельных операций используются Services.

---

## Services

Основные сервисы:

```text
ScanningService
RoutingService
BufferService
SortingService
```

---

## ScanningService

`ScanningService` отвечает за процесс сканирования товара.

Основные операции:

- перевод Item в состояние `SCANNING`;
- выполнение Scanner;
- получение barcode;
- переход Item в состояние `ROUTING`.

В синхронном backend-сценарии сканирование может выполняться полностью внутри сервиса.

В SimPy-сценарии начало и завершение сканирования разделены виртуальной задержкой.

---

## RoutingService

`RoutingService` отвечает за маршрутизацию.

Основные операции:

- запрос destination;
- работа с RouteProvider;
- выбор доступного Conveyor;
- передача Item на Conveyor;
- изменение статуса Item на `MOVING`.

---

## RouteProvider

Получение маршрута абстрагировано через интерфейс RouteProvider.

```text
RoutingService
      ↓
RouteProvider
      ↓
WMS
```

Это позволяет RoutingService не зависеть напрямую от конкретной реализации WMS.

---

## WMS

WMS хранит соответствие:

```text
barcode → destination
```

Пример:

```text
SIM-000000000001 → 1
SIM-000000000002 → 2
SIM-000000000003 → 3
```

В simulation layer маршруты создаются автоматически для сгенерированных товаров.

---

## BufferService

`BufferService` отвечает за временное хранение товаров.

Основные операции:

- отправка Item в Buffer;
- освобождение Item из Buffer;
- возврат Item обратно в Buffer при необходимости.

Основной сценарий:

```text
Conveyor full
     ↓
Buffer
     ↓
Retry
     ↓
Conveyor
```

Если Buffer также заполнен:

```text
Buffer full
     ↓
Manual Processing
```

---

## SortingService

`SortingService` отвечает за финальный этап сортировки.

Основные операции:

- сортировка Item;
- поиск нужного OutputBin;
- отправка товара в OutputBin;
- изменение статуса Item на `SORTED`;
- обновление location.

---

## Infrastructure Layer

Infrastructure Layer отвечает за технические детали хранения данных и взаимодействия с внешними системами.

Основные технологии:

```text
PostgreSQL
SQLAlchemy 2
Psycopg
Alembic
```

Domain-модели не содержат прямой SQL-логики.

---

## PostgreSQL

PostgreSQL используется для постоянного хранения данных.

База данных позволяет сохранять:

- товары;
- состояния обработки;
- события;
- результаты операций.

---

## SQLAlchemy

SQLAlchemy 2 используется как ORM и database toolkit.

Он отделяет persistence-логику от доменных объектов.

---

## Alembic

Alembic используется для управления схемой базы данных.

Применение миграций:

```bash
alembic upgrade head
```

Создание новой миграции:

```bash
alembic revision --autogenerate -m "migration description"
```

---

## API Layer

HTTP API реализован через FastAPI.

API Layer отвечает за:

- получение HTTP-запросов;
- validation;
- serialization;
- вызов application logic;
- формирование HTTP-ответов;
- OpenAPI;
- Swagger UI.

Pydantic используется для request/response schemas.

---

## Simulation Layer

Simulation Layer реализован через SimPy.

Его задача — моделировать физическую работу сортировочного центра с использованием виртуального времени.

Основные компоненты:

```text
SimulationConfig
SimulationRunner
ItemGenerator

ScannerStation
ConveyorStation
SorterStation

SimulationReport
```

---

## SimulationConfig

`SimulationConfig` содержит параметры виртуального сортировочного центра.

Основные параметры:

```text
duration_seconds
item_interval_seconds

scan_duration_seconds
scanner_capacity
scanner_error_rate

conveyor_length_meters
conveyor_speed_mps
conveyor_capacity

buffer_capacity
buffer_retry_interval_seconds

default_destination
destination_count

sorter_duration_seconds
sorter_capacity

output_bin_capacity
```

Конфигурация позволяет менять производительность системы без изменения business logic.

---

## SimulationRunner

`SimulationRunner` собирает полный виртуальный сортировочный центр.

Он отвечает за:

- создание `simpy.Environment`;
- создание Scanner;
- создание WMS;
- создание Controller;
- создание Conveyor;
- создание Buffer;
- создание Sensor;
- создание Sorter;
- создание OutputBins;
- запуск ItemGenerator;
- запуск фонового Buffer retry;
- запуск виртуального времени;
- сбор итоговых метрик.

---

## ItemGenerator

`ItemGenerator` генерирует новые товары через заданный временной интервал.

Параметр:

```text
item_interval_seconds
```

определяет интенсивность входного потока.

Для нагрузочного сценария:

```python
item_interval_seconds=0.036
```

что соответствует примерно:

```text
27.78 items/second
≈ 100,000 items/hour
```

---

## ScannerStation

`ScannerStation` использует:

```python
simpy.Resource
```

для моделирования ограниченной вычислительной или физической мощности Scanner.

Моделируются:

- количество параллельных scanning channels;
- текущая очередь;
- максимальная очередь;
- время ожидания;
- длительность сканирования.

Для high-load сценария:

```python
scanner_capacity=3
scan_duration_seconds=0.1
```

---

## ConveyorStation

`ConveyorStation` моделирует физическое перемещение Item.

Время движения:

```text
travel_time = conveyor_length / conveyor_speed
```

Для конфигурации:

```text
length = 10 m
speed = 2 m/s
```

получаем:

```text
travel_time = 5 seconds
```

Conveyor имеет ограничение на количество одновременно находящихся внутри товаров.

В high-load сценарии:

```python
conveyor_capacity=150
```

---

## Buffer

Buffer используется как временная очередь между этапами системы.

Если Conveyor не может сразу принять Item:

```text
Item
 ↓
Buffer
```

Background process периодически проверяет возможность повторной отправки:

```text
Buffer
 ↓
Retry
 ↓
Conveyor
```

Период retry задаётся:

```python
buffer_retry_interval_seconds
```

---

## Sensor

Sensor фиксирует появление товара перед сортировкой и создаёт событие для дальнейшей обработки.

Событие передаётся Controller.

---

## SorterStation

`SorterStation` также использует:

```python
simpy.Resource
```

Это позволяет моделировать несколько параллельных sorting channels.

High-load конфигурация:

```python
sorter_capacity=3
sorter_duration_seconds=0.1
```

После обработки Item направляется в OutputBin, соответствующий его destination.

---

## OutputBins

Для каждого destination создаётся отдельный `OutputBin`.

При:

```python
destination_count=400
```

автоматически создаются:

```text
OutputBin 1
OutputBin 2
OutputBin 3
...
OutputBin 400
```

Это позволяет моделировать сортировочный центр с сотнями направлений.

---

## 400-Destination Routing

Товары распределяются между направлениями детерминированно.

Используется циклическое распределение:

```text
Item 1   → Destination 1
Item 2   → Destination 2
...
Item 400 → Destination 400
Item 401 → Destination 1
```

Это обеспечивает равномерную нагрузку при performance testing.

---

## Statistics

Основная Statistics-модель собирает:

```text
processed_items
sorted_items
manual_processing_items
scan_errors
routing_errors
buffer_usage
conveyor_load
output_bin_load
average_conveyor_load
average_output_bin_load
simulation_time
throughput
success_rate
```

Simulation Layer добавляет дополнительные метрики:

```text
generated_items

scanner_current_queue
scanner_in_use
scanner_max_queue
scanner_average_wait_seconds

conveyor_current_queue
conveyor_in_use

sorter_current_queue
sorter_in_use

buffer_current_load
output_bin_current_load

arrival_rate_items_per_second
arrival_rate_items_per_hour

sorted_throughput_items_per_second
sorted_throughput_items_per_hour

in_flight_items
```

---

## Failure Handling

Система рассчитана на обработку ошибок без остановки всего pipeline.

Основные failure scenarios:

- Scanner error;
- Route not found;
- Equipment unavailable;
- Unsupported direction;
- Buffer full;
- OutputBin full;
- OutputBin not found.

Если автоматическая обработка невозможна:

```text
Item
 ↓
Manual Processing
```

---

## High-Load Validation

Система была протестирована при виртуальной нагрузке около:

```text
100,000 items/hour
```

и:

```text
400 sorting destinations
```

Используемая конфигурация:

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

Полученный результат:

```text
Generated:             16,667
Sorted:                16,523

Arrival rate:          100,002 items/hour
Sorted throughput:      99,138 items/hour

Scanner queue:               0
Conveyor queue:              0
Sorter queue:                0
Buffer load:                 0

Manual Processing:           0
Routing errors:              0
Scan errors:                 0

In-flight items:           144
```

Оставшиеся `144` товара находились внутри pipeline в момент завершения simulation window.

---

## Bottleneck Detection

SimPy использовался не только для генерации нагрузки, но и для поиска bottleneck'ов.

Последовательность обнаруженных ограничений:

```text
Scanner
   ↓
Conveyor
   ↓
Sorter
   ↓
OutputBin
```

После каждого теста конфигурация изменялась только для текущего bottleneck.

Это позволило определить минимально необходимую конфигурацию оборудования для целевого потока.

---

## Continuous Integration

GitHub Actions автоматически запускается при:

```text
push
pull_request
```

CI pipeline:

```text
Checkout
   ↓
Python 3.14
   ↓
Install Dependencies
   ↓
Ruff
   ↓
Mypy
   ↓
Pytest
```

CI гарантирует автоматическую проверку:

- linting;
- static typing;
- tests.

---

## Architectural Principles

Основные архитектурные принципы проекта:

- separation of concerns;
- dependency isolation;
- typed Python;
- reusable domain logic;
- explicit business rules;
- custom exceptions;
- infrastructure isolation;
- testability;
- deterministic simulation;
- measurable performance;
- configurable scalability;
- automated quality control.

---

## Architecture Goals

Архитектура проекта должна позволять:

- независимо развивать API;
- независимо менять persistence layer;
- тестировать domain logic без HTTP;
- тестировать domain logic без PostgreSQL;
- использовать одну бизнес-логику в API и SimPy;
- моделировать разные конфигурации оборудования;
- обнаруживать bottleneck'и;
- масштабировать количество destinations;
- добавлять новые типы оборудования;
- сохранять строгую типизацию и тестируемость.
````