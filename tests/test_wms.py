import pytest

from models.exceptions import (
    EquipmentUnavailableError,
    RouteNotFoundError,
)
from models.wms import WMS


def test_wms_returns_registered_destination() -> None:
    # Create an available WMS with one known route
    # Создаем доступную WMS с одним известным маршрутом
    wms = WMS(
        routes={"4601234567890": 5},
        available_destinations=[1, 2, 3, 4, 5],
        is_available=True,
    )

    destination = wms.get_destination("4601234567890")

    assert destination == 5
    assert wms.request_count == 1


def test_wms_raises_error_for_unknown_barcode() -> None:
    wms = WMS(
        routes={},
        available_destinations=[1, 2, 3, 4, 5],
        is_available=True,
    )

    with pytest.raises(RouteNotFoundError):
        wms.get_destination("9999999999999")

    assert wms.request_count == 1


def test_wms_raises_error_when_unavailable() -> None:
    wms = WMS(
        routes={"4601234567890": 5},
        available_destinations=[1, 2, 3, 4, 5],
        is_available=False,
    )

    with pytest.raises(EquipmentUnavailableError):
        wms.get_destination("4601234567890")

    assert wms.request_count == 1


def test_wms_rejects_invalid_initial_route() -> None:
    with pytest.raises(ValueError):
        WMS(
            routes={"4601234567890": 99},
            available_destinations=[1, 2, 3, 4, 5],
            is_available=True,
        )


@pytest.mark.parametrize(
    "available_destinations",
    [
        [],
        [0],
        [-1, 2, 3],
    ],
)
def test_wms_rejects_invalid_destinations(
    available_destinations: list[int],
) -> None:
    with pytest.raises(ValueError):
        WMS(
            routes={},
            available_destinations=available_destinations,
            is_available=True,
        )


@pytest.mark.parametrize(
    ("barcode", "destination"),
    [
        ("", 1),
        ("4601234567890", 99),
    ],
)
def test_wms_rejects_invalid_route(
    barcode: str,
    destination: int,
) -> None:
    wms = WMS(
        routes={},
        available_destinations=[1, 2, 3, 4, 5],
        is_available=True,
    )

    with pytest.raises(ValueError):
        wms.register_route(barcode, destination)
