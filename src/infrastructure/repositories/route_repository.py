from sqlalchemy import select

from infrastructure.orm import DestinationModel, RouteModel
from infrastructure.sqlalchemy_database import SessionFactory


def get_route_by_barcode(barcode: str) -> RouteModel | None:
    with SessionFactory() as session:
        statement = (
            select(RouteModel)
            .where(RouteModel.barcode == barcode)
        )

        return session.scalars(statement).one_or_none()


def create_route(
    barcode: str,
    destination_code: int,
) -> RouteModel:
    with SessionFactory() as session:
        destination_statement = (
            select(DestinationModel)
            .where(DestinationModel.code == destination_code)
        )

        destination = session.scalars(
            destination_statement
        ).one_or_none()

        if destination is None:
            raise ValueError(
                f"Destination with code {destination_code} does not exist"
            )

        route = RouteModel(
            barcode=barcode,
            destination=destination,
            is_active=True,
        )

        session.add(route)
        session.commit()

        return route


def set_route_active(
    barcode: str,
    is_active: bool,
) -> RouteModel | None:
    with SessionFactory() as session:
        statement = (
            select(RouteModel)
            .where(RouteModel.barcode == barcode)
        )

        route = session.scalars(statement).one_or_none()

        if route is None:
            return None

        route.is_active = is_active

        session.commit()

        return route