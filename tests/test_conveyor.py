import pytest

from models.conveyor import Conveyor
from models.enums import ConveyorStatus


def assert_conveyor_state(
    conveyor: Conveyor,
    expected_status: ConveyorStatus,
    expected_available: bool,
) -> None:
    assert conveyor.status == expected_status
    assert conveyor.is_available is expected_available


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
    conveyor_id: int,
    speed: float,
    capacity: int,
) -> None:
    with pytest.raises(ValueError):
        Conveyor(
            conveyor_id=conveyor_id,
            speed=speed,
            capacity=capacity,
            is_available=True,
        )


def test_conveyor_rejects_invalid_speed_change() -> None:
    conveyor = Conveyor(
        conveyor_id=1,
        speed=1.5,
        capacity=2,
        is_available=True,
    )

    with pytest.raises(ValueError):
        conveyor.change_speed(0)


def test_conveyor_state_management() -> None:
    # Create an available stopped Conveyor
    # Создаем доступный остановленный Conveyor
    conveyor = Conveyor(
        conveyor_id=1,
        speed=1.5,
        capacity=2,
        is_available=True,
    )

    assert_conveyor_state(
        conveyor,
        ConveyorStatus.STOPPED,
        True,
    )

    # Start the Conveyor
    # Запускаем Conveyor
    conveyor.start()

    assert_conveyor_state(
        conveyor,
        ConveyorStatus.RUNNING,
        True,
    )

    # Stop the Conveyor
    # Останавливаем Conveyor
    conveyor.stop()

    assert_conveyor_state(
        conveyor,
        ConveyorStatus.STOPPED,
        True,
    )

    # Disable the Conveyor
    # Делаем Conveyor недоступным
    conveyor.disable()

    assert_conveyor_state(
        conveyor,
        ConveyorStatus.UNAVAILABLE,
        False,
    )

    # Enable the Conveyor again
    # Снова делаем Conveyor доступным
    conveyor.enable()

    assert_conveyor_state(
        conveyor,
        ConveyorStatus.STOPPED,
        True,
    )