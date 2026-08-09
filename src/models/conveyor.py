from models.item import Item

class Conveyor:
    def __init__(
            self,
            conveyor_id: int,
            speed: float,
            capacity: int,
            is_available: bool,
    ):
        self.conveyor_id = conveyor_id
        self.speed = speed
        self.capacity = capacity
        self.items: list[Item] = []
        self.status = "STOPPED"
        self.is_available = is_available

    def accept_item(self, item: Item):
        if len(self.items) >= self.capacity:
            return False

        self.items.append(item)
        return True

    def move_items(self):
        return self.items

    def release_item(self):
        if not self.items:
            return None

        return self.items.pop(0)

    def change_speed(self, new_speed: float):
        self.speed = new_speed

    def stop(self):
        self.status = "STOPPED"
        self.speed = 0

    def start(self):
        self.status = "RUNNING"

    def report_status(self):
        return self.status

    