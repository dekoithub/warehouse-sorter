class Item:
    def __init__(self, id, barcode, weight, width, height, length, category, delivery_type, is_flammable, status, destination, location):
        self.id = id
        self.barcode = barcode
        self.weight = weight
        self.width = width
        self.height = height
        self.length = length
        self.category = category
        self.delivery_type = delivery_type
        self.is_flammable = is_flammable
        self.status = status
        self.destination = destination
        self.location = location

    def get_info(self):
        return {
            "id": self.id,
            "barcode": self.barcode,
            "weight": self.weight,
            "width": self.width,
            "height": self.height,
            "length": self.length,
            "category": self.category,
            "delivery_type": self.delivery_type,
            "is_flammable": self.is_flammable,
            "status": self.status,
            "destination": self.destination,
            "location": self.location,
        }

    def change_status(self, new_status):
        self.status = new_status

    def set_destination(self, destination):
        self.destination = destination

    def update_location(self, location):
        self.location = location