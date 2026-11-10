from collections.abc import Generator

import simpy

from application.controller import Controller
from models.item import Item
from models.sensor import Sensor
from models.sorter import Sorter


class SorterStation:
    def __init__(
        self,
        environment: simpy.Environment,
        controller: Controller,
        sensor: Sensor,
        sorter: Sorter,
        sort_duration_seconds: float,
        capacity: int = 1,
    ) -> None:
        if sort_duration_seconds <= 0:
            raise ValueError(
                "Sort duration must be greater than 0"
            )

        if capacity <= 0:
            raise ValueError(
                "Sorter capacity must be greater than 0"
            )

        self._environment = environment
        self._controller = controller
        self._sensor = sensor
        self._sorter = sorter
        self._sort_duration_seconds = sort_duration_seconds

        # Represents parallel sorter processing slots.
        # Представляет параллельные каналы обработки сортировщика.
        self._resource = simpy.Resource(
            environment,
            capacity=capacity,
        )

    @property
    def queue_length(self) -> int:
        return len(self._resource.queue)

    @property
    def in_use(self) -> int:
        return len(self._resource.users)

    def process(
        self,
        item: Item,
    ) -> Generator[simpy.events.Event, None, Item | None]:
        # Wait until one sorter processing slot becomes available.
        # Ждём освобождения одного канала сортировщика.
        with self._resource.request() as request:
            yield request

            item.update_location(self._sensor.position)

            sensor_event = self._sensor.detect_item(item)

            if sensor_event is None:
                self._controller.send_to_manual_processing(item)
                return None

            # Simulate physical sorting time.
            # Имитируем физическое время сортировки.
            yield self._environment.timeout(
                self._sort_duration_seconds
            )

            return self._controller.process_sorter_event(
                sensor_event,
                item,
                self._sorter,
            )