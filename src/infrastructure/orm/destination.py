from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.orm.base import Base

if TYPE_CHECKING:
    from infrastructure.orm.item import ItemModel
    from infrastructure.orm.route import RouteModel

from sqlalchemy import BigInteger, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.orm.base import Base


class DestinationModel(Base):
    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
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
        default=True,
    )

    items: Mapped[list[ItemModel]] = relationship(
        back_populates="destination",
    )

    routes: Mapped[list[RouteModel]] = relationship(
        back_populates="destination",
    )