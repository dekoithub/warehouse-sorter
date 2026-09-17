from fastapi import APIRouter, HTTPException, Path, status

from api.schemas.destination import (
    DestinationActiveUpdate,
    DestinationCreate,
    DestinationResponse,
)
from infrastructure.repositories.destination_repository import (
    create_destination,
    get_all_destinations,
    get_destination_by_code,
    set_destination_active,
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


@router.get(
    "/{code}",
    response_model=DestinationResponse,
)
def read_destination(
    code: int = Path(gt=0),
) -> DestinationResponse:
    destination = get_destination_by_code(code)

    if destination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found",
        )

    return DestinationResponse.model_validate(destination)


@router.post(
    "",
    response_model=DestinationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_destination_endpoint(
    destination_data: DestinationCreate,
) -> DestinationResponse:
    existing_destination = get_destination_by_code(
        destination_data.code
    )

    if existing_destination is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Destination with this code already exists",
        )

    destination = create_destination(
        code=destination_data.code,
        name=destination_data.name,
    )

    return DestinationResponse.model_validate(destination)


@router.patch(
    "/{code}",
    response_model=DestinationResponse,
)
def update_destination_active(
    destination_data: DestinationActiveUpdate,
    code: int = Path(gt=0),
) -> DestinationResponse:
    destination = set_destination_active(
        code=code,
        is_active=destination_data.is_active,
    )

    if destination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Destination not found",
        )

    return DestinationResponse.model_validate(destination)