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

        if id <= 0:
            raise ValueError("Item id must be greater than 0")

        if not barcode:
            raise ValueError("Barcode cannot be empty")

        if weight <= 0:
            raise ValueError("Weight must be greater than 0")

        if width <= 0:
            raise ValueError("Width must be greater than 0")

        if height <= 0:
            raise ValueError("Height must be greater than 0")

        if length <= 0:
            raise ValueError("Length must be greater than 0")

        if not category:
            raise ValueError("Category cannot be empty")

        if not delivery_type:
            raise ValueError("Delivery type cannot be empty")

        if destination is not None and destination <= 0:
            raise ValueError("Destination must be greater than 0")

        if not location:
            raise ValueError("Location cannot be empty")

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

    def change_status(self, new_status: ItemStatus) -> None:
        self.status = new_status

    def set_destination(self, destination: int | None) -> None:
        if destination is not None and destination <= 0:
            raise ValueError("Destination must be greater than 0")

        self.destination = destination

    def update_location(self, location: str) -> None:
        if not location:
            raise ValueError("Location cannot be empty")

        self.location = location
