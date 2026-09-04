from dataclasses import dataclass


@dataclass(frozen=True)
class SensorEvent:
    sensor_id: int
    item_id: int
    position: str
