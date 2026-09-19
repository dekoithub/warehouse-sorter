from infrastructure.mappers.item_mapper import ItemMapper
from infrastructure.repositories.item_repository import (
    get_item_by_barcode,
    save_domain_item,
)
from models.item import Item


class DatabaseItemStore:
    def get_by_barcode(
        self,
        barcode: str,
    ) -> Item | None:
        item_model = get_item_by_barcode(barcode)

        if item_model is None:
            return None

        return ItemMapper.to_domain(item_model)

    def save(
        self,
        item: Item,
    ) -> bool:
        saved_item = save_domain_item(item)

        return saved_item is not None
