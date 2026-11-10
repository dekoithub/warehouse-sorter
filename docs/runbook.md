# Runbook

## Overview

Этот документ описывает практический запуск, проверку и диагностику проекта Warehouse Sorter.

Runbook нужен для того, чтобы любой разработчик мог:

- клонировать проект;
- установить зависимости;
- поднять PostgreSQL;
- применить миграции;
- запустить FastAPI;
- открыть Swagger;
- запустить Docker Compose;
- выполнить тесты;
- выполнить Ruff и Mypy;
- запустить SimPy simulation;
- проверить high-load scenario;
- диагностировать типовые проблемы.

---

# Requirements

Для локальной разработки необходимы:

```text
Python 3.14
Git
PostgreSQL
Docker Desktop
Docker Compose
```

Для Windows рекомендуется:

```text
Windows
Git Bash
Docker Desktop
VS Code
```

---

# Clone Repository

Клонировать проект:

```bash
git clone <repository-url>
```

Перейти в директорию:

```bash
cd warehouse-sorter
```

Проверить текущую ветку:

```bash
git branch
```

---

# Virtual Environment

Создать виртуальное окружение:

```bash
python -m venv .venv
```

---

## Activate on Windows / Git Bash

```bash
source .venv/Scripts/activate
```

После активации terminal prompt должен содержать:

```text
(.venv)
```

---

## Deactivate

```bash
deactivate
```

---

# Install Dependencies

Установить проект вместе с development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Проверить Python:

```bash
python --version
```

Ожидаемая версия:

```text
Python 3.14.x
```

---

# Project Structure

Основные директории:

```text
src/
tests/
docs/
alembic/
.github/
```

Основные конфигурационные файлы:

```text
pyproject.toml
alembic.ini
compose.yaml
Dockerfile
```

---

# Environment Variables

Если проект использует `.env`, файл не должен попадать в Git.

Проверить:

```bash
git status
```

и:

```bash
git check-ignore .env
```

Секреты и локальные credentials не должны храниться в repository.

---

# PostgreSQL

Проект использует PostgreSQL как основную persistent database.

Основной database stack:

```text
PostgreSQL
SQLAlchemy 2
Psycopg
Alembic
```

---

# Start PostgreSQL with Docker

Самый простой способ поднять PostgreSQL вместе с приложением:

```bash
docker compose up
```

Или в background:

```bash
docker compose up -d
```

Проверить контейнеры:

```bash
docker compose ps
```

---

# Stop Docker Environment

Остановить containers:

```bash
docker compose down
```

---

# Stop and Remove Volumes

Если необходимо полностью удалить database volume:

```bash
docker compose down -v
```

Важно:

эта команда удаляет persistent Docker volumes.

Данные PostgreSQL будут потеряны.

---

# Docker Build

Стандартная сборка:

```bash
docker compose build
```

На текущей Windows / Docker Desktop конфигурации может использоваться:

```bash
BUILDX_BAKE_ENTITLEMENTS_FS=0 docker compose build
```

После успешной сборки:

```bash
docker compose up
```

---

# Rebuild After Code Changes

Если необходимо пересобрать image:

```bash
BUILDX_BAKE_ENTITLEMENTS_FS=0 docker compose build
docker compose up
```

Или:

```bash
BUILDX_BAKE_ENTITLEMENTS_FS=0 docker compose up --build
```

---

# Docker Status

Показать работающие сервисы:

```bash
docker compose ps
```

Показать все containers:

```bash
docker ps -a
```

---

# Docker Logs

Посмотреть logs всех сервисов:

```bash
docker compose logs
```

Следить за logs:

```bash
docker compose logs -f
```

Для конкретного сервиса:

```bash
docker compose logs -f <service-name>
```

---

# Database Migrations

Перед работой API schema базы данных должна соответствовать текущему коду.

Применить все migrations:

```bash
alembic upgrade head
```

---

## Check Current Migration

