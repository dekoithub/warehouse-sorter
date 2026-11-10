from application.controller import Controller
from application.use_cases.process_item import ProcessItemUseCase
from infrastructure.adapters.database_item_store import DatabaseItemStore
from infrastructure.adapters.database_route_provider import (
    DatabaseRouteProvider,
)
from infrastructure.repositories.destination_repository import (
    get_all_destinations,
)
from models.buffer import Buffer
from models.conveyor import Conveyor
from models.output_bin import OutputBin
from models.scanner import Scanner
from models.sensor import Sensor
from models.sorter import Sorter


def build_process_item_use_case() -> ProcessItemUseCase:
    route_provider = DatabaseRouteProvider()
    item_store = DatabaseItemStore()

    destinations = [
        destination for destination in get_all_destinations() if destination.is_active
    ]

    destination_codes = [destination.code for destination in destinations]

    if not destination_codes:
        raise RuntimeError("No active destinations available")

    scanner = Scanner(
        scanner_id=1,
        is_active=True,
        error_rate=0.0,
    )

    sorter_sensor = Sensor(
        sensor_id=2,
        position="Sorter Sensor",
        is_active=True,
    )

    conveyor = Conveyor(
        conveyor_id=1,
        speed=1.5,
        capacity=100,
        is_available=True,
    )

    buffer = Buffer(
        buffer_id=1,
        capacity=100,
    )

    sorter = Sorter(
        sorter_id=1,
        supported_directions=destination_codes,
        is_available=True,
    )

    controller = Controller(
        scanner=scanner,
        wms=route_provider,
    )

    controller.register_conveyor(conveyor)
    controller.register_buffer(buffer)

    for destination_code in destination_codes:
        controller.register_output_bin(
            OutputBin(
                bin_id=destination_code,
                capacity=100,
            )
        )

    return ProcessItemUseCase(
        controller=controller,
        item_store=item_store,
        sorter_sensor=sorter_sensor,
        sorter=sorter,
    )
