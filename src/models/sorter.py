from models.enums import SorterStatus
from models.exceptions import UnsupportedDirectionError

from models.item import Item


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
        self.status = SorterStatus.IDLE
        self.current_direction: int | None = None
        self.supported_directions = supported_directions
        self.is_available = is_available

    def accept_item(self, item: Item | None) -> bool:
        if not self.is_available:
            return False

        if item is None:
            return False

        return True

    def sort_item(
        self,
        item: Item | None,
        direction: int,
    ) -> Item | None:
        if not self.is_available:
            return None

        if item is None:
            return None

        if not self.change_direction(direction):
            return None

        return item

    def send_item(self, item: Item | None) -> Item | None:
        if not self.is_available:
            return None

        if item is None:
            return None

        return item

    def change_direction(self, direction: int) -> bool:
        if not self.is_available:
            return False

        if direction not in self.supported_directions:
            raise UnsupportedDirectionError(
                f"Direction {direction} is not supported"
            )

        self.current_direction = direction
        return True

    def report_status(self) -> SorterStatus:
        return self.status

    def report_error(self) -> str:
        self.status = SorterStatus.ERROR
        self.is_available = False
        return "Sorter error"