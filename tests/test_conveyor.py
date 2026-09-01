import pytest

from models.conveyor import Conveyor


@pytest.mark.parametrize(
    ("conveyor_id", "speed", "capacity"),
    [
        (0, 1.5, 2),
        (-1, 1.5, 2),
        (1, 0, 2),
        (1, -1.0, 2),
        (1, 1.5, 0),
        (1, 1.5, -1),
    ],
)
def test_conveyor_rejects_invalid_data(
    conveyor_id,
    speed,
    capacity,
):
    with pytest.raises(ValueError):
        Conveyor(
            conveyor_id=conveyor_id,
            speed=speed,
            capacity=capacity,
            is_available=True,
        )


def test_conveyor_rejects_invalid_speed_change():
    conveyor = Conveyor(
        conveyor_id=1,
        speed=1.5,
        capacity=2,
        is_available=True,
    )

    with pytest.raises(ValueError):
        conveyor.change_speed(0)