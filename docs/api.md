# API Documentation

## Overview

Warehouse Sorter предоставляет REST API на FastAPI для управления основными сущностями сортировочного центра.

API позволяет:

- проверять состояние приложения;
- создавать и получать направления сортировки;
- включать и отключать направления;
- создавать маршруты для barcode;
- получать маршруты;
- включать и отключать маршруты;
- создавать товары;
- получать товары;
- изменять состояние товара;
- запускать полный processing pipeline товара;
- получать историю processing events.

Название API:

```text
Warehouse Sorter API
```

Версия:

```text
1.0.0
```

---

## Base URL

При локальном запуске API:

```text
http://localhost:8000
```

---

## Swagger UI

FastAPI автоматически предоставляет интерактивную Swagger-документацию:

```text
http://localhost:8000/docs
```

Через Swagger UI можно:

- просматривать все endpoints;
- смотреть request schemas;
- смотреть response schemas;
- отправлять запросы;
- проверять status codes;
- тестировать API без отдельного HTTP-клиента.

---

## ReDoc

Дополнительная документация FastAPI:

```text
http://localhost:8000/redoc
```

---

## OpenAPI Schema

OpenAPI JSON:

```text
http://localhost:8000/openapi.json
```

---

# Health

## GET /health

Проверяет работоспособность API.

### Request

```http
GET /health
```

### Response

```json
{
  "status": "ok"
}
```

### Status Code

```text
200 OK
```

---

# Destinations

Destination представляет направление сортировки.

Например:

```text
Destination 1
Destination 2
Destination 3
...
Destination 400
```

Endpoints имеют prefix:

```text
/destinations
```

---

## GET /destinations

Возвращает список всех направлений.

### Request

```http
GET /destinations
```

### Response

```json
[
  {
    "id": 1,
    "code": 1,
    "name": "Destination 1",
    "is_active": true
  },
  {
    "id": 2,
    "code": 2,
    "name": "Destination 2",
    "is_active": true
  }
]
```

### Status Code

```text
200 OK
```

---

## GET /destinations/{code}

Возвращает направление по его code.

### Request

```http
GET /destinations/1
```

### Path Parameter

```text
code: integer > 0
```

### Response

```json
{
  "id": 1,
  "code": 1,
  "name": "Destination 1",
  "is_active": true
}
```

### Status Code

```text
200 OK
```

Если направление не найдено:

```text
404 Not Found
```

Response:

```json
{
  "detail": "Destination not found"
}
```

---

## POST /destinations

Создаёт новое направление сортировки.

### Request

```http
POST /destinations
Content-Type: application/json
```

Body:

```json
{
  "code": 1,
  "name": "Destination 1"
}
```

### Validation

`code`:

```text
integer > 0
```

`name`:

```text
non-empty string
```

### Response

```json
{
  "id": 1,
  "code": 1,
  "name": "Destination 1",
  "is_active": true
}
```

### Status Code

```text
201 Created
```

Если Destination с таким code уже существует:

```text
409 Conflict
```

Response:

```json
{
  "detail": "Destination with this code already exists"
}
```

---

## PATCH /destinations/{code}

Изменяет active state направления.

### Request

```http
PATCH /destinations/1
Content-Type: application/json
```

Body:

```json
{
  "is_active": false
}
```

### Response

```json
{
  "id": 1,
  "code": 1,
  "name": "Destination 1",
  "is_active": false
}
```

### Status Code

```text
200 OK
```

Если Destination не найден:

```text
404 Not Found
```

---

# Routes

Route связывает barcode товара с destination.

Пример:

```text
ITEM-0001
    ↓
Destination 5
```

Endpoints имеют prefix:

```text
/routes
```

---

## GET /routes

Возвращает все зарегистрированные маршруты.

### Request

```http
GET /routes
```

### Response

```json
[
  {
    "id": 1,
    "barcode": "ITEM-0001",
    "destination_id": 5,
    "is_active": true,
    "created_at": "2026-11-11T12:00:00"
  }
]
```

### Status Code

```text
200 OK
```

---

## GET /routes/{barcode}

Возвращает маршрут для указанного barcode.

### Request

```http
GET /routes/ITEM-0001
```

### Path Parameter

```text
barcode: non-empty string
```

