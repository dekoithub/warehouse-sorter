from sqlalchemy import select

from infrastructure.orm import ItemModel, ProcessingEventModel
from infrastructure.sqlalchemy_database import SessionFactory


def get_events_by_item_barcode(
    barcode: str,
) -> list[ProcessingEventModel]:
    with SessionFactory() as session:
        statement = (
            select(ProcessingEventModel)
            .join(ProcessingEventModel.item)
            .where(ItemModel.barcode == barcode)
            .order_by(ProcessingEventModel.created_at)
        )

        return list(session.scalars(statement).all())


def create_processing_event(
    barcode: str,
    event_type: str,
    location: str,
) -> ProcessingEventModel:
    with SessionFactory() as session:
        item_statement = (
            select(ItemModel)
            .where(ItemModel.barcode == barcode)
        )

        item = session.scalars(
            item_statement
        ).one_or_none()

        if item is None:
            raise ValueError(
                f"Item with barcode {barcode} does not exist"
            )

        event = ProcessingEventModel(
            item=item,
            event_type=event_type,
            location=location,
        )

        session.add(event)
        session.commit()

        return event