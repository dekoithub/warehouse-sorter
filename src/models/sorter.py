import logging

from models.enums import SorterStatus
from models.exceptions import (
    EquipmentUnavailableError,
    UnsupportedDirectionError,
)
from models.item import Item


logger = logging.getLogger(__name__)


class Sorter:
    def __init__(
        self,
        sorter_id: int,
        supported_directions: list[int],
        is_available: bool,
    ) -> None:

        if sorter_id <= 0:
            raise ValueError("Sorter id must be greater than 0")

        if not supported_directions:
            raise ValueError("Supported directions cannot be empty")

        if any(direction <= 0 for direction in supported_directions):
            raise ValueError("Supported directions must be greater than 0")

        if len(supported_directions) != len(set(supported_directions)):
            raise ValueError("Supported directions must be unique")
    
        self.sorter_id = sorter_id
        self.status = (
            SorterStatus.IDLE
            if is_available
            else SorterStatus.UNAVAILABLE
        )
        self.current_direction: int | None = None
        self.supported_directions = supported_directions

    @property
    def is_available(self) -> bool:
        return self.status == SorterStatus.IDLE


    def enable(self) -> None:
        self.status = SorterStatus.IDLE

        logger.info(
            "Sorter %s enabled",
            self.sorter_id,
        )

    def disable(self) -> None:
        self.status = SorterStatus.UNAVAILABLE

        logger.info(
            "Sorter %s disabled",
            self.sorter_id,
        )

    def sort_item(
        self,
        item: Item,
        direction: int,
    ) -> Item:
        self._change_direction(direction)

        return item

    def _change_direction(self, direction: int) -> None:
        if not self.is_available:
            raise EquipmentUnavailableError(
                f"Sorter {self.sorter_id} is unavailable"
            )

        if direction not in self.supported_directions:
            raise UnsupportedDirectionError(
                f"Direction {direction} is not supported"
            )

        self.current_direction = direction

        logger.debug(
            "Sorter %s changed direction to %s",
            self.sorter_id,
            direction,
        )

    def mark_error(self) -> None:
        self.status = SorterStatus.ERROR

        logger.error(
            "Sorter %s entered error state",
            self.sorter_id,
        )