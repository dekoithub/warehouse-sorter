import simpy

from models.conveyor import Conveyor
from models.enums import ItemStatus
from models.item import Item
from simulation.stations.conveyor_station import ConveyorStation


def make_item(item_id: int) -> Item:
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
        status=ItemStatus.ROUTING,
        destination=1,
        location="Scanner",
    )


def test_conveyor_station_uses_speed_to_calculate_travel_time() -> None:
    environment = simpy.Environment()

    conveyor = Conveyor(
        conveyor_id=1,
        speed=2.0,
        capacity=10,
        is_available=True,
    )

    station = ConveyorStation(
        environment=environment,
        conveyor=conveyor,
        length_meters=10.0,
    )

    assert station.travel_time_seconds == 5.0


def test_conveyor_station_transports_item() -> None:
    environment = simpy.Environment()

    conveyor = Conveyor(
        conveyor_id=1,
        speed=2.0,
        capacity=10,
        is_available=True,
    )

    station = ConveyorStation(
        environment=environment,
        conveyor=conveyor,
        length_meters=10.0,
    )

    item = make_item(1)

    process = environment.process(station.process(item))

    environment.run(until=2.0)

    assert item.status == ItemStatus.MOVING
    assert item.location == "Conveyor 1"

    environment.run(until=5.1)

    assert process.triggered
    assert process.value is item
    assert conveyor.items == ()
    assert station.in_use == 0
