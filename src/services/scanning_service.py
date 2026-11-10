import logging

from models.enums import ItemStatus
from models.item import Item
from models.scanner import Scanner

logger = logging.getLogger(__name__)


class ScanningService:
    def __init__(
        self,
        scanner: Scanner,
    ) -> None:
        self._scanner = scanner

    def start_scan(
        self,
        item: Item,
    ) -> None:
        # Mark the item as currently being scanned.
        # Отмечаем, что товар сейчас проходит сканирование.
        item.change_status(ItemStatus.SCANNING)

    def complete_scan(
        self,
        item: Item,
    ) -> str | None:
        # Perform the physical scanner operation.
        # Выполняем операцию физического сканера.
        barcode = self._scanner.scan(item)

        if barcode is None:
            return None

        logger.info(
            "Item %s scanned successfully: barcode %s",
            item.id,
            barcode,
        )

        item.change_status(ItemStatus.ROUTING)

        return barcode

    def scan_item(
        self,
        item: Item,
    ) -> str | None:
        # Keep the synchronous API for the application layer.
        # Сохраняем синхронный API для прикладного слоя.
        self.start_scan(item)
        return self.complete_scan(item)
