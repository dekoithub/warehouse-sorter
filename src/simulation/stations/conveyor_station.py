from collections.abc import Generator

import simpy

from models.conveyor import Conveyor
from models.enums import ItemStatus
from models.item import Item


class ConveyorStation:
    def __init__(
        self,
        environment: simpy.Environment,
        conveyor: Conveyor,
        length_meters: float,
    ) -> None:
        if length_meters <= 0:
            raise ValueError("Conveyor length must be greater than 0")

        self._environment = environment
        self._conveyor = conveyor
        self._length_meters = length_meters

        self._resource = simpy.Resource(
            environment,
            capacity=conveyor.capacity,
        )

    @property
    def travel_time_seconds(self) -> float:
        return self._length_meters / self._conveyor.speed

    @property
    def in_use(self) -> int:
        return len(self._resource.users)

    @property
    def queue_length(self) -> int:
        return len(self._resource.queue)

    @property
    def has_available_capacity(self) -> bool:
        return self.in_use < self._resource.capacity

    def process(
        self,
        item: Item,
    ) -> Generator[simpy.events.Event, None, Item]:
        # Wait for free conveyor capacity.
        # Ждём свободного места на конвейере.
        with self._resource.request() as request:
            yield request

            accepted = self._conveyor.accept_item(item)

            if not accepted:
                raise RuntimeError(
                    f"Conveyor {self._conveyor.conveyor_id} "
                    "rejected item despite available SimPy capacity"
                )

            self._conveyor.start()

            item.change_status(ItemStatus.MOVING)
            item.update_location(f"Conveyor {self._conveyor.conveyor_id}")

            # Simulate physical movement along the conveyor.
            # Моделируем физическое движение по конвейеру.
            yield self._environment.timeout(self.travel_time_seconds)

            released_item = self._conveyor.release_item()

            if released_item is None:
                raise RuntimeError(
                    f"Conveyor {self._conveyor.conveyor_id} released no item"
                )

            if not self._conveyor.items:
                self._conveyor.stop()

            return released_item
