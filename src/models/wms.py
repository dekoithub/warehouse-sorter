from models.enums import WMSStatus


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
        self.is_available = is_available

    def register_route(self, barcode: str, destination: int) -> None:
        if not barcode:
            raise ValueError("Barcode cannot be empty")

        if destination not in self.available_destinations:
            raise ValueError("Destination is not available")
    
        self.routes[barcode] = destination

    def get_destination(self, barcode: str) -> int | None:
        self.request_count += 1

        if not self.is_available:
            return None
        
        return self.routes.get(barcode)

    def remove_route(self, barcode: str) -> None:
        self.routes.pop(barcode, None)

    def is_destination_available(self, destination: int) -> bool:
        return destination in self.available_destinations

    def report_status(self) -> WMSStatus:
        return self.status