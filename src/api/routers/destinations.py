from fastapi import APIRouter

from api.schemas.destination import DestinationResponse
from infrastructure.repositories.destination_repository import (
    get_all_destinations,
)


router = APIRouter(
    prefix="/destinations",
    tags=["destinations"],
)


@router.get(
    "",
    response_model=list[DestinationResponse],
)
def read_destinations() -> list[DestinationResponse]:
    destinations = get_all_destinations()

    return [
        DestinationResponse.model_validate(destination)
        for destination in destinations
    ]