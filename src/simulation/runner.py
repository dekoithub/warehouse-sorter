from collections.abc import Generator

import simpy

from application.controller import Controller
from models.buffer import Buffer
from models.conveyor import Conveyor
from models.item import Item
from models.output_bin import OutputBin
from models.scanner import Scanner
from models.sensor import Sensor
from models.sorter import Sorter
from models.statistics import Statistics
from models.wms import WMS
from services.scanning_service import ScanningService
from simulation.config import SimulationConfig
from simulation.item_generator import ItemGenerator
from simulation.report import SimulationReport
from simulation.stations.conveyor_station import ConveyorStation
from simulation.stations.scanner_station import ScannerStation
from simulation.stations.sorter_station import SorterStation


class SimulationRunner:
    def __init__(
        self,
        config: SimulationConfig,
    ) -> None:
        self.config = config
        self.environment = simpy.Environment()
        self.statistics = Statistics()

        self._generated_items: list[Item] = []

        scanner = Scanner(
            scanner_id=1,
            is_active=True,
            error_rate=config.scanner_error_rate,
        )

        self.destinations = list(
            range(
                config.default_destination,
                config.default_destination + config.destination_count,
            )
        )

        self._wms = WMS(
            routes={},
            available_destinations=self.destinations,
            is_available=True,
        )

        self.controller = Controller(
            scanner=scanner,
            wms=self._wms,
        )
        self.controller.statistics = self.statistics

        scanning_service = ScanningService(scanner)

        self.scanner_station = ScannerStation(
            environment=self.environment,
            scanning_service=scanning_service,
            scan_duration_seconds=config.scan_duration_seconds,
            capacity=config.scanner_capacity,
        )

        conveyor = Conveyor(
            conveyor_id=1,
            speed=config.conveyor_speed_mps,
            capacity=config.conveyor_capacity,
            is_available=True,
        )

        self.controller.register_conveyor(conveyor)

        self.buffer = Buffer(
            buffer_id=1,
            capacity=config.buffer_capacity,
        )

        self.controller.register_buffer(self.buffer)

        self.conveyor_station = ConveyorStation(
            environment=self.environment,
            conveyor=conveyor,
            length_meters=config.conveyor_length_meters,
        )

        sorter_sensor = Sensor(
            sensor_id=2,
            position="Sorter Sensor",
            is_active=True,
        )

        sorter = Sorter(
            sorter_id=1,
            supported_directions=self.destinations,
            is_available=True,
        )

        # Create one output bin for every sorting destination.
        # Создаём отдельный выходной накопитель для каждого направления.
        self.output_bins = [
            OutputBin(
                bin_id=destination,
                capacity=config.output_bin_capacity,
            )
            for destination in self.destinations
        ]

        for output_bin in self.output_bins:
            self.controller.register_output_bin(
                output_bin
            )

        # Temporary compatibility alias for existing tests and report.
        # Временный алиас для совместимости со старыми тестами и отчётом.
        self.output_bin = self.output_bins[0]

        self.controller.register_output_bin(self.output_bin)

        self.sorter_station = SorterStation(
            environment=self.environment,
            controller=self.controller,
            sensor=sorter_sensor,
            sorter=sorter,
            sort_duration_seconds=config.sorter_duration_seconds,
            capacity=config.sorter_capacity,
        )

        self.item_generator = ItemGenerator(
            environment=self.environment,
            interval_seconds=config.item_interval_seconds,
            on_item=self._handle_generated_item,
        )

    @property
    def generated_items(self) -> tuple[Item, ...]:
        return tuple(self._generated_items)

    def run(self) -> SimulationReport:
        # Start the continuous item arrival process.
        # Запускаем непрерывный процесс поступления товаров.
        self.environment.process(self.item_generator.run())

        # Start background buffer draining.
        # Запускаем фоновую обработку товаров из буфера.
        self.environment.process(self._drain_buffer())

        # Advance all scheduled simulation processes.
        # Выполняем события до конца виртуального времени.
        self.environment.run(until=self.config.duration_seconds)

        self.statistics.set_simulation_time(float(self.environment.now))

        # Capture final equipment loads.
        # Фиксируем загрузку оборудования в конце симуляции.
        self.controller.update_statistics()

        base_report = self.statistics.generate_report()

        simulation_time = float(self.environment.now)

        arrival_rate_items_per_second = (
            len(self._generated_items) / simulation_time if simulation_time > 0 else 0.0
        )

        sorted_throughput_items_per_second = (
            self.statistics.sorted_items / simulation_time
            if simulation_time > 0
            else 0.0
        )

        in_flight_items = (
            len(self._generated_items)
            - self.statistics.sorted_items
            - self.statistics.manual_processing_items
        )

        report: SimulationReport = {
            **base_report,
            "generated_items": len(self._generated_items),
            "scanner_current_queue": (self.scanner_station.queue_length),
            "scanner_in_use": self.scanner_station.in_use,
            "scanner_max_queue": (self.scanner_station.max_queue_length),
            "scanner_average_wait_seconds": (
                self.scanner_station.average_wait_time_seconds
            ),
            "conveyor_current_queue": (self.conveyor_station.queue_length),
            "conveyor_in_use": self.conveyor_station.in_use,
            "sorter_current_queue": (self.sorter_station.queue_length),
            "sorter_in_use": self.sorter_station.in_use,
            "buffer_current_load": len(self.buffer.items),
            "output_bin_current_load": sum(
                output_bin.current_load
                for output_bin in self.output_bins
            ),
            "arrival_rate_items_per_second": (arrival_rate_items_per_second),
            "arrival_rate_items_per_hour": (arrival_rate_items_per_second * 3600),
            "sorted_throughput_items_per_second": (sorted_throughput_items_per_second),
            "sorted_throughput_items_per_hour": (
                sorted_throughput_items_per_second * 3600
            ),
            "in_flight_items": in_flight_items,
        }

        return report

    def _handle_generated_item(
        self,
        item: Item,
    ) -> None:
        self._generated_items.append(item)

        # Distribute generated items evenly across available destinations.
        # Равномерно распределяем товары по доступным направлениям.
        destination_index = (
            (item.id - 1) % len(self.destinations)
        )

        destination = self.destinations[
            destination_index
        ]

        self._wms.register_route(
            item.barcode,
            destination,
        )

        self.environment.process(self._process_item(item))

    def _process_item(
        self,
        item: Item,
    ) -> Generator[simpy.events.Event]:
        self.controller.register_item(item)

        barcode = yield from self.scanner_station.process(item)

        if barcode is None:
            self.controller.handle_scan_error(item)
            return

        destination = self.controller.resolve_route(item)

        if destination is None:
            return

        if not self.conveyor_station.has_available_capacity:
            if not self.controller.send_to_buffer(item):
                self.controller.send_to_manual_processing(item)

            return

        transported_item = yield from (self.conveyor_station.process(item))

        yield from self.sorter_station.process(transported_item)

    def _drain_buffer(
        self,
    ) -> Generator[simpy.events.Event]:
        while True:
            if self.buffer.items and self.conveyor_station.has_available_capacity:
                item = self.controller.take_from_buffer(self.buffer)

                if item is not None:
                    self.environment.process(self._process_buffered_item(item))

            yield self.environment.timeout(self.config.buffer_retry_interval_seconds)

    def _process_buffered_item(
        self,
        item: Item,
    ) -> Generator[simpy.events.Event]:
        transported_item = yield from (self.conveyor_station.process(item))

        yield from self.sorter_station.process(transported_item)
