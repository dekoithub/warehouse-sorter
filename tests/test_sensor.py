import pytest

from models.sensor import Sensor


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