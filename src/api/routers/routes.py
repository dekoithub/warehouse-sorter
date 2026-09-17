from fastapi import APIRouter, HTTPException, Path, status

from api.schemas.route import (
    RouteActiveUpdate,
    RouteCreate,
    RouteResponse,
)
from infrastructure.repositories.route_repository import (
    create_route,
    get_all_routes,
    get_route_by_barcode,
    set_route_active,
)

router = APIRouter(
    prefix="/routes",
    tags=["routes"],
)


@router.get(
    "",
    response_model=list[RouteResponse],
)
def read_routes() -> list[RouteResponse]:
    routes = get_all_routes()

    return [RouteResponse.model_validate(route) for route in routes]


@router.get(
    "/{barcode}",
    response_model=RouteResponse,
)
def read_route(
    barcode: str = Path(min_length=1),
) -> RouteResponse:
    route = get_route_by_barcode(barcode)

    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found",
        )

    return RouteResponse.model_validate(route)


@router.post(
    "",
    response_model=RouteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_route_endpoint(
    route_data: RouteCreate,
) -> RouteResponse:
    existing_route = get_route_by_barcode(route_data.barcode)

    if existing_route is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Route for this barcode already exists",
        )

    try:
        route = create_route(
            barcode=route_data.barcode,
            destination_code=route_data.destination_code,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error

    return RouteResponse.model_validate(route)


@router.patch(
    "/{barcode}",
    response_model=RouteResponse,
)
def update_route_active(
    route_data: RouteActiveUpdate,
    barcode: str = Path(min_length=1),
) -> RouteResponse:
    route = set_route_active(
        barcode=barcode,
        is_active=route_data.is_active,
    )

    if route is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Route not found",
        )

    return RouteResponse.model_validate(route)
