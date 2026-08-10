from models.item import Item

class OutputBin:
    def __init__(
        self,
        bin_id: int,
        capacity: int,
    ):
        self.bin_id = bin_id
        self.capacity = capacity
        self.items: list[Item] = []
        self.current_load = 0
        self.status = "EMPTY"
        self.is_full = False

    def add_item(self, item: Item):
        if self.is_full:
            return False
        
        self.items.append(item)
        self.current_load += 1

        if self.current_load >= self.capacity:
            self.is_full = True
            self.status = "FULL"
        else:
            self.status = "OCCUPIED"

        return True

    def remove_all_items(self):
        self.items.clear()
        self.current_load = 0
        self.is_full = False
        self.status = "EMPTY"

    def is_available(self):
        return self.current_load < self.capacity

    def report_status(self):
        return self.status

    def report_full(self):
        return self.is_full