class Scanner:
    def __init__(self, scanner_id, is_active, error_rate):
        self.scanner_id = scanner_id
        self.is_active = is_active
        self.error_rate = error_rate
        self.scan_count = 0

    def detect_item(self):
        return self.is_active

    def scan(self, item):
        self.scan_count += 1
        return item.barcode

    def send_result(self, barcode):
        return barcode

    def report_error(self):
        return "Scanner error"

    