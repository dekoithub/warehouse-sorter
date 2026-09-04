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

    def scan_item(
        self,
        item: Item,
    ) -> str | None:
        item.change_status(ItemStatus.SCANNING)

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