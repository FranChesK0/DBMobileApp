from database import engine, session_factory
from database.models import BaseModel


def create_tables() -> None:
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)
