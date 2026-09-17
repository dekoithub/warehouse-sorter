from typing import Protocol


class RouteProvider(Protocol):
    def get_destination(
        self,
        barcode: str,
    ) -> int: ...
