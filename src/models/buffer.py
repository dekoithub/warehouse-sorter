from models.enums import BufferStatus
from models.exceptions import BufferFullError

from models.item import Item


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
        self.status = BufferStatus.EMPTY
        self.is_full = False

    def add_item(self, item: Item) -> bool:
        if len(self.items) >= self.capacity:
            raise BufferFullError(
                f"Buffer {self.buffer_id} is full"
            )

        if not self.is_available():
            return False

        self.items.append(item)

        if len(self.items) >= self.capacity:
            self.is_full = True
            self.status = BufferStatus.FULL
        else:
            self.status = BufferStatus.OCCUPIED

        return True

    def release_item(self) -> Item | None:
        if not self.items:
            return None

        item = self.items.pop(0)
        self.is_full = False

        if self.items:
            self.status = BufferStatus.OCCUPIED
        else:
            self.status = BufferStatus.EMPTY

        return item

    def is_available(self) -> bool:
        if self.status == BufferStatus.ERROR:
            return False

        return len(self.items) < self.capacity

    def report_status(self) -> BufferStatus:
        return self.status

    def report_error(self) -> str:
        self.status = BufferStatus.ERROR
        return "Buffer error"