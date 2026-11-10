import logging

from models.enums import SensorStatus
from models.events import SensorEvent
from models.item import Item

logger = logging.getLogger(__name__)


class Sensor:
    def __init__(
        self,
        sensor_id: int,
        position: str,
        is_active: bool,
    ) -> None:

        if sensor_id <= 0:
            raise ValueError("Sensor id must be greater than 0")

        if not position:
            raise ValueError("Sensor position cannot be empty")

        self.sensor_id = sensor_id
        self.position = position
        self.detection_count = 0
        self.status = SensorStatus.ACTIVE if is_active else SensorStatus.INACTIVE

    @property
    def is_active(self) -> bool:
        return self.status == SensorStatus.ACTIVE

    def activate(self) -> None:
        self.status = SensorStatus.ACTIVE

        logger.info(
            "Sensor %s activated",
            self.sensor_id,
        )

    def deactivate(self) -> None:
        self.status = SensorStatus.INACTIVE

        logger.info(
            "Sensor %s deactivated",
            self.sensor_id,
        )

    def detect_item(
        self,
        item: Item,
    ) -> SensorEvent | None:
        if not self.is_active:
            logger.warning(
                "Sensor %s cannot detect item %s: status=%s",
                self.sensor_id,
                item.id,
                self.status,
            )
            return None

        self.detection_count += 1

        return SensorEvent(
            sensor_id=self.sensor_id,
            item_id=item.id,
            position=self.position,
        )

    def mark_error(self) -> None:
        self.status = SensorStatus.ERROR

        logger.error(
            "Sensor %s entered error state",
            self.sensor_id,
        )
