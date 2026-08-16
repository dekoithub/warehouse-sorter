from models.item import Item


class Buffer:
    def __init__(
        self,
        buffer_id: int,
        capacity: int,
    ):
        self.buffer_id = buffer_id
        self.capacity = capacity
        self.items: list[Item] = []
        self.status = "EMPTY"
        self.is_full = False

    def add_item(self, item: Item):
        if not self.is_available():
            return False

        self.items.append(item)

        if len(self.items) >= self.capacity:
            self.is_full = True
            self.status = "FULL"
        else:
            self.status = "OCCUPIED"

        return True

    def release_item(self):
        if not self.items:
            return None

        item = self.items.pop(0)
        self.is_full = False

        if self.items:
            self.status = "OCCUPIED"
        else:
            self.status = "EMPTY"

        return item

    def is_available(self):
        return len(self.items) < self.capacity

    def report_status(self):
        return self.status

    def report_error(self):
        self.status = "ERROR"
        return "Buffer error"