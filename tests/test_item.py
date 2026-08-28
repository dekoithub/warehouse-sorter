from models.enums import ItemStatus


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