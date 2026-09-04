import copy

import pytest

from models.buffer import Buffer
from models.enums import BufferStatus
from models.exceptions import BufferFullError
from models.item import Item


def assert_buffer_state(
    buffer: Buffer,
    expected_status: BufferStatus,
    expected_full: bool,
) -> None:
    assert buffer.status == expected_status
    assert buffer.is_full is expected_full


@pytest.mark.parametrize(
    ("buffer_id", "capacity"),
    [
        (0, 1),
        (-1, 1),
        (1, 0),
        (1, -1),
    ],
)
def test_buffer_rejects_invalid_data(
    buffer_id: int,
    capacity: int,
) -> None:
    with pytest.raises(ValueError):
        Buffer(
            buffer_id=buffer_id,
            capacity=capacity,
        )


def test_buffer_raises_error_when_full(
    item: Item,
) -> None:
    buffer = Buffer(
        buffer_id=1,
        capacity=1,
    )

    buffer.add_item(item)

    with pytest.raises(BufferFullError):
        buffer.add_item(item)


def test_buffer_state_management(
    item: Item,
) -> None:
    # Create an empty Buffer
    # Создаем пустой Buffer
    buffer = Buffer(
        buffer_id=1,
        capacity=2,
    )

    assert_buffer_state(
        buffer,
        BufferStatus.EMPTY,
        False,
    )

    # Add the first Item
    # Добавляем первый Item
    buffer.add_item(item)

    assert_buffer_state(
        buffer,
        BufferStatus.OCCUPIED,
        False,
    )

    # Add the second Item
    # Добавляем второй Item
    second_item = copy.deepcopy(item)
    buffer.add_item(second_item)

    assert_buffer_state(
        buffer,
        BufferStatus.FULL,
        True,
    )

    # Release one Item
    # Освобождаем один Item
    buffer.release_item()

    assert_buffer_state(
        buffer,
        BufferStatus.OCCUPIED,
        False,
    )

    # Simulate a Buffer error
    # Имитируем ошибку Buffer
    buffer.mark_error()

    assert_buffer_state(
        buffer,
        BufferStatus.ERROR,
        False,
    )
    assert buffer.is_available() is False