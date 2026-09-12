from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
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

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
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