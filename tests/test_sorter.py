import pytest

from models.exceptions import (
    EquipmentUnavailableError,
    UnsupportedDirectionError,
)
from models.sorter import Sorter
from models.enums import SorterStatus


@pytest.mark.parametrize(
    ("sorter_id", "supported_directions"),
    [
        (0, [1, 2, 3]),
        (-1, [1, 2, 3]),
        (1, []),
        (1, [0, 1, 2]),
        (1, [-1, 1, 2]),
        (1, [1, 2, 2]),
    ],
)
def test_sorter_rejects_invalid_data(
    sorter_id,
    supported_directions,
):
    with pytest.raises(ValueError):
        Sorter(
            sorter_id=sorter_id,
            supported_directions=supported_directions,
            is_available=True,
        )

def test_sorter_raises_error_for_unsupported_direction(item):
    sorter = Sorter(
        sorter_id=1,
        supported_directions=[1, 2, 3, 4, 5],
        is_available=True,
    )

    with pytest.raises(UnsupportedDirectionError):
        sorter.sort_item(item, 99)

def test_sorter_raises_error_when_unavailable(item):
    # Create an unavailable Sorter
    # Создаем недоступный Sorter
    sorter = Sorter(
        sorter_id=1,
        supported_directions=[1, 2, 3, 4, 5],
        is_available=False,
    )

    # Sorting must fail when Sorter is unavailable
    # Сортировка должна завершиться ошибкой, если Sorter недоступен
    with pytest.raises(EquipmentUnavailableError):
        sorter.sort_item(item, 5)

def test_sorter_state_management():
    # Create an available Sorter
    # Создаем доступный Sorter
    sorter = Sorter(
        sorter_id=1,
        supported_directions=[1, 2, 3, 4, 5],
        is_available=True,
    )

    # Verify the initial state
    # Проверяем начальное состояние
    assert sorter.status == SorterStatus.IDLE
    assert sorter.is_available is True

    # Disable the Sorter
    # Отключаем Sorter
    sorter.disable()

    assert sorter.status == SorterStatus.UNAVAILABLE
    assert sorter.is_available is False

    # Enable the Sorter again
    # Снова включаем Sorter
    sorter.enable()

    assert sorter.status == SorterStatus.IDLE
    assert sorter.is_available is True

    # Simulate a Sorter error
    # Имитируем ошибку Sorter
    sorter.mark_error()

    assert sorter.status == SorterStatus.ERROR
    assert sorter.is_available is False