from models.wms import WMS


def test_wms_returns_registered_destination():
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


def test_wms_returns_none_for_unknown_barcode():
    # Create an available WMS without the requested barcode
    # Создаем доступную WMS без запрашиваемого штрихкода
    wms = WMS(
        routes={},
        available_destinations=[1, 2, 3, 4, 5],
        is_available=True,
    )

    destination = wms.get_destination("9999999999999")

    assert destination is None
    assert wms.request_count == 1


def test_wms_returns_none_when_unavailable():
    # Create an unavailable WMS with an existing route
    # Создаем недоступную WMS с существующим маршрутом
    wms = WMS(
        routes={"4601234567890": 5},
        available_destinations=[1, 2, 3, 4, 5],
        is_available=False,
    )

    destination = wms.get_destination("4601234567890")

    assert destination is None
    assert wms.request_count == 1