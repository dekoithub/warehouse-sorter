import copy

import pytest

from models.buffer import Buffer
from models.enums import BufferStatus
from models.exceptions import BufferFullError


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
    buffer_id,
    capacity,
):
    with pytest.raises(ValueError):
        Buffer(
            buffer_id=buffer_id,
            capacity=capacity,
        )


def test_buffer_raises_error_when_full(item):
    buffer = Buffer(
        buffer_id=1,
        capacity=1,
    )

    buffer.add_item(item)

    with pytest.raises(BufferFullError):
        buffer.add_item(item)


def test_buffer_state_management(item):
    # Create an empty Buffer
    # Создаем пустой Buffer
    buffer = Buffer(
        buffer_id=1,
        capacity=2,
    )

    assert buffer.status == BufferStatus.EMPTY
    assert buffer.is_full is False

    # Add the first Item
    # Добавляем первый Item
    buffer.add_item(item)

    assert buffer.status == BufferStatus.OCCUPIED
    assert buffer.is_full is False

    # Add the second Item
    # Добавляем второй Item
    second_item = copy.deepcopy(item)
    buffer.add_item(second_item)

    assert buffer.status == BufferStatus.FULL
    assert buffer.is_full is True

    # Release one Item
    # Освобождаем один Item
    buffer.release_item()

    assert buffer.status == BufferStatus.OCCUPIED
    assert buffer.is_full is False

    # Simulate a Buffer error
    # Имитируем ошибку Buffer
    buffer.mark_error()

    assert buffer.status == BufferStatus.ERROR
    assert buffer.is_available() is False
