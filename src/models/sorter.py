from models.item import Item

class Sorter:
    def __init__(
        self,
        sorter_id: int,
        supported_directions: list[int],
        is_available: bool,
    ):
        self.sorter_id = sorter_id
        self.status = "IDLE"
        self.current_direction = None
        self.supported_directions = supported_directions
        self.is_available = is_available

    def accept_item(self, item: Item):
        if not self.is_available:
            return False

        return True

    def sort_item(self, item: Item, directiom: int):
        if not self.change_direction(directiom):
            return False

        return item

    def send_item(self, item: Item):
        return item

    def change_direction(self, direction: int):
        if direction not in self.supported_directions:
            return False

        self.current_direction = direction
        return True

    def report_status(self):
        return self.status

    def report_error(self):
        self.status = "ERROR"
        return "Sorter error"