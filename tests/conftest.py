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