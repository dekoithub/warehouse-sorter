import pytest

from models.item import Item


@pytest.fixture
def item():
    # Create a reusable Item instance for tests
    # Создаем переиспользуемый экземпляр Item для тестов
    return Item(
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

def test_item_initial_data(item):
    # Verify that constructor arguments were stored in the expected attributes
    # Проверяем, что аргументы конструктора сохранились в ожидаемых атрибутах
    assert item.id == 1
    assert item.barcode == "4601234567890"
    assert item.status == "CREATED"
    assert item.destination is None
    assert item.location == "Scanner"

def test_item_state_changes(item):
    # Change the Item state through its public methods
    # Изменяем состояние Item через его публичные методы
    item.change_status("MOVING")
    item.set_destination(5)
    item.update_location("Conveyor 1")

    # Verify that every operation changed the expected attribute
    # Проверяем, что каждая операция изменила ожидаемый атрибут
    assert item.status == "MOVING"
    assert item.destination == 5
    assert item.location == "Conveyor 1"