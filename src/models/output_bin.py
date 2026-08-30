from models.enums import OutputBinStatus


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
        self.status = OutputBinStatus.EMPTY
        self.is_full = False

    def add_item(self, item: Item):
        if not self.is_available():
            return False
        
        self.items.append(item)
        self.current_load += 1

        if self.current_load >= self.capacity:
            self.is_full = True
            self.status = OutputBinStatus.FULL
        else:
            self.status = OutputBinStatus.OCCUPIED

        return True

    def remove_all_items(self):
        self.items.clear()
        self.current_load = 0
        self.is_full = False
        self.status = OutputBinStatus.EMPTY

    def is_available(self):
        return self.current_load < self.capacity

    def report_status(self):
        return self.status

    def report_full(self):
        return self.is_full