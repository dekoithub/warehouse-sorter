from collections.abc import Generator

import simpy

from models.item import Item
from services.scanning_service import ScanningService


class ScannerStation:
    def __init__(
        self,
        environment: simpy.Environment,
        scanning_service: ScanningService,
        scan_duration_seconds: float,
        capacity: int = 1,
    ) -> None:
        if scan_duration_seconds <= 0:
            raise ValueError("Scan duration must be greater than 0")

        if capacity <= 0:
            raise ValueError("Scanner capacity must be greater than 0")

        self._environment = environment
        self._scanning_service = scanning_service
        self._scan_duration_seconds = scan_duration_seconds

        self._resource = simpy.Resource(
            environment,
            capacity=capacity,
        )

        self._wait_times: list[float] = []
        self._max_queue_length = 0

    @property
    def queue_length(self) -> int:
        return len(self._resource.queue)

    @property
    def in_use(self) -> int:
        return len(self._resource.users)

    @property
    def wait_times(self) -> tuple[float, ...]:
        return tuple(self._wait_times)

    @property
    def average_wait_time_seconds(self) -> float:
        if not self._wait_times:
            return 0.0

        return sum(self._wait_times) / len(self._wait_times)

    @property
    def max_queue_length(self) -> int:
        return self._max_queue_length

    def process(
        self,
        item: Item,
    ) -> Generator[simpy.events.Event, None, str | None]:
        request_time = float(self._environment.now)

        # Wait until scanner capacity becomes available.
        # Ждём, пока освободится место на сканере.
        with self._resource.request() as request:
            self._max_queue_length = max(
                self._max_queue_length,
                self.queue_length,
            )

            yield request

            wait_time = float(self._environment.now) - request_time
            self._wait_times.append(wait_time)

            self._scanning_service.start_scan(item)

            # Simulate the physical scanning duration.
            # Моделируем физическое время сканирования товара.
            yield self._environment.timeout(self._scan_duration_seconds)

            return self._scanning_service.complete_scan(item)
