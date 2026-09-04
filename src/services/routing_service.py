import logging

from models.conveyor import Conveyor
from models.enums import ItemStatus
from models.exceptions import EquipmentUnavailableError
from models.item import Item
from models.wms import WMS

logger = logging.getLogger(__name__)


class RoutingService:
    def __init__(
        self,
        wms: WMS,
    ) -> None:
        self._wms = wms

    def request_route(self, barcode: str) -> int:
        return self._wms.get_destination(barcode)

    def send_to_conveyor(
        self,
        item: Item,
        conveyors: list[Conveyor],
    ) -> Conveyor | None:
        for conveyor in conveyors:
            try:
                accepted = conveyor.accept_item(item)

                if not accepted:
                    continue

                conveyor.start()

            except EquipmentUnavailableError as error:
                logger.warning("%s", error)
                continue

            item.change_status(ItemStatus.MOVING)
            item.update_location(f"Conveyor {conveyor.conveyor_id}")

            logger.info(
                "Item %s sent to Conveyor %s",
                item.id,
                conveyor.conveyor_id,
            )

            return conveyor

        return None
