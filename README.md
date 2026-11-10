# Warehouse Sorter

A backend system and discrete-event simulation of an automated warehouse sorting center.

The project models the complete lifecycle of an item inside a sorting center: scanning, route resolution through WMS, conveyor transportation, temporary buffering, sorting, and delivery to an output bin.

The project combines a production-oriented Python backend with a SimPy simulation layer that makes it possible to model load, identify infrastructure bottlenecks, and validate system scalability.

---

## Key Features

- item lifecycle management;
- barcode scanning;
- route resolution through WMS;
- conveyor transportation;
- buffering when the conveyor is temporarily unavailable;
- automatic retry from the buffer;
- automated sorting;
- manual processing fallback;
- output bin management;
- processing statistics;
- PostgreSQL persistence;
- database migrations with Alembic;
- REST API with FastAPI;
- Docker and Docker Compose;
- discrete-event simulation with SimPy;
- high-load simulation;
- support for hundreds of sorting destinations;
- automated CI with GitHub Actions.

---

## Simulation Performance

The simulation layer is used to model a high-load warehouse sorting center.

The tested configuration supports approximately:

- **100,000 incoming items per hour**;
- **400 sorting destinations**;
- multiple parallel scanner channels;
- parallel sorter processing;
- conveyor capacity modelling;
- buffering;
- routing to output bins;
- virtual warehouse time.

### Load Test Result

Virtual simulation duration:

```text
600 seconds
```

Result:

```text
Generated items:              16,667
Sorted items:                 16,523

Incoming rate:                ~100,002 items/hour
Sorted throughput:            ~99,138 items/hour

Scanner queue:                0
Conveyor queue:               0
Sorter queue:                 0

Buffer:                       0
Manual Processing:            0

Routing errors:               0
Scan errors:                  0
```

The remaining items were still inside the processing pipeline when the virtual simulation time ended.

---

## 400 Sorting Destinations

The number of sorting destinations is configurable:

```python
destination_count=400
```

With this configuration, the system automatically creates:

```text
Destination 1
Destination 2
Destination 3
...
Destination 400
```

Each destination has its own `OutputBin`.

The route for each item is resolved through WMS, after which the Sorter directs the item to the corresponding output bin.

### Load Distribution

During the 400-destination test:

```text
OutputBin 1–123   → 42 items
OutputBin 124–400 → 41 items
```

Total:

```text
16,523 sorted items
400 destinations
```

---

## Project Architecture

The project is divided into several responsibility layers:

- API;
- Application Layer;
- Domain Models;
- Services;
- Infrastructure;
- Simulation.

### Structure

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

## Item Processing Pipeline

Normal item flow:

```text
Item
  ↓
Scanner
  ↓
WMS
  ↓
Route Resolution
  ↓
Conveyor
  ↓
Sensor
  ↓
Sorter
  ↓
OutputBin
```

If the Conveyor is temporarily overloaded:

```text
Conveyor unavailable
        ↓
      Buffer
        ↓
      Retry
        ↓
     Conveyor
```

If the item cannot be processed automatically:

```text
Processing Error
      ↓
Manual Processing
```

---

## Item Statuses

The system uses the following item states:

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

They make it possible to track the item lifecycle at every processing stage.

---

## Technology Stack

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

### Testing and Code Quality

- Pytest
- Mypy
- Ruff

### Infrastructure

- Docker
- Docker Compose
- GitHub Actions

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd warehouse-sorter
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows using Git Bash:

```bash
source .venv/Scripts/activate
```

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

---

## Code Quality Checks

### Pytest

```bash
python -m pytest
```

### Ruff

```bash
python -m ruff check src tests
```

Automatic fixes:

```bash
python -m ruff check src tests --fix
```

Formatting:

```bash
python -m ruff format src tests
```

### Mypy

```bash
python -m mypy src tests
```

---

## Running the Simulation

```bash
python -m simulation.main
```

The main simulation configuration is located in:

```text
src/simulation/config.py
```

---

## Simulation Configuration

The following parameters can be configured:

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

