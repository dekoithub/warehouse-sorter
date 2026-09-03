import pytest

from models.conveyor import Conveyor
from models.enums import ConveyorStatus


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

def test_conveyor_state_management():
    # Create an available stopped Conveyor
    # Создаем доступный остановленный Conveyor
    conveyor = Conveyor(
        conveyor_id=1,
        speed=1.5,
        capacity=2,
        is_available=True,
    )

    assert conveyor.status == ConveyorStatus.STOPPED
    assert conveyor.is_available is True

    # Start the Conveyor
    # Запускаем Conveyor
    conveyor.start()

    assert conveyor.status == ConveyorStatus.RUNNING
    assert conveyor.is_available is True

    # Stop the Conveyor
    # Останавливаем Conveyor
    conveyor.stop()

    assert conveyor.status == ConveyorStatus.STOPPED
    assert conveyor.is_available is True

    # Disable the Conveyor
    # Делаем Conveyor недоступным
    conveyor.disable()

    assert conveyor.status == ConveyorStatus.UNAVAILABLE
    assert conveyor.is_available is False

    # Enable the Conveyor again
    # Снова делаем Conveyor доступным
    conveyor.enable()

    assert conveyor.status == ConveyorStatus.STOPPED
    assert conveyor.is_available is True