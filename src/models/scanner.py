import random

from models.item import Item

class Scanner:
    def __init__(
        self,
        scanner_id: int,
        is_active: bool,
        error_rate: float,
    ) -> None:
        self.scanner_id = scanner_id
        self.is_active = is_active
        self.error_rate = error_rate
        self.scan_count = 0

    def detect_item(self) -> bool:
        return self.is_active

    def scan(self, item: Item) -> str | None:
        if not self.is_active:
            return None
        
        self.scan_count += 1

        if random.random() < self.error_rate:
            return None
        
        return item.barcode

    def send_result(self, barcode: str | None) -> str | None:
        return barcode

    def report_error(self) -> str:
        return "Scanner error"

    