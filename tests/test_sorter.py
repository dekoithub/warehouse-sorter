import pytest

from models.enums import SorterStatus
from models.exceptions import (
    EquipmentUnavailableError,
    UnsupportedDirectionError,
)
from models.item import Item
from models.sorter import Sorter


def assert_sorter_state(
    sorter: Sorter,
    expected_status: SorterStatus,
    expected_available: bool,
) -> None:
    assert sorter.status == expected_status
    assert sorter.is_available is expected_available


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
    sorter_id: int,
    supported_directions: list[int],
) -> None:
    with pytest.raises(ValueError):
        Sorter(
            sorter_id=sorter_id,
            supported_directions=supported_directions,
            is_available=True,
        )


def test_sorter_raises_error_for_unsupported_direction(
    item: Item,
) -> None:
    sorter = Sorter(
        sorter_id=1,
        supported_directions=[1, 2, 3, 4, 5],
        is_available=True,
    )

    with pytest.raises(UnsupportedDirectionError):
        sorter.sort_item(item, 99)


def test_sorter_raises_error_when_unavailable(
    item: Item,
) -> None:
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


def test_sorter_state_management() -> None:
    # Create an available Sorter
    # Создаем доступный Sorter
    sorter = Sorter(
        sorter_id=1,
        supported_directions=[1, 2, 3, 4, 5],
        is_available=True,
    )

    # Verify the initial state
    # Проверяем начальное состояние
    assert_sorter_state(
        sorter,
        SorterStatus.IDLE,
        True,
    )

    # Disable the Sorter
    # Отключаем Sorter
    sorter.disable()

    assert_sorter_state(
        sorter,
        SorterStatus.UNAVAILABLE,
        False,
    )

    # Enable the Sorter again
    # Снова включаем Sorter
    sorter.enable()

    assert_sorter_state(
        sorter,
        SorterStatus.IDLE,
        True,
    )

    # Simulate a Sorter error
    # Имитируем ошибку Sorter
    sorter.mark_error()

    assert_sorter_state(
        sorter,
        SorterStatus.ERROR,
        False,
    )
