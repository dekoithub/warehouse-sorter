import pytest

from models.enums import SensorStatus
from models.sensor import Sensor


def assert_sensor_state(
    sensor: Sensor,
    expected_status: SensorStatus,
    expected_active: bool,
) -> None:
    assert sensor.status == expected_status
    assert sensor.is_active is expected_active


@pytest.mark.parametrize(
    ("sensor_id", "position"),
    [
        (0, "Scanner"),
        (-1, "Scanner"),
        (1, ""),
    ],
)
def test_sensor_rejects_invalid_data(
    sensor_id: int,
    position: str,
) -> None:
    with pytest.raises(ValueError):
        Sensor(
            sensor_id=sensor_id,
            position=position,
            is_active=True,
        )


def test_sensor_state_management() -> None:
    # Create an active Sensor
    # Создаем активный Sensor
    sensor = Sensor(
        sensor_id=1,
        position="Scanner",
        is_active=True,
    )

    # Verify the initial state
    # Проверяем начальное состояние
    assert_sensor_state(
        sensor,
        SensorStatus.ACTIVE,
        True,
    )

    # Deactivate the Sensor
    # Деактивируем Sensor
    sensor.deactivate()

    assert_sensor_state(
        sensor,
        SensorStatus.INACTIVE,
        False,
    )

    # Activate the Sensor again
    # Снова активируем Sensor
    sensor.activate()

    assert_sensor_state(
        sensor,
        SensorStatus.ACTIVE,
        True,
    )

    # Simulate a Sensor error
    # Имитируем ошибку Sensor
    sensor.mark_error()

    assert_sensor_state(
        sensor,
        SensorStatus.ERROR,
        False,
    )