```bash
alembic current
```

---

## View Migration History

```bash
alembic history
```

---

## Create New Migration

После изменения SQLAlchemy models:

```bash
alembic revision --autogenerate -m "migration description"
```

После создания migration необходимо проверить generated file вручную.

---

## Apply New Migration

```bash
alembic upgrade head
```

---

# Run FastAPI Locally

Активировать virtual environment:

```bash
source .venv/Scripts/activate
```

Запустить приложение через Uvicorn:

```bash
uvicorn api.main:app --reload
```

Если `src` не находится автоматически в Python path, использовать запуск через package configuration проекта.

---

# API Address

После запуска API:

```text
http://localhost:8000
```

---

# Health Check

Открыть:

```text
http://localhost:8000/health
```

Ожидаемый response:

```json
{
  "status": "ok"
}
```

---

# Swagger UI

Открыть:

```text
http://localhost:8000/docs
```

Swagger позволяет:

- просматривать endpoints;
- отправлять requests;
- проверять schemas;
- тестировать API.

---

# ReDoc

```text
http://localhost:8000/redoc
```

---

# OpenAPI

```text
http://localhost:8000/openapi.json
```

---

# Basic API Verification

После запуска API можно проверить health endpoint:

```bash
curl http://localhost:8000/health
```

Ожидаемый результат:

```json
{"status":"ok"}
```

---

# Create Destination

Пример:

```bash
curl -X POST http://localhost:8000/destinations \
  -H "Content-Type: application/json" \
  -d '{
    "code": 5,
    "name": "Output Zone 5"
  }'
```

---

# Create Route

```bash
curl -X POST http://localhost:8000/routes \
  -H "Content-Type: application/json" \
  -d '{
    "barcode": "ITEM-0001",
    "destination_code": 5
  }'
```

---

# Create Item

```bash
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{
    "barcode": "ITEM-0001",
    "weight": 2.5,
    "width": 20,
    "height": 10,
    "length": 30,
    "category": "electronics",
    "delivery_type": "standard",
    "status": "CREATED",
    "location": "RECEIVING"
  }'
```

---

# Process Item

```bash
curl -X POST http://localhost:8000/items/ITEM-0001/process
```

При успешной обработке Item должен перейти в состояние:

```text
SORTED
```

и получить destination и OutputBin.

---

# Read Item

```bash
curl http://localhost:8000/items/ITEM-0001
```

---

# Read Processing Events

```bash
curl http://localhost:8000/items/ITEM-0001/events
```

---

# Quality Checks

Перед commit рекомендуется выполнить полный набор локальных проверок.

---

## Pytest

```bash
python -m pytest
```

Все tests должны завершиться успешно.

---

## Ruff

```bash
python -m ruff check src tests
```

---

## Ruff Auto Fix

```bash
python -m ruff check src tests --fix
```

---

## Ruff Format

```bash
python -m ruff format src tests
```

---

## Mypy

```bash
python -m mypy src tests
```

---

# Full Local Quality Check

Можно выполнить последовательно:

```bash
python -m ruff check src tests
python -m mypy src tests
python -m pytest
```

Это соответствует основным проверкам CI.

---

# GitHub Actions CI

GitHub Actions автоматически запускается при:

```text
push
pull_request
```

CI выполняет:

```text
Ruff
 ↓
Mypy
 ↓
Pytest
```

Если одна из проверок завершается с ошибкой, workflow становится:

```text
Failed
```

Если все проверки успешны:

```text
Success
```

---

# Run Simulation

Запуск simulation layer:

```bash
python -m simulation.main
```

Simulation использует:

```text
SimPy
```

для моделирования виртуального времени и физических ограничений оборудования.

---

# Simulation Configuration

Основные параметры находятся в:

```text
src/simulation/config.py
```

Конфигурация включает:

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

---

# High-Load Scenario

Проверенная high-load конфигурация:

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

Целевая нагрузка:

