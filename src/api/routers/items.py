from fastapi import APIRouter, HTTPException, Path, status

from api.dependencies import build_process_item_use_case
from api.schemas.item import (
    ItemCreate,
    ItemProcessResponse,
    ItemResponse,
    ItemStateUpdate,
)
from api.schemas.processing_event import ProcessingEventResponse
from application.use_cases.process_item import (
    ItemNotFoundError,
    ItemPersistenceError,
)
from infrastructure.repositories.item_repository import (
    create_item,
    get_all_items,
    get_item_by_barcode,
    update_item_state_with_event,
)
from infrastructure.repositories.processing_event_repository import (
    get_events_by_item_barcode,
)

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get(
    "",
    response_model=list[ItemResponse],
)
def read_items() -> list[ItemResponse]:
    items = get_all_items()

    return [ItemResponse.model_validate(item) for item in items]


@router.get(
    "/{barcode}",
    response_model=ItemResponse,
)
def read_item(
    barcode: str = Path(min_length=1),
) -> ItemResponse:
    item = get_item_by_barcode(barcode)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return ItemResponse.model_validate(item)


@router.get(
    "/{barcode}/events",
    response_model=list[ProcessingEventResponse],
)
def read_item_events(
    barcode: str = Path(min_length=1),
) -> list[ProcessingEventResponse]:
    item = get_item_by_barcode(barcode)

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    events = get_events_by_item_barcode(barcode)

    return [ProcessingEventResponse.model_validate(event) for event in events]


@router.post(
    "",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item_endpoint(
    item_data: ItemCreate,
) -> ItemResponse:
    existing_item = get_item_by_barcode(item_data.barcode)

    if existing_item is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Item with this barcode already exists",
        )

    try:
        item = create_item(
            barcode=item_data.barcode,
            weight=item_data.weight,
            width=item_data.width,
            height=item_data.height,
            length=item_data.length,
            category=item_data.category,
            delivery_type=item_data.delivery_type,
            status=item_data.status,
            location=item_data.location,
            destination_code=item_data.destination_code,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return ItemResponse.model_validate(item)


@router.post(
    "/{barcode}/process",
    response_model=ItemProcessResponse,
)
def process_item_endpoint(
    barcode: str = Path(min_length=1),
) -> ItemProcessResponse:
    use_case = build_process_item_use_case()

    try:
        item = use_case.execute(barcode)

    except ItemNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    except ItemPersistenceError as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        ) from error

    return ItemProcessResponse.model_validate(item)


@router.patch(
    "/{barcode}",
    response_model=ItemResponse,
)
def update_item(
    item_data: ItemStateUpdate,
    barcode: str = Path(min_length=1),
) -> ItemResponse:
    item = update_item_state_with_event(
        barcode=barcode,
        status=item_data.status,
        location=item_data.location,
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
        )

    return ItemResponse.model_validate(item)
