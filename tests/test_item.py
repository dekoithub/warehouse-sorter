from models.item import Item


def test_item_initial_data():
    # Create a controlled Item instance for checking its initial state
    # Создаем контролируемый объект Item для проверки его начального состояния
    item = Item(
        id=1,
        barcode="4601234567890",
        weight=2.4,
        width=250,
        height=150,
        length=300,
        category="Electronics",
        delivery_type="Courier",
        is_flammable=False,
        status="CREATED",
        destination=None,
        location="Scanner",
    )

    # Verify that constructor arguments were stored in the expected attributes
    # Проверяем, что аргументы конструктора сохранились в ожидаемых атрибутах
    assert item.id == 1
    assert item.barcode == "4601234567890"
    assert item.status == "CREATED"
    assert item.destination is None
    assert item.location == "Scanner"