```text
~100,000 items/hour
```

Количество направлений:

```text
400
```

---

# Expected High-Load Result

При simulation duration:

```text
600 seconds
```

был получен результат примерно:

```text
Generated items:                 16,667
Sorted items:                    16,523

Arrival rate:                   100,002 items/hour
Sorted throughput:               99,138 items/hour

Scanner queue:                        0
Conveyor queue:                       0
Sorter queue:                         0
Buffer load:                          0

Manual Processing:                    0
Routing errors:                       0
Scan errors:                          0

In-flight items:                    144
```

---

# Verify Item Accounting

Для stable high-load test:

```text
Sorted + In-flight = Generated
```

Проверка:

```text
16,523 + 144 = 16,667
```

Это означает, что товары не теряются внутри simulation pipeline.

---

# Expected In-Flight State

На момент завершения simulation:

```text
scanner_in_use = 3
conveyor_in_use = 138
sorter_in_use = 3
```

Сумма:

```text
3 + 138 + 3 = 144
```

что соответствует:

```text
in_flight_items = 144
```

---

# 400-Destination Verification

При:

```python
destination_count=400
```

должно быть создано:

```text
400 OutputBins
```

Идентификаторы:

```text
1 ... 400
```

В validated load test товары распределились примерно:

```text
OutputBin 1–123   → 42 items
OutputBin 124–400 → 41 items
```

Средняя загрузка:

```text
41.3075 items/bin
```

---

# Troubleshooting

## Python Command Not Found

Проверить:

```bash
python --version
```

Если Python недоступен, проверить installation и PATH.

---

## Virtual Environment Not Active

Terminal prompt должен содержать:

```text
(.venv)
```

Если нет:

```bash
source .venv/Scripts/activate
```

---

## Module Not Found

Переустановить проект:

```bash
python -m pip install -e ".[dev]"
```

---

## Ruff Not Found

Проверить installation:

```bash
python -m ruff --version
```

Если package отсутствует:

```bash
python -m pip install -e ".[dev]"
```

---

## Mypy Not Found

```bash
python -m mypy --version
```

При необходимости:

```bash
python -m pip install -e ".[dev]"
```

---

## Pytest Not Found

```bash
python -m pytest --version
```

При необходимости:

```bash
python -m pip install -e ".[dev]"
```

---

# PostgreSQL Connection Error

Если приложение не может подключиться к PostgreSQL:

проверить containers:

```bash
docker compose ps
```

Проверить logs:

```bash
docker compose logs
```

Убедиться, что PostgreSQL имеет состояние:

```text
healthy
```

---

# Database Schema Error

Если приложение сообщает об отсутствующей таблице или column:

```bash
alembic current
alembic history
alembic upgrade head
```

---

# Docker Build Error

Очистить и повторить build:

```bash
docker compose down
BUILDX_BAKE_ENTITLEMENTS_FS=0 docker compose build
```

---

# Docker Container Fails on Startup

Посмотреть logs:

```bash
docker compose logs
```

или:

```bash
docker compose logs -f
```

Проверить:

- database availability;
- environment variables;
- migration errors;
- Python import errors.

---

# Port 8000 Already in Use

Проверить процессы.

В Windows:

```bash
netstat -ano | findstr :8000
```

Либо запустить Uvicorn на другом порту:

```bash
uvicorn api.main:app --reload --port 8001
```

После этого Swagger:

```text
http://localhost:8001/docs
```

---

# Simulation Queue Growth

Если:

```text
scanner_current_queue
```

или:

```text
scanner_max_queue
```

быстро растёт, Scanner является bottleneck.

Проверить:

```text
scanner_capacity
scan_duration_seconds
```

---

# Conveyor Queue Growth

Если растёт:

```text
conveyor_current_queue
```

проверить:

```text
conveyor_capacity
conveyor_length_meters
conveyor_speed_mps
```

Время transport:

