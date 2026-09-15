from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Identity,
    Integer,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.orm.base import Base

if TYPE_CHECKING:
    from infrastructure.orm.item import ItemModel
    from infrastructure.orm.route import RouteModel


class DestinationModel(Base):
    __tablename__ = "destinations"

    __table_args__ = (
        CheckConstraint(
            "code > 0",
            name="destinations_code_positive",
        ),
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )

    code: Mapped[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true"),
    )

    items: Mapped[list[ItemModel]] = relationship(
        back_populates="destination",
    )

    routes: Mapped[list[RouteModel]] = relationship(
        back_populates="destination",
    )
