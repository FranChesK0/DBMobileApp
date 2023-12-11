from sqlalchemy import select

from database import engine, session_factory
from database.models import BaseModel, BaseModelType, PkTypes
from misc import LoggerName, get_logger

logger = get_logger(LoggerName.DATABASE)


def create_tables() -> None:
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)


def insert(orm: BaseModel | list[BaseModel]) -> None:
    with session_factory() as session:
        if isinstance(orm, BaseModel):
            session.add(orm)
        elif isinstance(orm, list):
            session.add_all(orm)
        session.commit()


def select_all(orm: type[BaseModelType]) -> list[BaseModelType]:
    with session_factory() as session:
        query = select(orm)
        return list(session.execute(query).scalars().all())


def select_by_pk(orm: type[BaseModelType], pk: PkTypes | tuple[PkTypes]) -> BaseModelType:
    with session_factory() as session:
        return session.get(orm, pk)
