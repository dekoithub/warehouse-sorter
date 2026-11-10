import simpy

from models.enums import ItemStatus
from models.item import Item
from simulation.item_generator import ItemGenerator


def test_item_generator_creates_items_over_time() -> None:
    environment = simpy.Environment()
    generated_items: list[Item] = []

    generator = ItemGenerator(
        environment=environment,
        interval_seconds=1.0,
        on_item=generated_items.append,
    )

    environment.process(generator.run())
    environment.run(until=3.0)

    assert len(generated_items) == 3

    assert generated_items[0].id == 1
    assert generated_items[1].id == 2
    assert generated_items[2].id == 3


def test_generated_item_uses_domain_item() -> None:
    environment = simpy.Environment()
    generated_items: list[Item] = []

    generator = ItemGenerator(
        environment=environment,
        interval_seconds=1.0,
        on_item=generated_items.append,
    )

    environment.process(generator.run())
    environment.run(until=1.0)

    item = generated_items[0]

    assert isinstance(item, Item)
    assert item.barcode == "SIM-000000000001"
    assert item.status == ItemStatus.CREATED
    assert item.destination is None
    assert item.location == "Scanner"
