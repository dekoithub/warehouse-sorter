# Warehouse Sorter

Backend-система и дискретно-событийная симуляция автоматизированного сортировочного центра.

Проект моделирует полный жизненный цикл товара внутри сортировочного центра: сканирование, определение маршрута через WMS, транспортировку по конвейеру, временное хранение в буфере, сортировку и доставку в выходной накопитель.

Проект сочетает production-подход к разработке Python backend-приложения и SimPy-симуляцию, позволяющую моделировать нагрузку, находить узкие места инфраструктуры и проверять масштабируемость системы.

---

## Основные возможности

- управление жизненным циклом товара;
- сканирование штрихкодов;
- определение маршрута через WMS;
- транспортировка товаров по конвейеру;
- буферизация при временной недоступности конвейера;
- повторная отправка товаров из буфера;
- автоматическая сортировка;
- отправка проблемных товаров на ручную обработку;
- работа с выходными накопителями;
- сбор статистики;
- PostgreSQL;
- миграции через Alembic;
- REST API на FastAPI;
- Docker и Docker Compose;
- дискретно-событийная симуляция на SimPy;
- моделирование высокой нагрузки;
- поддержка сотен направлений сортировки;
- автоматический CI через GitHub Actions.

---

## Производительность симуляции

Слой симуляции используется для моделирования высоконагруженного сортировочного центра.

В ходе нагрузочного тестирования была проверена конфигурация примерно на:

- **100 000 поступающих товаров в час**;
- **400 направлений сортировки**;
- несколько параллельных каналов сканирования;
- параллельную обработку сортировщиком;
- моделирование ёмкости конвейера;
- использование буфера;
- маршрутизацию в выходные накопители;
- виртуальное время сортировочного центра.

### Результат нагрузочного теста

Продолжительность виртуальной симуляции:

```text
600 секунд
```

Результат:

```text
Сгенерировано товаров:        16 667
Отсортировано товаров:        16 523

Входной поток:                ~100 002 товаров/час
Выходной throughput:          ~99 138 товаров/час

Очередь Scanner:              0
Очередь Conveyor:             0
Очередь Sorter:               0

Buffer:                       0
Manual Processing:            0

Routing errors:               0
Scan errors:                  0
```

Оставшиеся товары находились внутри pipeline в момент окончания виртуального времени симуляции.

---

## 400 направлений сортировки

Количество направлений задаётся через конфигурацию:

```python
destination_count=400
```

При такой конфигурации автоматически создаются направления:

```text
Destination 1
Destination 2
Destination 3
...
Destination 400
```

Для каждого направления создаётся собственный `OutputBin`.

Маршрут товара определяется через WMS, после чего Sorter направляет товар в соответствующий выходной накопитель.

### Распределение нагрузки

В тесте на 400 направлений:

```text
OutputBin 1–123   → 42 товара
OutputBin 124–400 → 41 товар
```

Всего:

```text
16 523 отсортированных товара
400 направлений
```

---

## Архитектура проекта

Проект разделён на несколько уровней ответственности:

- API;
- Application Layer;
- Domain Models;
- Services;
- Infrastructure;
- Simulation.

### Структура

```text
src/
├── api/
│
├── application/
│   ├── controller.py
│   ├── controllers/
│   ├── ports/
│   └── use_cases/
│
├── infrastructure/
│
├── models/
│   ├── buffer.py
│   ├── conveyor.py
│   ├── enums.py
│   ├── events.py
│   ├── exceptions.py
│   ├── item.py
│   ├── output_bin.py
│   ├── scanner.py
│   ├── sensor.py
│   ├── sorter.py
│   ├── statistics.py
│   └── wms.py
│
├── services/
│   ├── buffer_service.py
│   ├── route_provider.py
│   ├── routing_service.py
│   ├── scanning_service.py
│   └── sorting_service.py
│
└── simulation/
    ├── stations/
    │   ├── conveyor_station.py
    │   ├── scanner_station.py
    │   └── sorter_station.py
    │
    ├── config.py
    ├── item_generator.py
    ├── main.py
    ├── report.py
    └── runner.py
```

---

## Pipeline обработки товара

Обычный путь товара:

```text
Item
  ↓
Scanner
  ↓
WMS
  ↓
Route resolution
  ↓
Conveyor
  ↓
Sensor
  ↓
Sorter
  ↓
OutputBin
```

Если Conveyor временно перегружен:

```text
Conveyor unavailable
        ↓
      Buffer
        ↓
      Retry
        ↓
     Conveyor
```

Если товар невозможно обработать автоматически:

```text
Processing Error
      ↓
Manual Processing
```

---

## Статусы товара

В системе используются следующие состояния:

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

Они позволяют отслеживать жизненный цикл товара на каждом этапе обработки.

---

## Технологический стек

### Backend

- Python 3.14
- FastAPI
- Pydantic
- SQLAlchemy 2
- PostgreSQL
- Alembic
- Psycopg

### Simulation

- SimPy

### Тестирование и качество кода

- Pytest
- Mypy
- Ruff

### Infrastructure

- Docker
- Docker Compose
- GitHub Actions

---

## Установка

Клонировать репозиторий:

```bash
git clone <repository-url>
cd warehouse-sorter
```

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать окружение в Windows через Git Bash:

```bash
source .venv/Scripts/activate
```

Установить проект вместе с development-зависимостями:

```bash
python -m pip install -e ".[dev]"
```

---

## Проверка качества кода

### Pytest

```bash
python -m pytest
```

### Ruff

```bash
python -m ruff check src tests
```

Автоматическое исправление:

```bash
python -m ruff check src tests --fix
```

