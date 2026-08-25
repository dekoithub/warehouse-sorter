from models.scanner import Scanner


def test_scanner_successful_scan(item):
    # Create an active scanner with guaranteed successful scanning
    # Создаем активный сканер с гарантированно успешным сканированием
    scanner = Scanner(
        scanner_id=1,
        is_active=True,
        error_rate=0.0,
    )

    barcode = scanner.scan(item)

    assert barcode == item.barcode
    assert scanner.scan_count == 1

def test_scanner_scan_error(item):
    # Create a scanner with guaranteed scan failure
    # Создаем сканер с гарантированной ошибкой сканирования
    scanner = Scanner(
        scanner_id=1,
        is_active=True,
        error_rate=1.0,
    )

    barcode = scanner.scan(item)

    assert barcode is None
    assert scanner.scan_count == 1