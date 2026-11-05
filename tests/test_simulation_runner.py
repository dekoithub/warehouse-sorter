import pytest

from models.enums import ItemStatus
from simulation.config import SimulationConfig
from simulation.runner import SimulationRunner


def test_simulation_runner_advances_virtual_time() -> None:
    config = SimulationConfig(
        duration_seconds=60.0,
    )
    runner = SimulationRunner(config)

    report = runner.run()

    assert runner.environment.now == 60.0
    assert report["simulation_time"] == 60.0


def test_simulation_config_rejects_invalid_duration() -> None:
    with pytest.raises(
        ValueError,
        match="Simulation duration must be greater than 0",
    ):
        SimulationConfig(
            duration_seconds=0,
        )


def test_simulation_runner_generates_and_scans_items() -> None:
    config = SimulationConfig(
        duration_seconds=3.0,
        item_interval_seconds=1.0,
        scan_duration_seconds=0.25,
        scanner_capacity=1,
    )

    runner = SimulationRunner(config)

    runner.run()

    assert len(runner.generated_items) == 3

    assert all(item.status == ItemStatus.MOVING for item in runner.generated_items)

    assert runner.scanner_station.in_use == 0
    assert runner.scanner_station.queue_length == 0


def test_simulation_runner_builds_scanner_queue_under_load() -> None:
    config = SimulationConfig(
        duration_seconds=1.5,
        item_interval_seconds=0.1,
        scan_duration_seconds=1.0,
        scanner_capacity=1,
    )

    runner = SimulationRunner(config)

    runner.run()

    assert len(runner.generated_items) > 1
    assert runner.scanner_station.in_use == 1
    assert runner.scanner_station.queue_length > 0


def test_simulation_report_contains_scanner_metrics() -> None:
    config = SimulationConfig(
        duration_seconds=1.5,
        item_interval_seconds=0.1,
        scan_duration_seconds=1.0,
        scanner_capacity=1,
    )

    runner = SimulationRunner(config)

    report = runner.run()

    generated_items = report["generated_items"]
    scanner_current_queue = report["scanner_current_queue"]
    scanner_in_use = report["scanner_in_use"]
    scanner_max_queue = report["scanner_max_queue"]
    scanner_average_wait = report["scanner_average_wait_seconds"]

    assert isinstance(generated_items, int)
    assert isinstance(scanner_current_queue, int)
    assert isinstance(scanner_in_use, int)
    assert isinstance(scanner_max_queue, int)
    assert isinstance(scanner_average_wait, float)

    assert generated_items > 1
    assert scanner_current_queue > 0
    assert scanner_in_use == 1
    assert scanner_max_queue > 0
    assert scanner_average_wait >= 0


def test_simulation_processes_item_end_to_end() -> None:
    config = SimulationConfig(
        duration_seconds=2.0,
        item_interval_seconds=10.0,
        scan_duration_seconds=0.1,
        scanner_capacity=1,
        conveyor_length_meters=1.0,
        conveyor_speed_mps=2.0,
        conveyor_capacity=1,
        default_destination=5,
        sorter_duration_seconds=0.1,
        output_bin_capacity=10,
    )

    runner = SimulationRunner(config)

    runner.run()

    assert len(runner.generated_items) == 1

    item = runner.generated_items[0]

    assert item.destination == 5
    assert item.status == ItemStatus.SORTED
    assert item.location == "OutputBin 5"

    assert runner.conveyor_station.in_use == 0
    assert runner.conveyor_station.queue_length == 0

    assert runner.sorter_station.in_use == 0
    assert runner.sorter_station.queue_length == 0

    assert runner.output_bin.current_load == 1


def test_simulation_sends_items_to_buffer_when_conveyor_is_full() -> None:
    config = SimulationConfig(
        duration_seconds=0.5,
        item_interval_seconds=0.1,
        scan_duration_seconds=0.01,
        scanner_capacity=1,
        conveyor_length_meters=10.0,
        conveyor_speed_mps=1.0,
        conveyor_capacity=1,
        buffer_capacity=10,
        default_destination=1,
        sorter_duration_seconds=0.1,
        output_bin_capacity=100,
    )

    runner = SimulationRunner(config)

    runner.run()

    assert runner.statistics.buffer_usage > 0
    assert len(runner.buffer.items) > 0

    assert any(item.status == ItemStatus.BUFFERED for item in runner.generated_items)


def test_simulation_sends_item_to_manual_processing_on_scan_error() -> None:
    config = SimulationConfig(
        duration_seconds=1.0,
        item_interval_seconds=10.0,
        scan_duration_seconds=0.1,
        scanner_capacity=1,
        scanner_error_rate=1.0,
    )

    runner = SimulationRunner(config)

    runner.run()

    assert len(runner.generated_items) == 1

    item = runner.generated_items[0]

    assert item.status == ItemStatus.MANUAL_PROCESSING
    assert item.location == "Manual Processing"

    assert runner.statistics.scan_errors == 1
    assert runner.statistics.manual_processing_items == 1


def test_simulation_sends_item_to_manual_processing_when_buffer_is_full() -> None:
    config = SimulationConfig(
        duration_seconds=0.35,
        item_interval_seconds=0.1,
        scan_duration_seconds=0.01,
        scanner_capacity=1,
        scanner_error_rate=0.0,
        conveyor_length_meters=10.0,
        conveyor_speed_mps=1.0,
        conveyor_capacity=1,
        buffer_capacity=1,
        buffer_retry_interval_seconds=0.01,
        default_destination=1,
        sorter_duration_seconds=0.1,
        output_bin_capacity=100,
    )

    runner = SimulationRunner(config)

    runner.run()

    assert len(runner.generated_items) >= 3

    assert runner.statistics.buffer_usage >= 1
    assert runner.statistics.manual_processing_items >= 1

    assert any(
        item.status == ItemStatus.MANUAL_PROCESSING for item in runner.generated_items
    )