### Response

```json
{
  "id": 1,
  "barcode": "ITEM-0001",
  "destination_id": 5,
  "is_active": true,
  "created_at": "2026-11-11T12:00:00"
}
```

### Status Code

```text
200 OK
```

Если Route не найден:

```text
404 Not Found
```

Response:

```json
{
  "detail": "Route not found"
}
```

---

## POST /routes

Создаёт новый маршрут.

### Request

```http
POST /routes
Content-Type: application/json
```

Body:

```json
{
  "barcode": "ITEM-0001",
  "destination_code": 5
}
```

### Validation

`barcode`:

```text
non-empty string
```

`destination_code`:

```text
integer > 0
```

### Response

```json
{
  "id": 1,
  "barcode": "ITEM-0001",
  "destination_id": 5,
  "is_active": true,
  "created_at": "2026-11-11T12:00:00"
}
```

### Status Code

```text
201 Created
```

Если Route для указанного barcode уже существует:

```text
409 Conflict
```

Response:

```json
{
  "detail": "Route for this barcode already exists"
}
```

Если указанный Destination не существует, API возвращает:

```text
404 Not Found
```

---

## PATCH /routes/{barcode}

Включает или отключает существующий Route.

### Request

```http
PATCH /routes/ITEM-0001
Content-Type: application/json
```

Body:

```json
{
  "is_active": false
}
```

### Response

```json
{
  "id": 1,
  "barcode": "ITEM-0001",
  "destination_id": 5,
  "is_active": false,
  "created_at": "2026-11-11T12:00:00"
}
```

### Status Code

```text
200 OK
```

Если Route не найден:

```text
404 Not Found
```

---

# Items

Item представляет товар, проходящий через сортировочный центр.

Endpoints имеют prefix:

```text
/items
```

---

## Item Statuses

Поддерживаются следующие статусы:

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

## GET /items

Возвращает список всех товаров.

### Request

```http
GET /items
```

### Response

```json
[
  {
    "id": 1,
    "barcode": "ITEM-0001",
    "weight": "2.5",
    "width": 20,
    "height": 10,
    "length": 30,
    "category": "electronics",
    "delivery_type": "standard",
    "is_flammable": false,
    "status": "CREATED",
    "destination_id": null,
    "location": "RECEIVING",
    "created_at": "2026-11-11T12:00:00"
  }
]
```

### Status Code

```text
200 OK
```

---

## GET /items/{barcode}

Возвращает товар по barcode.

### Request

```http
GET /items/ITEM-0001
```

### Path Parameter

```text
barcode: non-empty string
```

### Response

```json
{
  "id": 1,
  "barcode": "ITEM-0001",
  "weight": "2.5",
  "width": 20,
  "height": 10,
  "length": 30,
  "category": "electronics",
  "delivery_type": "standard",
  "is_flammable": false,
  "status": "CREATED",
  "destination_id": null,
  "location": "RECEIVING",
  "created_at": "2026-11-11T12:00:00"
}
```

### Status Code

```text
200 OK
```

Если Item не найден:

```text
404 Not Found
```

Response:

```json
{
  "detail": "Item not found"
}
```

---

## POST /items

Создаёт новый Item.

### Request

```http
POST /items
Content-Type: application/json
```

Body:

```json
{
  "barcode": "ITEM-0001",
  "weight": 2.5,
  "width": 20,
  "height": 10,
  "length": 30,
  "category": "electronics",
  "delivery_type": "standard",
  "status": "CREATED",
  "location": "RECEIVING",
  "destination_code": null
}
```

### Required Fields

```text
barcode
weight
width
height
length
category
delivery_type
location
```

`status` по умолчанию:

```text
CREATED
```

`destination_code` может быть:

```text
null
```

---

## Item Validation

### barcode

```text
non-empty string
```

### weight

```text
Decimal > 0
```

### width

```text
integer > 0
```

### height

```text
integer > 0
```

### length

```text
integer > 0
```

### category

```text
non-empty string
```

### delivery_type

```text
non-empty string
```

### destination_code

```text
integer > 0
```

или:

```text
null
```

---

## POST /items Response

