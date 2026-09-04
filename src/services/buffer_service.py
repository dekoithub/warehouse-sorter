import logging

from models.buffer import Buffer
from models.enums import ItemStatus
from models.exceptions import BufferFullError
from models.item import Item
from models.statistics import Statistics


logger = logging.getLogger(__name__)


class BufferService:
    def __init__(
        self,
        buffers: list[Buffer],
    ) -> None:
        self._buffers = buffers

    def send_to_buffer(
        self,
        item: Item,
        statistics: Statistics | None,
    ) -> bool:
        for buffer in self._buffers:
            try:
                added = buffer.add_item(item)

            except BufferFullError as error:
                logger.warning("%s", error)
                continue

            if not added:
                continue

            item.change_status(ItemStatus.BUFFERED)
            item.update_location(
                f"Buffer {buffer.buffer_id}"
            )

            logger.info(
                "Item %s sent to Buffer %s",
                item.id,
                buffer.buffer_id,
            )

            if statistics is not None:
                statistics.register_buffer_usage()

            return True

        return False

    def release_item(
        self,
        buffer: Buffer,
    ) -> Item | None:
        item = buffer.release_item()

        if item is None:
            return None

        logger.info(
            "Item %s released from Buffer %s",
            item.id,
            buffer.buffer_id,
        )

        return item

    def return_to_buffer(
        self,
        item: Item,
        buffer: Buffer,
    ) -> bool:
        try:
            added = buffer.add_item(item)

        except BufferFullError as error:
            logger.warning("%s", error)
            return False

        if not added:
            return False

        item.change_status(ItemStatus.BUFFERED)
        item.update_location(
            f"Buffer {buffer.buffer_id}"
        )

        logger.warning(
            "No Conveyor available for item %s; returned to Buffer %s",
            item.id,
            buffer.buffer_id,
        )

        return True