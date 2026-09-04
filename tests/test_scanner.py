import pytest

from models.item import Item
from models.scanner import Scanner


def test_scanner_successful_scan(
    item: Item,
) -> None:
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


def test_scanner_scan_error(
    item: Item,
) -> None:
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


@pytest.mark.parametrize(
    ("scanner_id", "error_rate"),
    [
        (0, 0.0),
        (-1, 0.0),
        (1, -0.1),
        (1, 1.1),
    ],
)
def test_scanner_rejects_invalid_data(
    scanner_id: int,
    error_rate: float,
) -> None:
    with pytest.raises(ValueError):
        Scanner(
            scanner_id=scanner_id,
            is_active=True,
            error_rate=error_rate,
        )