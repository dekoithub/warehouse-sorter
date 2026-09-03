import logging

from models.enums import WMSStatus
from models.exceptions import (
    EquipmentUnavailableError,
    RouteNotFoundError,
)


logger = logging.getLogger(__name__)


class WMS:
    def __init__(
        self,
        routes: dict[str, int],
        available_destinations: list[int],
        is_available: bool,
    ) -> None:

        if not available_destinations:
            raise ValueError("Available destinations cannot be empty")

        if any(destination <= 0 for destination in available_destinations):
                raise ValueError("Destinations must be greater than 0")

        for barcode, destination in routes.items():
            if not barcode:
                raise ValueError("Barcode cannot be empty")

            if destination not in available_destinations:
                raise ValueError("Route destination is not available")
        
        self.routes = routes
        self.available_destinations = available_destinations
        self.request_count = 0
        self.status = (
            WMSStatus.AVAILABLE
            if is_available
            else WMSStatus.UNAVAILABLE
        )

    def register_route(self, barcode: str, destination: int) -> None:
        if not barcode:
            raise ValueError("Barcode cannot be empty")

        if destination not in self.available_destinations:
            raise ValueError("Destination is not available")
    
        self.routes[barcode] = destination

        logger.debug(
            "Route registered: barcode=%s, destination=%s",
            barcode,
            destination,
        )

    @property
    def is_available(self) -> bool:
        return self.status == WMSStatus.AVAILABLE


    def enable(self) -> None:
        self.status = WMSStatus.AVAILABLE
        logger.info("WMS enabled")


    def disable(self) -> None:
        self.status = WMSStatus.UNAVAILABLE
        logger.info("WMS disabled")


    def get_destination(self, barcode: str) -> int:
        self.request_count += 1

        if not self.is_available:
            raise EquipmentUnavailableError("WMS is unavailable")

        destination = self.routes.get(barcode)

        if destination is None:
            raise RouteNotFoundError(
                f"Route not found for barcode {barcode}"
            )

        return destination

    def remove_route(self, barcode: str) -> None:
        destination = self.routes.pop(barcode, None)

        if destination is not None:
            logger.debug(
                "Route removed: barcode=%s, destination=%s",
                barcode,
                destination,
            )

    def is_destination_available(self, destination: int) -> bool:
        return destination in self.available_destinations

    def report_status(self) -> WMSStatus:
        return self.status