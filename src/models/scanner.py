import random

from models.item import Item

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

    