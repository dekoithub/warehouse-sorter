from models.enums import ItemStatus


class Item:
    def __init__(
        self,
        id: int,
        barcode: str,
        weight: float,
        width: int,
        height: int,
        length: int,
        category: str,
        delivery_type: str,
        is_flammable: bool,
        status: ItemStatus,
        destination: int | None,
        location: str,
    ) -> None:
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

    def get_info(self) -> dict[str, object]:
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

    def change_status(self, new_status: ItemStatus) -> None:
        self.status = new_status

    def set_destination(self, destination: int | None) -> None:
        self.destination = destination

    def update_location(self, location: str) -> None:
        self.location = location