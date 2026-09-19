from application.controller import Controller
from application.ports.item_store import ItemStore
from models.enums import ItemStatus
from models.item import Item
from models.sensor import Sensor
from models.sorter import Sorter


class ItemNotFoundError(Exception):
    pass


class ItemPersistenceError(Exception):
    pass


class ProcessItemUseCase:
    def __init__(
        self,
        controller: Controller,
        item_store: ItemStore,
        sorter_sensor: Sensor,
        sorter: Sorter,
    ) -> None:
        self._controller = controller
        self._item_store = item_store
        self._sorter_sensor = sorter_sensor
        self._sorter = sorter

    def execute(
        self,
        barcode: str,
    ) -> Item:
        item = self._item_store.get_by_barcode(barcode)

        if item is None:
            raise ItemNotFoundError(f"Item with barcode {barcode} not found")

        self._controller.register_item(item)

        scanned_barcode = self._controller.scanning_service.scan_item(item)

        if scanned_barcode is None:
            self._controller.handle_scan_error(item)
            self._save_item(item)
            return item

        self._controller.route_item(item)

        if item.status != ItemStatus.MOVING:
            self._save_item(item)
            return item

        released_item = None

        for conveyor in self._controller.conveyors:
            if item not in conveyor.items:
                continue

            released_item = conveyor.release_item()

            if not conveyor.items:
                conveyor.stop()

            break

        if released_item is None:
            self._controller.send_to_manual_processing(item)
            self._save_item(item)
            return item

        released_item.update_location("Sorter Sensor")

        sorter_event = self._sorter_sensor.detect_item(released_item)

        if sorter_event is None:
            self._controller.send_to_manual_processing(released_item)
            self._save_item(released_item)
            return released_item

        self._controller.process_sorter_event(
            sorter_event,
            released_item,
            self._sorter,
        )

        self._save_item(released_item)

        return released_item

    def _save_item(
        self,
        item: Item,
    ) -> None:
        if not self._item_store.save(item):
            raise ItemPersistenceError(
                f"Failed to save item with barcode {item.barcode}"
            )
