import pytest

from models.sensor import Sensor
from models.enums import SensorStatus


@pytest.mark.parametrize(
    ("sensor_id", "position"),
    [
        (0, "Scanner"),
        (-1, "Scanner"),
        (1, ""),
    ],
)
def test_sensor_rejects_invalid_data(
    sensor_id,
    position,
):
    with pytest.raises(ValueError):
        Sensor(
            sensor_id=sensor_id,
            position=position,
            is_active=True,
        )

def test_sensor_state_management():
    # Create an active Sensor
    # Создаем активный Sensor
    sensor = Sensor(
        sensor_id=1,
        position="Scanner",
        is_active=True,
    )

    # Verify the initial state
    # Проверяем начальное состояние
    assert sensor.status == SensorStatus.ACTIVE
    assert sensor.is_active is True

    # Deactivate the Sensor
    # Деактивируем Sensor
    sensor.deactivate()

    assert sensor.status == SensorStatus.INACTIVE
    assert sensor.is_active is False

    # Activate the Sensor again
    # Снова активируем Sensor
    sensor.activate()

    assert sensor.status == SensorStatus.ACTIVE
    assert sensor.is_active is True

    # Simulate a Sensor error
    # Имитируем ошибку Sensor
    sensor.report_error()

    assert sensor.status == SensorStatus.ERROR
    assert sensor.is_active is False