Форматирование:

```bash
python -m ruff format src tests
```

### Mypy

```bash
python -m mypy src tests
```

---

## Запуск симуляции

```bash
python -m simulation.main
```

Основная конфигурация находится в:

```text
src/simulation/config.py
```

---

## Конфигурация симуляции

Можно настраивать:

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

### Пример высоконагруженной конфигурации

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

## Метрики симуляции

Финальный отчёт содержит:

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

Метрики позволяют находить bottleneck'и и проверять, соответствует ли конфигурация оборудования заданной нагрузке.

---

## Поиск bottleneck'ов

При нагрузочном тестировании система масштабировалась последовательно.

### Scanner

Первым bottleneck стал Scanner.

При одном канале сканирования начала быстро расти очередь входящих товаров.

После увеличения:

```python
scanner_capacity=3
```

очередь Scanner исчезла.

### Conveyor

Следующим ограничением стал Conveyor.

После расчёта необходимого количества одновременно находящихся на конвейере товаров была увеличена его ёмкость:

```python
conveyor_capacity=150
```

### Sorter

После снятия ограничения Conveyor очередь переместилась на Sorter.

Sorter был масштабирован:

```python
sorter_capacity=3
```

### OutputBin

После увеличения производительности Sorter ограничением стала вместимость OutputBin.

В нагрузочном сценарии она была увеличена:

```python
output_bin_capacity=20000
```

### Итог

После настройки компонентов система смогла устойчиво моделировать поток порядка:

```text
100 000 товаров/час
```

без:

```text
Scanner queue
Conveyor queue
Sorter queue
Buffer overflow
Manual Processing
Routing errors
Scan errors
```

при штатном нагрузочном сценарии.

---

## Docker

### Сборка

```bash
BUILDX_BAKE_ENTITLEMENTS_FS=0 docker compose build
```

### Запуск

```bash
docker compose up
```

Контейнеризированное окружение включает:

- FastAPI;
- PostgreSQL;
- healthcheck;
- автоматическое применение Alembic migrations.

---

## PostgreSQL

Для постоянного хранения данных используется PostgreSQL.

Стек работы с БД:

```text
SQLAlchemy 2
Psycopg
Alembic
PostgreSQL
```

---

## Alembic

Применить миграции:

```bash
alembic upgrade head
```

Создать новую миграцию:

```bash
alembic revision --autogenerate -m "migration description"
```

---

## FastAPI

Проект предоставляет REST API для работы с системой сортировки.

Архитектурно backend разделён между:

```text
API
 ↓
Application Layer
 ↓
Services
 ↓
Domain Models
 ↓
Infrastructure
```

Документация API доступна через Swagger UI.

---

## GitHub Actions / CI

В проекте настроен автоматический CI через GitHub Actions.

Workflow запускается при:

```text
push
pull_request
```

Pipeline:

```text
Checkout repository
        ↓
Python 3.14
        ↓
Install dependencies
        ↓
Ruff
        ↓
Mypy
        ↓
Pytest
```

Если одна из проверок завершается ошибкой, CI job завершается неуспешно.

---

## Тестирование

Тестами покрываются:

- domain models;
- Controller;
- services;
- Buffer;
- Conveyor;
- Scanner;
- Sensor;
- Sorter;
- OutputBin;
- маршрутизация;
- обработка ошибок;
- база данных;
- API;
- SimPy simulation;
- scanner queues;
- conveyor load;
- buffer overflow;
- manual processing;
- несколько направлений;
- конфигурация на 400 направлений.

---

## Обработка ошибок

В проекте используются собственные исключения бизнес-логики.

Обрабатываются сценарии:

```text
оборудование недоступно
маршрут не найден
направление не поддерживается
Buffer переполнен
OutputBin переполнен
OutputBin не найден
ошибка сканирования
```

Проблемные товары могут перенаправляться в:

```text
Manual Processing
```

без остановки всей системы.

---

## Цели проекта

Проект создаётся не как простой CRUD, а как production-oriented backend и system-design проект.

Основные цели:

- моделирование реального предметного домена;
- разделение ответственности между слоями;
- строгая типизация Python;
- автоматические тесты;
- PostgreSQL;
- миграции базы данных;
- REST API;
- Docker;
- моделирование физического оборудования;
- дискретно-событийная симуляция;
- нагрузочное тестирование;
- поиск bottleneck'ов;
- проверка масштабируемости;
- автоматический CI.

---

## Реализовано

- Domain Models
- Item Lifecycle
- Scanner
- WMS
- Routing
- Conveyor
- Buffer
- Sensor
- Sorter
- OutputBin
- Controller
- Services
- Custom Exceptions
- Logging
- Statistics
- PostgreSQL
- SQLAlchemy 2
- Alembic
- FastAPI
- Pydantic
- Docker
- Docker Compose
- Pytest
- Ruff
- Mypy
- SimPy
- Typed Simulation Reports
- Scanner Queue Metrics
- Conveyor Metrics
- Sorter Metrics
- Buffer Retry
- Manual Processing Fallback
- Load Simulation
- ~100 000 товаров/час
- 400 направлений сортировки
- GitHub Actions CI

---

## Текущий статус

Основная функциональность backend и simulation layer реализована.

Подтверждена работа системы при моделируемой нагрузке порядка:

```text
~100 000 товаров/час
```

и:

```text
400 направлений сортировки
```

Проект находится на финальном этапе:

```text
Документация
      ↓
Финальная упаковка
      ↓
Portfolio-ready release
```

---

## Автор

**Denis Korchitskiy**

Python Backend Developer

GitHub:

```text
https://github.com/dekoithub
```