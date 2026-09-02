import pytest
from models.exceptions import BufferFullError

from models.buffer import Buffer


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