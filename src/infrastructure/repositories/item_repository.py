from decimal import Decimal

from sqlalchemy import select

from infrastructure.orm import DestinationModel, ItemModel
from infrastructure.sqlalchemy_database import SessionFactory

from sqlalchemy import select

from infrastructure.orm import ItemModel
from infrastructure.sqlalchemy_database import SessionFactory


def get_all_items() -> list[ItemModel]:
    with SessionFactory() as session:
        statement = (
            select(ItemModel)
            .order_by(ItemModel.id)
        )

        return list(session.scalars(statement).all())


def get_item_by_barcode(barcode: str) -> ItemModel | None:
    with SessionFactory() as session:
        statement = (
            select(ItemModel)
            .where(ItemModel.barcode == barcode)
        )

        return session.scalars(statement).one_or_none()


def create_item(
    barcode: str,
    weight: Decimal,
    width: int,
    height: int,
    length: int,
    category: str,
    delivery_type: str,
    status: str,
    location: str,
    destination_code: int | None = None,
) -> ItemModel:
    with SessionFactory() as session:
        destination = None

        if destination_code is not None:
            statement = select(DestinationModel).where(
                DestinationModel.code == destination_code
            )
            destination = session.scalars(statement).one_or_none()

            if destination is None:
                raise ValueError(
                    f"Destination with code {destination_code} does not exist"
                )

        item = ItemModel(
            barcode=barcode,
            weight=weight,
            width=width,
            height=height,
            length=length,
            category=category,
            delivery_type=delivery_type,
            status=status,
            location=location,
            destination=destination,
        )

        session.add(item)
        session.commit()

        return item


def update_item_state(
    barcode: str,
    status: str,
    location: str,
) -> ItemModel | None:
    with SessionFactory() as session:
        statement = (
            select(ItemModel)
            .where(ItemModel.barcode == barcode)
        )

        item = session.scalars(statement).one_or_none()

        if item is None:
            return None

        item.status = status
        item.location = location

        session.commit()

        return item