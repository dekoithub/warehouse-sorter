import pytest

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