```text
travel_time = length / speed
```

---

# Sorter Queue Growth

Если растёт:

```text
sorter_current_queue
```

проверить:

```text
sorter_capacity
sorter_duration_seconds
```

---

# Buffer Growth

Если растёт:

```text
buffer_current_load
```

это обычно означает, что downstream equipment не успевает обрабатывать входящий поток.

Необходимо искать bottleneck после Buffer.

---

# Manual Processing Growth

Если увеличивается:

```text
manual_processing_items
```

проверить:

- scan errors;
- routing errors;
- Buffer overflow;
- OutputBin capacity;
- unsupported destinations;
- missing routes.

---

# Scan Errors

Если:

```text
scan_errors > 0
```

проверить:

```text
scanner_error_rate
```

Для baseline performance test используется:

```python
scanner_error_rate=0.0
```

---

# Routing Errors

Если:

```text
routing_errors > 0
```

проверить:

- существует ли Route;
- существует ли Destination;
- active ли Destination;
- поддерживает ли Sorter нужное направление.

---

# OutputBin Full

Если OutputBin достигает capacity:

проверить:

```text
output_bin_capacity
destination_count
```

Для длительного 100k/hour scenario используется:

```python
output_bin_capacity=20000
```

---

# Git Workflow

Перед изменениями:

```bash
git status
```

После изменений:

```bash
git diff
```

Проверить staged changes:

```bash
git diff --cached
```

---

# Before Commit Checklist

Перед commit выполнить:

```bash
python -m ruff check src tests
python -m mypy src tests
python -m pytest
```

Затем проверить:

```bash
git status
```

---

# Before Push Checklist

Перед push убедиться, что:

```text
Ruff        passed
Mypy        passed
Pytest      passed
```

После push проверить GitHub Actions.

---

# Production-Like Verification

Минимальная end-to-end проверка:

```text
1. PostgreSQL запущен
2. Alembic migrations применены
3. FastAPI запущен
4. /health возвращает 200
5. Destination создан
6. Route создан
7. Item создан
8. Item обработан
9. Item имеет статус SORTED
10. ProcessingEvent сохранён
```

---

# Recommended Development Sequence

Обычный development workflow:

```text
Activate .venv
      ↓
Pull latest changes
      ↓
Implement changes
      ↓
Run Ruff
      ↓
Run Mypy
      ↓
Run Pytest
      ↓
Run application/simulation if required
      ↓
Review git diff
      ↓
Commit
      ↓
Push
      ↓
Verify GitHub Actions
```

---

# Documentation

Основные документы проекта:

```text
README.md
README_RU.md
docs/architecture.md
docs/calculations.md
docs/api.md
docs/runbook.md
```

Назначение:

```text
README.md
→ основной overview проекта

README_RU.md
→ русская версия overview

architecture.md
→ устройство системы и ответственность компонентов

calculations.md
→ расчёты throughput и capacity

api.md
→ REST API

runbook.md
→ запуск, проверки и диагностика
```

---

# Final Health Checklist

Проект находится в корректном состоянии, если:

```text
Docker build             PASS
PostgreSQL               HEALTHY
Alembic                  HEAD
FastAPI /health          200 OK
Swagger                  AVAILABLE

Ruff                     PASS
Mypy                     PASS
Pytest                   PASS
GitHub Actions           SUCCESS

Simulation               PASS
100k/hour scenario       PASS
400 destinations         PASS
```

---

# Summary

Warehouse Sorter можно проверить на трёх уровнях:

## Backend

```text
FastAPI
PostgreSQL
SQLAlchemy
Alembic
```

## Quality

```text
Ruff
Mypy
Pytest
GitHub Actions
```

## Simulation

```text
SimPy
100,000 items/hour
400 destinations
Bottleneck metrics
```

Runbook позволяет воспроизвести основные сценарии проекта, проверить работоспособность системы и локализовать проблемы без изучения всего исходного кода.
````