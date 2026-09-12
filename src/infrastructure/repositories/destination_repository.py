from sqlalchemy import select

from infrastructure.orm.destination import DestinationModel
from infrastructure.sqlalchemy_database import SessionFactory


def get_all_destinations() -> list[DestinationModel]:
    with SessionFactory() as session:
        statement = (
            select(DestinationModel)
            .order_by(DestinationModel.id)
        )

        return list(session.scalars(statement).all())


def get_destination_by_code(code: int) -> DestinationModel | None:
    with SessionFactory() as session:
        statement = (
            select(DestinationModel)
            .where(DestinationModel.code == code)
        )

        return session.scalars(statement).one_or_none()


def create_destination(
    code: int,
    name: str,
) -> DestinationModel:
    with SessionFactory() as session:
        destination = DestinationModel(
            code=code,
            name=name,
            is_active=True,
        )

        session.add(destination)
        session.commit()

        return destination