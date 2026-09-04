import logging

from models.buffer import Buffer
from models.conveyor import Conveyor
from models.enums import ItemStatus
from models.exceptions import (
    EquipmentUnavailableError,
    OutputBinFullError,
    OutputBinNotFoundError,
    RouteNotFoundError,
    UnsupportedDirectionError,
)
from models.item import Item
from models.output_bin import OutputBin
from models.scanner import Scanner
from models.sorter import Sorter
from models.statistics import Statistics
from models.wms import WMS
from services.buffer_service import BufferService
from services.routing_service import RoutingService
from services.scanning_service import ScanningService
from services.sorting_service import SortingService

logger = logging.getLogger(__name__)


class Controller:
    def __init__(
        self,
        scanner: Scanner,
        wms: WMS,
    ) -> None:
        self.scanning_service = ScanningService(scanner)
        self.routing_service = RoutingService(wms)
        self.sorting_service = SortingService()
        self.conveyors: list[Conveyor] = []
        self.buffers: list[Buffer] = []
        self.buffer_service = BufferService(self.buffers)
        self.output_bins: list[OutputBin] = []
        self.statistics: Statistics | None = None

    def register_item(self, item: Item) -> Item:
        if self.statistics is not None:
            self.statistics.register_processed_item()

        return item

    def route_item(self, item: Item) -> int | None:
        try:
            destination = self.routing_service.request_route(item.barcode)

        except (EquipmentUnavailableError, RouteNotFoundError) as error:
            self._handle_routing_failure(
                item,
                error,
            )
            return None

        item.set_destination(destination)

        logger.info(
            "Route found for item %s: destination %s",
            item.id,
            destination,
        )

        conveyor = self.routing_service.send_to_conveyor(
            item,
            self.conveyors,
        )

        if conveyor is not None:
            return destination

        if self.send_to_buffer(item):
            return destination

        self.send_to_manual_processing(item)

        return None

    def handle_scan_error(self, item: Item) -> None:
        logger.warning(
            "Scan failed for item %s",
            item.id,
        )

        if self.statistics is not None:
            self.statistics.register_scan_error()

        item.change_status(ItemStatus.ERROR)
        self.send_to_manual_processing(item)

    def send_to_buffer(self, item: Item) -> bool:
        return self.buffer_service.send_to_buffer(
            item,
            self.statistics,
        )

    def send_to_manual_processing(self, item: Item) -> bool:
        if item.status == ItemStatus.MANUAL_PROCESSING:
            return True

        item.change_status(ItemStatus.MANUAL_PROCESSING)
        item.update_location("Manual Processing")

        logger.warning(
            "Item %s sent to manual processing",
            item.id,
        )

        if self.statistics is not None:
            self.statistics.register_manual_processing_item()

        return True

    def update_statistics(self) -> dict[str, object] | None:
        if self.statistics is None:
            return None

        for conveyor in self.conveyors:
            self.statistics.set_conveyor_load(
                conveyor.conveyor_id,
                len(conveyor.items),
            )

        for output_bin in self.output_bins:
            self.statistics.set_output_bin_load(
                output_bin.bin_id,
                output_bin.current_load,
            )

        return self.statistics.generate_report()

    def process_sensor_event(
        self,
        sensor_event: dict[str, int | str] | None,
        item: Item,
    ) -> int | None:
        if not self._validate_sensor_event(
            sensor_event,
            item,
            "Sensor",
        ):
            return None

        barcode = self.scanning_service.scan_item(item)

        if barcode is None:
            self.handle_scan_error(item)
            return None

        return self.route_item(item)

    def _validate_sensor_event(
        self,
        sensor_event: dict[str, int | str] | None,
        item: Item,
        source: str,
    ) -> bool:
        if sensor_event is None:
            logger.warning(
                "%s event is missing for item %s",
                source,
                item.id,
            )
            return False

        if sensor_event["item_id"] != item.id:
            logger.warning(
                "%s event item mismatch: expected %s, received %s",
                source,
                item.id,
                sensor_event["item_id"],
            )
            return False

        return True

    def _handle_routing_failure(
        self,
        item: Item,
        error: Exception,
    ) -> None:
        logger.warning(
            "Failed to route item %s: %s",
            item.id,
            error,
        )

        if self.statistics is not None:
            self.statistics.register_routing_error()

        self.send_to_manual_processing(item)

    def _handle_processing_failure(
        self,
        item: Item,
        error: Exception,
    ) -> None:
        logger.warning(
            "Failed to process item %s: %s",
            item.id,
            error,
        )

        if self.send_to_buffer(item):
            return

        self.send_to_manual_processing(item)

    def process_sorter_event(
        self,
        sensor_event: dict[str, int | str] | None,
        item: Item,
        sorter: Sorter,
    ) -> Item | None:
        if not self._validate_sensor_event(
            sensor_event,
            item,
            "Sorter sensor",
        ):
            return None

        if item.destination is None:
            logger.warning(
                "Item %s has no destination",
                item.id,
            )

            self.send_to_manual_processing(item)
            return None

        try:
            sorted_item = self.sorting_service.sort_to_output_bin(
                item,
                sorter,
                self.output_bins,
            )

        except (
            UnsupportedDirectionError,
            OutputBinNotFoundError,
        ) as error:
            self._handle_routing_failure(
                item,
                error,
            )
            return None

        except (
            EquipmentUnavailableError,
            OutputBinFullError,
        ) as error:
            self._handle_processing_failure(
                item,
                error,
            )
            return None

        if self.statistics is not None:
            self.statistics.register_sorted_item()

        return sorted_item

    def release_from_buffer(
        self,
        buffer: Buffer,
    ) -> Item | None:
        item = self.buffer_service.release_item(buffer)

        if item is None:
            return None

        conveyor = self.routing_service.send_to_conveyor(
            item,
            self.conveyors,
        )

        if conveyor is not None:
            logger.info(
                "Item %s moved from Buffer %s to Conveyor %s",
                item.id,
                buffer.buffer_id,
                conveyor.conveyor_id,
            )

            return item

        if self.buffer_service.return_to_buffer(
            item,
            buffer,
        ):
            return None

        self.send_to_manual_processing(item)

        return None
