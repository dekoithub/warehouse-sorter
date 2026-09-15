from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    Numeric,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.orm.base import Base

if TYPE_CHECKING:
    from infrastructure.orm.destination import DestinationModel
    from infrastructure.orm.processing_event import ProcessingEventModel


class ItemModel(Base):
    __tablename__ = "items"

    __table_args__ = (
        CheckConstraint(
            "weight > 0",
            name="items_weight_positive",
        ),
        CheckConstraint(
            "width > 0 AND height > 0 AND length > 0",
            name="items_dimensions_positive",
        ),
        CheckConstraint(
            """
            status IN (
                'CREATED',
                'SCANNING',
                'ROUTING',
                'MOVING',
                'BUFFERED',
                'SORTED',
                'MANUAL_PROCESSING',
                'ERROR'
            )
            """,
            name="items_status_valid",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    barcode: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )

    weight: Mapped[Decimal] = mapped_column(
        Numeric(10, 3),
        nullable=False,
    )

    width: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    height: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    length: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    delivery_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_flammable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("false"),
    )

    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    destination_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey(
            "destinations.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    location: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    destination: Mapped[DestinationModel | None] = relationship(
        back_populates="items",
    )

    processing_events: Mapped[list[ProcessingEventModel]] = relationship(
        back_populates="item",
    )
