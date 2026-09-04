import logging

from models.enums import ItemStatus
from models.exceptions import (
    OutputBinFullError,
    OutputBinNotFoundError,
)
from models.item import Item
from models.output_bin import OutputBin
from models.sorter import Sorter

logger = logging.getLogger(__name__)


class SortingService:
    def sort_item(
        self,
        item: Item,
        sorter: Sorter,
    ) -> Item:
        if item.destination is None:
            raise ValueError("Item destination cannot be None")

        return sorter.sort_item(
            item,
            item.destination,
        )

    def find_output_bin(
        self,
        item: Item,
        output_bins: list[OutputBin],
    ) -> OutputBin | None:
        for output_bin in output_bins:
            if output_bin.bin_id == item.destination:
                return output_bin

        return None

    def send_to_output_bin(
        self,
        item: Item,
        output_bin: OutputBin,
    ) -> bool:
        if not output_bin.add_item(item):
            return False

        item.change_status(ItemStatus.SORTED)
        item.update_location(f"OutputBin {output_bin.bin_id}")

        logger.info(
            "Item %s sorted to OutputBin %s",
            item.id,
            output_bin.bin_id,
        )

        return True

    def sort_to_output_bin(
        self,
        item: Item,
        sorter: Sorter,
        output_bins: list[OutputBin],
    ) -> Item:
        sorted_item = self.sort_item(
            item,
            sorter,
        )

        output_bin = self.find_output_bin(
            sorted_item,
            output_bins,
        )

        if output_bin is None:
            raise OutputBinNotFoundError(
                f"No OutputBin found for destination {sorted_item.destination}"
            )

        if not self.send_to_output_bin(
            sorted_item,
            output_bin,
        ):
            raise OutputBinFullError(
                f"OutputBin {output_bin.bin_id} cannot accept item {sorted_item.id}"
            )

        return sorted_item
