from infrastructure.repositories.route_repository import (
    get_destination_code_by_barcode,
)
from models.exceptions import RouteNotFoundError


class DatabaseRouteProvider:
    def get_destination(
        self,
        barcode: str,
    ) -> int:
        destination = get_destination_code_by_barcode(barcode)

        if destination is None:
            raise RouteNotFoundError(f"Route not found for barcode {barcode}")

        return destination
