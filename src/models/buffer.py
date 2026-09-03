import logging

from models.enums import BufferStatus
from models.exceptions import BufferFullError
from models.item import Item


logger = logging.getLogger(__name__)


class Buffer:
    def __init__(
        self,
        buffer_id: int,
        capacity: int,
    ) -> None:
        if buffer_id <= 0:
            raise ValueError("Buffer id must be greater than 0")

        if capacity <= 0:
            raise ValueError("Buffer capacity must be greater than 0")

        self.buffer_id = buffer_id
        self.capacity = capacity
        self.items: list[Item] = []
        self._has_error = False

    @property
    def is_full(self) -> bool:
        return len(self.items) >= self.capacity

    @property
    def status(self) -> BufferStatus:
        if self._has_error:
            return BufferStatus.ERROR

        if not self.items:
            return BufferStatus.EMPTY

        if self.is_full:
            return BufferStatus.FULL

        return BufferStatus.OCCUPIED

    def add_item(self, item: Item) -> bool:
        if self.is_full:
            raise BufferFullError(
                f"Buffer {self.buffer_id} is full"
            )

        if not self.is_available():
            return False

        self.items.append(item)
        return True

    def release_item(self) -> Item | None:
        if not self.items:
            return None

        return self.items.pop(0)

    def is_available(self) -> bool:
        return not self._has_error and not self.is_full

    def report_status(self) -> BufferStatus:
        return self.status

    def report_error(self) -> str:
        self._has_error = True

        logger.error(
            "Buffer %s entered error state",
            self.buffer_id,
        )

        return "Buffer error"