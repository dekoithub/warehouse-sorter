from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.orm.base import Base

if TYPE_CHECKING:
    from infrastructure.orm.item import ItemModel


class ProcessingEventModel(Base):
    __tablename__ = "processing_events"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    item_id: Mapped[int] = mapped_column(
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