### High-Load Configuration Example

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

## Simulation Metrics

The final simulation report contains:

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

These metrics make it possible to identify bottlenecks and validate whether the equipment configuration is suitable for the target load.

---

## Bottleneck Analysis

During load testing, the system was scaled step by step.

### Scanner

The Scanner was the first bottleneck.

With a single scanning channel, the incoming item queue started growing rapidly.

After increasing:

```python
scanner_capacity=3
```

the Scanner queue disappeared.

### Conveyor

The Conveyor became the next bottleneck.

After calculating the number of items that needed to be transported simultaneously, the conveyor capacity was increased:

```python
conveyor_capacity=150
```

### Sorter

After removing the Conveyor limitation, the queue moved to the Sorter.

The Sorter was scaled to:

```python
sorter_capacity=3
```

### OutputBin

After increasing Sorter throughput, the OutputBin capacity became the next limitation.

For the load scenario it was increased to:

```python
output_bin_capacity=20000
```

### Final Result

After scaling the system components, the simulation was able to sustain approximately:

```text
100,000 items/hour
```

without:

```text
Scanner queue
Conveyor queue
Sorter queue
Buffer overflow
Manual Processing
Routing errors
Scan errors
```

under the validated load-test configuration.

---

## Docker

### Build

```bash
BUILDX_BAKE_ENTITLEMENTS_FS=0 docker compose build
```

### Run

```bash
docker compose up
```

The containerized environment includes:

- FastAPI;
- PostgreSQL;
- health checks;
- automatic Alembic migrations.

---

## PostgreSQL

PostgreSQL is used for persistent data storage.

Database stack:

```text
SQLAlchemy 2
Psycopg
Alembic
PostgreSQL
```

---

## Alembic

Apply migrations:

```bash
alembic upgrade head
```

Create a new migration:

```bash
alembic revision --autogenerate -m "migration description"
```

---

## FastAPI

The project provides a REST API for interacting with the warehouse sorting system.

The backend architecture is separated into:

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

API documentation is available through Swagger UI.

---

## GitHub Actions / CI

The project uses automated CI through GitHub Actions.

The workflow runs on:

```text
push
pull_request
```

Pipeline:

```text
Checkout Repository
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

If any check fails, the CI job is marked as unsuccessful.

---

## Testing

Tests cover:

- Domain Models;
- Controller;
- Services;
- Buffer;
- Conveyor;
- Scanner;
- Sensor;
- Sorter;
- OutputBin;
- routing;
- error handling;
- database integration;
- API;
- SimPy simulation;
- scanner queues;
- conveyor load;
- buffer overflow;
- manual processing;
- multiple destinations;
- 400-destination configuration.

---

## Error Handling

The project uses custom business-logic exceptions.

Handled scenarios include:

```text
equipment unavailable
route not found
unsupported direction
Buffer full
OutputBin full
OutputBin not found
scanning error
```

Problematic items can be redirected to:

```text
Manual Processing
```

without stopping the entire system.

---

## Project Goals

The project is designed not as a simple CRUD application, but as a production-oriented backend and system-design project.

Main goals:

- model a realistic warehouse domain;
- separate responsibilities between application layers;
- use strict Python typing;
- implement automated tests;
- work with PostgreSQL;
- use database migrations;
- provide a REST API;
- containerize the application;
- model physical warehouse equipment;
- use discrete-event simulation;
- perform load testing;
- identify bottlenecks;
- validate scalability;
- automate code-quality checks through CI.

---

## Implemented

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
- ~100,000 items/hour
- 400 sorting destinations
- GitHub Actions CI

---

## Current Status

The main backend functionality and simulation layer are implemented.

The system has been validated under a simulated load of approximately:

```text
~100,000 items/hour
```

with:

```text
400 sorting destinations
```

The project is currently in its final stage:

```text
Documentation
      ↓
Final Packaging
      ↓
Portfolio-Ready Release
```

---

## Author

**Denis Korchitskiy**

Python Backend Developer

GitHub:

```text
https://github.com/dekoithub
```
````