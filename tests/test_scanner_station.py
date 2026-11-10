import simpy

from models.enums import ItemStatus
from models.item import Item
from models.scanner import Scanner
from services.scanning_service import ScanningService
from simulation.stations.scanner_station import ScannerStation


def assert_item_status(
    item: Item,
    expected_status: ItemStatus,
) -> None:
    assert item.status == expected_status


def make_item(
    item_id: int,
) -> Item:
    return Item(
        id=item_id,
        barcode=f"SIM-{item_id}",
        weight=1.0,
        width=100,
        height=100,
        length=100,
        category="Simulation",
        delivery_type="Standard",
        is_flammable=False,
        status=ItemStatus.CREATED,
        destination=None,
        location="Scanner",
    )


def test_scanner_station_processes_items_sequentially() -> None:
    environment = simpy.Environment()

    scanner = Scanner(
        scanner_id=1,
        is_active=True,
        error_rate=0.0,
    )

    scanning_service = ScanningService(scanner)

    station = ScannerStation(
        environment=environment,
        scanning_service=scanning_service,
        scan_duration_seconds=1.0,
        capacity=1,
    )

    first_item = make_item(1)
    second_item = make_item(2)

    environment.process(station.process(first_item))
    environment.process(station.process(second_item))

    environment.run(until=0.5)

    assert_item_status(
        first_item,
        ItemStatus.SCANNING,
    )
    assert_item_status(
        second_item,
        ItemStatus.CREATED,
    )

    assert station.in_use == 1
    assert station.queue_length == 1

    environment.run(until=1.5)

    assert first_item.status == ItemStatus.ROUTING
    assert second_item.status == ItemStatus.SCANNING

    environment.run(until=2.1)

    assert_item_status(
        second_item,
        ItemStatus.ROUTING,
    )
    assert scanner.scan_count == 2
    assert station.in_use == 0
    assert station.queue_length == 0


def test_scanner_station_tracks_queue_metrics() -> None:
    environment = simpy.Environment()

    scanner = Scanner(
        scanner_id=1,
        is_active=True,
        error_rate=0.0,
    )

    scanning_service = ScanningService(scanner)

    station = ScannerStation(
        environment=environment,
        scanning_service=scanning_service,
        scan_duration_seconds=1.0,
        capacity=1,
    )

    first_item = make_item(1)
    second_item = make_item(2)
    third_item = make_item(3)

    environment.process(station.process(first_item))
    environment.process(station.process(second_item))
    environment.process(station.process(third_item))

    environment.run(until=3.1)

    assert station.wait_times == (
        0.0,
        1.0,
        2.0,
    )
    assert station.average_wait_time_seconds == 1.0
    assert station.max_queue_length == 2
