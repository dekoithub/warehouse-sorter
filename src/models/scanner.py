import logging
import random

from models.item import Item

logger = logging.getLogger(__name__)


class Scanner:
    def __init__(
        self,
        scanner_id: int,
        is_active: bool,
        error_rate: float,
    ) -> None:

        if scanner_id <= 0:
            raise ValueError("Scanner id must be greater than 0")

        if not 0 <= error_rate <= 1:
            raise ValueError("Error rate must be between 0 and 1")

        self.scanner_id = scanner_id
        self._is_active = is_active
        self.error_rate = error_rate
        self.scan_count = 0

    @property
    def is_active(self) -> bool:
        return self._is_active

    def activate(self) -> None:
        self._is_active = True
        logger.info(
            "Scanner %s activated",
            self.scanner_id,
        )

    def deactivate(self) -> None:
        self._is_active = False
        logger.info(
            "Scanner %s deactivated",
            self.scanner_id,
        )

    def scan(self, item: Item) -> str | None:
        if not self.is_active:
            return None

        self.scan_count += 1

        if random.random() < self.error_rate:
            return None

        return item.barcode
