from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from infrastructure.orm import (
    DestinationModel,
    ItemModel,
    ProcessingEventModel,
)
from infrastructure.sqlalchemy_database import SessionFactory
from models.item import Item


def get_all_items() -> list[ItemModel]:
    with SessionFactory() as session:
        statement = (
            select(ItemModel)
            .options(selectinload(ItemModel.destination))
            .order_by(ItemModel.id)
        )

        return list(session.scalars(statement).all())


def get_item_by_barcode(
    barcode: str,
) -> ItemModel | None:
    with SessionFactory() as session:
        statement = (
            select(ItemModel)
            .options(selectinload(ItemModel.destination))
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


def update_item_state_with_event(
    barcode: str,
    status: str,
    location: str,
) -> ItemModel | None:
    with SessionFactory() as session:
        statement = select(ItemModel).where(ItemModel.barcode == barcode)

        item = session.scalars(statement).one_or_none()

        if item is None:
            return None

        item.status = status
        item.location = location

        event = ProcessingEventModel(
            item=item,
            event_type=status,
            location=location,
        )

        session.add(event)
        session.commit()

        return item


def save_domain_item(
    domain_item: Item,
) -> ItemModel | None:
    with SessionFactory() as session:
        item_statement = (
            select(ItemModel)
            .options(selectinload(ItemModel.destination))
            .where(ItemModel.barcode == domain_item.barcode)
        )

        item_model = session.scalars(item_statement).one_or_none()

        if item_model is None:
            return None

        destination = None

        if domain_item.destination is not None:
            destination_statement = select(DestinationModel).where(
                DestinationModel.code == domain_item.destination
            )

            destination = session.scalars(destination_statement).one_or_none()

            if destination is None:
                raise ValueError(
                    f"Destination with code {domain_item.destination} does not exist"
                )

        item_model.status = domain_item.status.value
        item_model.location = domain_item.location
        item_model.destination = destination

        event = ProcessingEventModel(
            item=item_model,
            event_type=domain_item.status.value,
            location=domain_item.location,
        )

        session.add(event)
        session.commit()

        return item_model
