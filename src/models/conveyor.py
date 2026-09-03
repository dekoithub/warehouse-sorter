import logging

from models.enums import ConveyorStatus
from models.exceptions import EquipmentUnavailableError
from models.item import Item


logger = logging.getLogger(__name__)


class Conveyor:
    def __init__(
        self,
        conveyor_id: int,
        speed: float,
        capacity: int,
        is_available: bool,
    ) -> None:
        if conveyor_id <= 0:
            raise ValueError("Conveyor id must be greater than 0")

        if speed <= 0:
            raise ValueError("Conveyor speed must be greater than 0")

        if capacity <= 0:
            raise ValueError("Conveyor capacity must be greater than 0")

        self.conveyor_id = conveyor_id
        self.speed = speed
        self.capacity = capacity
        self.items: list[Item] = []
        self.status = (
            ConveyorStatus.STOPPED
            if is_available
            else ConveyorStatus.UNAVAILABLE
        )

    @property
    def is_available(self) -> bool:
        return self.status != ConveyorStatus.UNAVAILABLE


    def enable(self) -> None:
        self.status = ConveyorStatus.STOPPED

        logger.info(
            "Conveyor %s enabled",
            self.conveyor_id,
        )

    def disable(self) -> None:
        self.status = ConveyorStatus.UNAVAILABLE

        logger.info(
            "Conveyor %s disabled",
            self.conveyor_id,
        )

    def accept_item(self, item: Item) -> bool:
        if not self.is_available:
            raise EquipmentUnavailableError(
                f"Conveyor {self.conveyor_id} is unavailable"
            )

        if len(self.items) >= self.capacity:
            return False

        self.items.append(item)
        return True

    def release_item(self) -> Item | None:
        if not self.items:
            return None

        return self.items.pop(0)

    def change_speed(self, new_speed: float) -> None:
        if new_speed <= 0:
            raise ValueError("Conveyor speed must be greater than 0")

        old_speed = self.speed
        self.speed = new_speed

        logger.info(
            "Conveyor %s speed changed from %s to %s",
            self.conveyor_id,
            old_speed,
            new_speed,
        )

    def stop(self) -> None:
        if not self.is_available:
            raise EquipmentUnavailableError(
                f"Conveyor {self.conveyor_id} is unavailable"
            )

        self.status = ConveyorStatus.STOPPED

        logger.debug(
            "Conveyor %s stopped",
            self.conveyor_id,
        )

    def start(self) -> None:
        if not self.is_available:
            raise EquipmentUnavailableError(
                f"Conveyor {self.conveyor_id} is unavailable"
            )

        self.status = ConveyorStatus.RUNNING

        logger.debug(
            "Conveyor %s started",
            self.conveyor_id,
        )