from models.item import Item
from models.scanner import Scanner
from models.wms import WMS
from models.conveyor import Conveyor
from models.buffer import Buffer
from models.statistics import Statistics
from models.output_bin import OutputBin


class Controller:
    def __init__(
            self,
            scanner: Scanner,
            wms: WMS,
    ):
        self.scanner = scanner
        self.wms = wms

        self.conveyors: list[Conveyor] = []
        self.buffers: list[Buffer] = []
        self.output_bins: list[OutputBin] = []

        self.statistics: Statistics | None = None

    def register_item(self, item: Item):
        return item

    def request_route(self, barcode: str):
        destination = self.wms.get_destination(barcode)

        if destination is None:
            return None

        if not self.wms.is_destination_available(destination):
            return None

        return destination

    def route_item(self, item: Item):
        destination = self.request_route(item.barcode)

        if destination is None:
            if self.statistics is not None:
                self.statistics.register_routing_error()

            self.send_to_manual_processing(item)

            return None

        item.set_destination(destination)

        for conveyor in self.conveyors:
            if conveyor.accept_item(item):
                conveyor.start()

                item.change_status("MOVING")
                item.update_location(
                    f"Conveyor {conveyor.conveyor_id}"
                )

                return destination

        if self.send_to_buffer(item):
            return destination

        return None

    def handle_scan_error(self, item: Item):
        if self.statistics is not None:
            self.statistics.register_scan_error()

        item.change_status("ERROR")
        self.send_to_manual_processing(item)

        return None

    def send_to_buffer(self, item: Item):
        for buffer in self.buffers:
            if buffer.add_item(item):
                item.change_status("BUFFERED")
                item.update_location(
                    f"Buffer {buffer.buffer_id}"
                )

                if self.statistics is not None:
                    self.statistics.register_buffer_usage()

                return True

        return False

    def send_to_manual_processing(self, item: Item):
        item.change_status("MANUAL_PROCESSING")
        item.update_location("Manual Processing")

        return True

    def update_statistics(self):
        if self.statistics is None:
            return None

        return self.statistics.generate_report()

    def process_sensor_event(self, sensor_event: dict, item: Item):
        if sensor_event is None:
            return None

        if sensor_event["item_id"] != item.id:
            return None

        if not self.scanner.detect_item():
            return None

        item.change_status("SCANNING")

        barcode = self.scanner.scan(item)

        if barcode is None:
            return self.handle_scan_error(item)

        barcode = self.scanner.send_result(barcode)

        item.change_status("ROUTING")

        return self.route_item(item)
    