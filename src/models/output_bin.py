from models.enums import OutputBinStatus
from models.item import Item


class OutputBin:
    def __init__(
        self,
        bin_id: int,
        capacity: int,
    ) -> None:
        if bin_id <= 0:
            raise ValueError("Output bin id must be greater than 0")

        if capacity <= 0:
            raise ValueError("Output bin capacity must be greater than 0")

        self.bin_id = bin_id
        self.capacity = capacity
        self._items: list[Item] = []

    @property
    def current_load(self) -> int:
        return len(self._items)

    @property
    def is_full(self) -> bool:
        return self.current_load >= self.capacity

    @property
    def status(self) -> OutputBinStatus:
        if not self._items:
            return OutputBinStatus.EMPTY

        if self.is_full:
            return OutputBinStatus.FULL

        return OutputBinStatus.OCCUPIED

    def add_item(self, item: Item) -> bool:
        if not self.is_available():
            return False

        self._items.append(item)
        return True

    def remove_all_items(self) -> None:
        self._items.clear()

    def is_available(self) -> bool:
        return not self.is_full
