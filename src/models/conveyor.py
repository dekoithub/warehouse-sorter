from models.enums import ConveyorStatus

from models.item import Item


class Conveyor:
    def __init__(
        self,
        conveyor_id: int,
        speed: float,
        capacity: int,
        is_available: bool,
    ) -> None:
        self.conveyor_id = conveyor_id
        self.speed = speed
        self.capacity = capacity
        self.items: list[Item] = []
        self.status = ConveyorStatus.STOPPED
        self.is_available = is_available

    def accept_item(self, item: Item) -> bool:
        if not self.is_available:
            return False 
        
        if len(self.items) >= self.capacity:
            return False

        self.items.append(item)
        return True

    def move_items(self) -> list[Item] | bool:
        if not self.is_available:
            return False

        if self.status != ConveyorStatus.RUNNING:
            return False

        return self.items

    def release_item(self) -> Item | None:
        if not self.items:
            return None

        return self.items.pop(0)

    def change_speed(self, new_speed: float) -> None:
        self.speed = new_speed

    def stop(self) -> bool:
        self.status = ConveyorStatus.STOPPED
        return True

    def start(self) -> bool:
        if not self.is_available:
            return False

        self.status = ConveyorStatus.RUNNING
        return True

    def report_status(self) -> ConveyorStatus:
        return self.status

    