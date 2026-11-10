from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.orm.base import Base

if TYPE_CHECKING:
    from infrastructure.orm.item import ItemModel


class ProcessingEventModel(Base):
    __tablename__ = "processing_events"

    __table_args__ = (
        CheckConstraint(
            """
            event_type IN (
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
            name="processing_events_type_valid",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(
            "items.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    event_type: Mapped[str] = mapped_column(
        Text,
        nullable=False,
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

    item: Mapped[ItemModel] = relationship(
        back_populates="processing_events",
    )