```json
{
  "id": 1,
  "barcode": "ITEM-0001",
  "weight": "2.5",
  "width": 20,
  "height": 10,
  "length": 30,
  "category": "electronics",
  "delivery_type": "standard",
  "is_flammable": false,
  "status": "CREATED",
  "destination_id": null,
  "location": "RECEIVING",
  "created_at": "2026-11-11T12:00:00"
}
```

### Status Code

```text
201 Created
```

Если Item с таким barcode уже существует:

```text
409 Conflict
```

Response:

```json
{
  "detail": "Item with this barcode already exists"
}
```

Если передан некорректный связанный объект, API может вернуть:

```text
404 Not Found
```

---

# Update Item State

## PATCH /items/{barcode}

Изменяет status и location существующего Item.

### Request

```http
PATCH /items/ITEM-0001
Content-Type: application/json
```

Body:

```json
{
  "status": "MOVING",
  "location": "CONVEYOR-1"
}
```

### Response

```json
{
  "id": 1,
  "barcode": "ITEM-0001",
  "weight": "2.5",
  "width": 20,
  "height": 10,
  "length": 30,
  "category": "electronics",
  "delivery_type": "standard",
  "is_flammable": false,
  "status": "MOVING",
  "destination_id": 5,
  "location": "CONVEYOR-1",
  "created_at": "2026-11-11T12:00:00"
}
```

### Status Code

```text
200 OK
```

Если Item не найден:

```text
404 Not Found
```

---

# Process Item

## POST /items/{barcode}/process

Запускает application use case полного processing pipeline для существующего Item.

### Request

```http
POST /items/ITEM-0001/process
```

Endpoint создаёт:

```text
ProcessItemUseCase
```

через dependency layer и запускает:

```text
execute(barcode)
```

---

## Processing Flow

Концептуальный pipeline:

```text
Item
 ↓
Scanning
 ↓
Routing
 ↓
Conveyor
 ↓
Sensor
 ↓
Sorter
 ↓
OutputBin
```

Маршрут определяется на основе зарегистрированного Route.

---

## Process Response

Response содержит сокращённое состояние обработанного Item:

```json
{
  "id": 1,
  "barcode": "ITEM-0001",
  "status": "SORTED",
  "destination": 5,
  "location": "OutputBin 5"
}
```

### Status Code

При успешной обработке:

```text
200 OK
```

---

## Process Item Errors

Если Item не найден:

```text
404 Not Found
```

Если возникает ошибка persistence layer:

```text
500 Internal Server Error
```

---

# Processing Events

## GET /items/{barcode}/events

Возвращает историю событий обработки товара.

### Request

```http
GET /items/ITEM-0001/events
```

Перед получением событий API сначала проверяет существование Item.

---

## Processing Event Response

```json
[
  {
    "id": 1,
    "item_id": 1,
    "event_type": "CREATED",
    "location": "RECEIVING",
    "created_at": "2026-11-11T12:00:00"
  },
  {
    "id": 2,
    "item_id": 1,
    "event_type": "SORTED",
    "location": "OutputBin 5",
    "created_at": "2026-11-11T12:00:01"
  }
]
```

### Event Fields

```text
id
item_id
event_type
location
created_at
```

### Status Code

```text
200 OK
```

Если Item не найден:

```text
404 Not Found
```

---

# Pydantic Schemas

## DestinationCreate

```text
code: int > 0
name: non-empty string
```

---

## DestinationActiveUpdate

```text
is_active: bool
```

---

## DestinationResponse

```text
id: int
code: int
name: str
is_active: bool
```

---

## RouteCreate

```text
barcode: non-empty string
destination_code: int > 0
```

---

## RouteActiveUpdate

```text
is_active: bool
```

---

## RouteResponse

```text
id: int
barcode: str
destination_id: int
is_active: bool
created_at: datetime
```

---

## ItemCreate

```text
barcode: str
weight: Decimal
width: int
height: int
length: int
category: str
delivery_type: str
status: ItemStatus
location: str
destination_code: int | null
```

---

## ItemStateUpdate

```text
status: ItemStatus
location: str
```

---

## ItemResponse

```text
id: int
barcode: str
weight: Decimal
width: int
height: int
length: int
category: str
delivery_type: str
is_flammable: bool
status: str
destination_id: int | null
location: str
created_at: datetime
```

