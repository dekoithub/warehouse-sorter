import pytest

from models.enums import ItemStatus
from models.item import Item


def test_item_initial_data(item):
    # Verify the initial state prepared by the shared fixture
    # Проверяем начальное состояние, подготовленное общей фикстурой
    assert item.id == 1
    assert item.barcode == "4601234567890"
    assert item.status == ItemStatus.CREATED
    assert isinstance(item.status, ItemStatus)
    assert item.destination is None
    assert item.location == "Scanner"


def test_item_state_changes(item):
    # Change the Item state through its public methods
    # Изменяем состояние Item через его публичные методы
    item.change_status(ItemStatus.MOVING)
    item.set_destination(5)
    item.update_location("Conveyor 1")

    # Verify the resulting state
    # Проверяем итоговое состояние
    assert item.status == ItemStatus.MOVING
    assert item.destination == 5
    assert item.location == "Conveyor 1"


@pytest.mark.parametrize(
    ("field", "invalid_value"),
    [
        ("id", 0),
        ("weight", 0),
        ("width", 0),
        ("height", 0),
        ("length", 0),
        ("destination", 0),
        ("barcode", ""),
        ("category", ""),
        ("delivery_type", ""),
        ("location", ""),
    ],
)
def test_item_rejects_invalid_data(
    valid_item_data,
    field,
    invalid_value,
):
    data = valid_item_data.copy()
    data[field] = invalid_value

    with pytest.raises(ValueError):
        Item(**data)


def test_item_rejects_invalid_destination_update(item):
    # Destination must remain valid after Item creation
    # Destination должен оставаться корректным после создания Item
    with pytest.raises(ValueError):
        item.set_destination(0)


def test_item_rejects_empty_location_update(item):
    # Location cannot become empty after Item creation
    # Location не может стать пустой после создания Item
    with pytest.raises(ValueError):
        item.update_location("")
