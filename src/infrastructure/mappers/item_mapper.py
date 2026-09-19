from infrastructure.orm import ItemModel
from models.enums import ItemStatus
from models.item import Item


class ItemMapper:
    @staticmethod
    def to_domain(
        item_model: ItemModel,
    ) -> Item:
        destination = (
            item_model.destination.code if item_model.destination is not None else None
        )

        return Item(
            id=item_model.id,
            barcode=item_model.barcode,
            weight=float(item_model.weight),
            width=item_model.width,
            height=item_model.height,
            length=item_model.length,
            category=item_model.category,
            delivery_type=item_model.delivery_type,
            is_flammable=item_model.is_flammable,
            status=ItemStatus(item_model.status),
            destination=destination,
            location=item_model.location,
        )
