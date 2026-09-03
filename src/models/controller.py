import logging

from models.enums import ItemStatus
from models.exceptions import (
    BufferFullError,
    EquipmentUnavailableError,
    RouteNotFoundError,
    UnsupportedDirectionError,
)

from models.item import Item
from models.scanner import Scanner
from models.wms import WMS
from models.conveyor import Conveyor
from models.buffer import Buffer
from models.statistics import Statistics
from models.output_bin import OutputBin
from models.sorter import Sorter


logger = logging.getLogger(__name__)


class Controller:
    def __init__(
        self,
        scanner: Scanner,
        wms: WMS,
    ) -> None:
        self.scanner = scanner
        self.wms = wms
        self.conveyors: list[Conveyor] = []
        self.buffers: list[Buffer] = []
        self.output_bins: list[OutputBin] = []
        self.statistics: Statistics | None = None

    def register_item(self, item: Item) -> Item:
        if self.statistics is not None:
            self.statistics.register_processed_item()

        return item

    def request_route(self, barcode: str) -> int:
        return self.wms.get_destination(barcode)

    def route_item(self, item: Item) -> int | None:
        try:
            destination = self.request_route(item.barcode)

        except (EquipmentUnavailableError, RouteNotFoundError) as error:
            logger.warning(
                "Failed to route item %s: %s",
                item.id,
                error,
            )

            if self.statistics is not None:
                self.statistics.register_routing_error()

            self.send_to_manual_processing(item)

            return None

        item.set_destination(destination)

        logger.info(
            "Route found for item %s: destination %s",
            item.id,
            destination,
        )

        for conveyor in self.conveyors:
            try:
                accepted = conveyor.accept_item(item)

                if not accepted:
                    continue

                conveyor.start()

            except EquipmentUnavailableError as error:
                logger.warning("%s", error)
                continue

            item.change_status(ItemStatus.MOVING)
            item.update_location(f"Conveyor {conveyor.conveyor_id}")

            logger.info(
                "Item %s sent to Conveyor %s",
                item.id,
                conveyor.conveyor_id,
            )

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
        for buffer in self.buffers:
            try:
                added = buffer.add_item(item)

            except BufferFullError as error:
                logger.warning("%s", error)
                continue

            if added:
                item.change_status(ItemStatus.BUFFERED)
                item.update_location(f"Buffer {buffer.buffer_id}")

                logger.info(
                    "Item %s sent to Buffer %s",
                    item.id,
                    buffer.buffer_id,
                )

                if self.statistics is not None:
                    self.statistics.register_buffer_usage()

                return True

        return False

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
            self.statistics.conveyor_load[conveyor.conveyor_id] = len(conveyor.items)

        for output_bin in self.output_bins:
            self.statistics.output_bin_load[output_bin.bin_id] = output_bin.current_load

        return self.statistics.generate_report()

    def process_sensor_event(
        self,
        sensor_event: dict[str, int | str] | None,
        item: Item,
    ) -> int | None:
        if sensor_event is None:
            logger.warning(
                "Sensor event is missing for item %s",
                item.id,
            )
            return None
        
        if sensor_event["item_id"] != item.id:
            logger.warning(
                "Sensor event item mismatch: expected %s, received %s",
                item.id,
                sensor_event["item_id"],
            )
            return None

        if not self.scanner.detect_item():
            self.handle_scan_error(item)
            return None

        item.change_status(ItemStatus.SCANNING)

        barcode = self.scanner.scan(item)

        if barcode is None:
            self.handle_scan_error(item)
            return None

        logger.info(
            "Item %s scanned successfully: barcode %s",
            item.id,
            barcode,
        )

        item.change_status(ItemStatus.ROUTING)

        return self.route_item(item)

    def process_sorter_event(
        self,
        sensor_event: dict[str, int | str] | None,
        item: Item,
        sorter: Sorter,
    ) -> Item | None:
        if sensor_event is None:
            logger.warning(
                "Sorter sensor event is missing for item %s",
                item.id,
            )
            return None

        if sensor_event["item_id"] != item.id:
            logger.warning(
                "Sorter sensor item mismatch: expected %s, received %s",
                item.id,
                sensor_event["item_id"],
            )
            return None

        if item.destination is None:
            logger.warning(
                "Item %s has no destination",
                item.id,
            )

            self.send_to_manual_processing(item)
            return None

        try:
            sorted_item = sorter.sort_item(
                item,
                item.destination,
            )

        except UnsupportedDirectionError as error:
            logger.warning(
                "Failed to sort item %s: %s",
                item.id,
                error,
            )

            if self.statistics is not None:
                self.statistics.register_routing_error()

            self.send_to_manual_processing(item)
            return None

        except EquipmentUnavailableError as error:
            logger.warning("%s", error)

            if self.send_to_buffer(item):
                return None

            self.send_to_manual_processing(item)
            return None
        
        for output_bin in self.output_bins:
            if output_bin.bin_id != sorted_item.destination:
                continue

            if output_bin.add_item(sorted_item):
                sorted_item.change_status(ItemStatus.SORTED)
                sorted_item.update_location(
                    f"OutputBin {output_bin.bin_id}"
                )

                logger.info(
                    "Item %s sorted to OutputBin %s",
                    sorted_item.id,
                    output_bin.bin_id,
                )

                if self.statistics is not None:
                    self.statistics.register_sorted_item()

                return sorted_item

            logger.warning(
                "OutputBin %s cannot accept item %s",
                output_bin.bin_id,
                sorted_item.id,
            )

            if self.send_to_buffer(sorted_item):
                return None

            self.send_to_manual_processing(sorted_item)
            return None

        logger.warning(
            "No OutputBin found for item %s with destination %s",
            sorted_item.id,
            sorted_item.destination,
        )

        if self.statistics is not None:
            self.statistics.register_routing_error()

        self.send_to_manual_processing(sorted_item)

        return None
    
    def release_from_buffer(
        self,
        buffer: Buffer,
    ) -> Item | None:
        item = buffer.release_item()

        if item is None:
            return None

        logger.info(
            "Item %s released from Buffer %s",
            item.id,
            buffer.buffer_id,
        )

        for conveyor in self.conveyors:
            try:
                accepted = conveyor.accept_item(item)

                if not accepted:
                    continue

                conveyor.start()

            except EquipmentUnavailableError as error:
                logger.warning("%s", error)
                continue

            item.change_status(ItemStatus.MOVING)
            item.update_location(f"Conveyor {conveyor.conveyor_id}")

            logger.info(
                "Item %s moved from Buffer %s to Conveyor %s",
                item.id,
                buffer.buffer_id,
                conveyor.conveyor_id,
            )

            return item
        
        if buffer.add_item(item):
            item.change_status(ItemStatus.BUFFERED)
            item.update_location(f"Buffer {buffer.buffer_id}")

            logger.warning(
                "No Conveyor available for item %s; returned to Buffer %s",
                item.id,
                buffer.buffer_id,
            )

            return None

        self.send_to_manual_processing(item)

        return None