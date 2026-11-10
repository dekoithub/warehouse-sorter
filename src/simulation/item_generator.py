from collections.abc import Callable, Generator

import simpy

from models.enums import ItemStatus
from models.item import Item


class ItemGenerator:
    def __init__(
        self,
        environment: simpy.Environment,
        interval_seconds: float,
        on_item: Callable[[Item], None],
    ) -> None:
        if interval_seconds <= 0:
            raise ValueError("Item interval must be greater than 0")

        self._environment = environment
        self._interval_seconds = interval_seconds
        self._on_item = on_item
        self._next_item_id = 1

    def run(
        self,
    ) -> Generator[simpy.events.Timeout]:
        while True:
            item = self._create_item(
                self._next_item_id,
            )
            self._next_item_id += 1

            self._on_item(item)

            # Wait until the next item enters the system.
            # Ждём виртуальное время до поступления следующего товара.
            yield self._environment.timeout(self._interval_seconds)

    @staticmethod
    def _create_item(item_id: int) -> Item:
        return Item(
            id=item_id,
            barcode=f"SIM-{item_id:012d}",
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
