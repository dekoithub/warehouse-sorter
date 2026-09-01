from models.enums import SensorStatus

from models.item import Item


class Sensor:
    def __init__(
        self,
        sensor_id: int,
        position: str,
        is_active: bool,
    ):

        if sensor_id <= 0:
            raise ValueError("Sensor id must be greater than 0")

        if not position:
            raise ValueError("Sensor position cannot be empty")

        self.sensor_id = sensor_id
        self.position = position
        self.is_active = is_active
        self.detection_count = 0
        self.status = (
            SensorStatus.ACTIVE
            if is_active
            else SensorStatus.INACTIVE
        )

    def detect_item(self, item: Item) -> bool:
        if not self.is_active:
            return False

        self.detection_count += 1
        return True

    def send_signal(
        self, 
        item: Item
    )-> dict[str, int | str] | None:
        if not self.is_active:
            return None

        return {
            "sensor_id": self.sensor_id,
            "item_id": item.id,
            "position": self.position,
        }

    def report_status(self) -> SensorStatus:
        return self.status

    def report_error(self) -> str:
        self.status = SensorStatus.ERROR
        self.is_active = False
        return "Sensor error"