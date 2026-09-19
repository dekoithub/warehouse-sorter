from typing import Protocol

from models.item import Item


class ItemStore(Protocol):
    def get_by_barcode(
        self,
        barcode: str,
    ) -> Item | None: ...

    def save(
        self,
        item: Item,
    ) -> bool: ...