---

## ItemProcessResponse

```text
id: int
barcode: str
status: str
destination: int | null
location: str
```

---

## ProcessingEventResponse

```text
id: int
item_id: int
event_type: str
location: str
created_at: datetime
```

---

# HTTP Status Codes

Основные status codes API:

| Status | Meaning |
|---|---|
| `200 OK` | запрос успешно выполнен |
| `201 Created` | ресурс успешно создан |
| `404 Not Found` | ресурс не найден |
| `409 Conflict` | ресурс с таким уникальным значением уже существует |
| `422 Unprocessable Entity` | request не прошёл Pydantic/FastAPI validation |
| `500 Internal Server Error` | ошибка внутренней обработки или persistence |

---

# Validation Errors

FastAPI автоматически выполняет validation через Pydantic.

Например, следующий запрос некорректен:

```json
{
  "code": -1,
  "name": ""
}
```

потому что:

```text
code > 0
name must not be empty
```

В таком случае FastAPI возвращает:

```text
422 Unprocessable Entity
```

---

# Typical API Workflow

Типичный сценарий использования API:

## 1. Create Destination

```http
POST /destinations
```

```json
{
  "code": 5,
  "name": "Output Zone 5"
}
```

---

## 2. Create Route

```http
POST /routes
```

```json
{
  "barcode": "ITEM-0001",
  "destination_code": 5
}
```

---

## 3. Create Item

```http
POST /items
```

```json
{
  "barcode": "ITEM-0001",
  "weight": 2.5,
  "width": 20,
  "height": 10,
  "length": 30,
  "category": "electronics",
  "delivery_type": "standard",
  "status": "CREATED",
  "location": "RECEIVING"
}
```

---

## 4. Process Item

```http
POST /items/ITEM-0001/process
```

Expected final state:

```json
{
  "id": 1,
  "barcode": "ITEM-0001",
  "status": "SORTED",
  "destination": 5,
  "location": "OutputBin 5"
}
```

---

## 5. Read Item

```http
GET /items/ITEM-0001
```

---

## 6. Read Processing History

```http
GET /items/ITEM-0001/events
```

Этот endpoint позволяет проверить историю обработки товара.

---

# cURL Examples

## Health Check

```bash
curl http://localhost:8000/health
```

---

## Create Destination

```bash
curl -X POST http://localhost:8000/destinations \
  -H "Content-Type: application/json" \
  -d '{
    "code": 5,
    "name": "Output Zone 5"
  }'
```

---

## Create Route

```bash
curl -X POST http://localhost:8000/routes \
  -H "Content-Type: application/json" \
  -d '{
    "barcode": "ITEM-0001",
    "destination_code": 5
  }'
```

---

## Create Item

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

## Process Item

```bash
curl -X POST \
  http://localhost:8000/items/ITEM-0001/process
```

---

## Read Item

```bash
curl http://localhost:8000/items/ITEM-0001
```

---

## Read Item Events

```bash
curl http://localhost:8000/items/ITEM-0001/events
```

---

# Endpoint Summary

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | API health check |
| GET | `/destinations` | list destinations |
| GET | `/destinations/{code}` | get destination |
| POST | `/destinations` | create destination |
| PATCH | `/destinations/{code}` | enable/disable destination |
| GET | `/routes` | list routes |
| GET | `/routes/{barcode}` | get route |
| POST | `/routes` | create route |
| PATCH | `/routes/{barcode}` | enable/disable route |
| GET | `/items` | list items |
| GET | `/items/{barcode}` | get item |
| POST | `/items` | create item |
| PATCH | `/items/{barcode}` | update item state |
| POST | `/items/{barcode}/process` | process item |
| GET | `/items/{barcode}/events` | get processing history |

---

# API Design Goals

API layer проекта построен вокруг следующих принципов:

- typed request and response models;
- Pydantic validation;
- explicit HTTP status codes;
- separation of HTTP and business logic;
- reusable application use cases;
- persistence outside route handlers where orchestration requires it;
- automatic OpenAPI documentation;
- predictable error responses;
- testable endpoints.

API является внешним интерфейсом к backend-системе Warehouse Sorter и использует существующую application/domain логику вместо отдельной реализации бизнес-процессов.
````