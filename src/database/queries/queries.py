from database import engine, session_factory
from database.models import BaseModel


def create_tables() -> None:
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)


def insert(orm: BaseModel | list[BaseModel]):
    with session_factory() as session:
        if isinstance(orm, BaseModel):
            session.add(orm)
        elif isinstance(orm, list):
            session.add_all(orm)
        session.commit()
