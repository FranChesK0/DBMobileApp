from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload, contains_eager

from database import engine, session_factory
from database import models
from database.database_types import PkTypes
from database.models import BaseModel, BaseModelType
from misc import LoggerName, get_logger

logger = get_logger(LoggerName.DATABASE)


async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)
        await connection.run_sync(BaseModel.metadata.create_all)


async def insert(orm: BaseModelType | list[BaseModelType]) -> None:
    async with session_factory() as session:
        if isinstance(orm, BaseModel):
            session.add(orm)
        elif isinstance(orm, list):
            session.add_all(orm)
        await session.commit()


async def select_all(orm: type[BaseModelType]) -> list[BaseModelType]:
    async with session_factory() as session:
        query = select(orm).options(*_get_options(orm))
        return list((await session.execute(query)).unique().scalars().all())


async def select_by_parameter(orm: type[BaseModelType], name: str, value: any) -> list[BaseModelType]:
    async with session_factory() as session:
        query = select(orm).options(*_get_options(orm)).filter_by(**{name: value})
        return list((await session.execute(query)).unique().scalars().all())


def _get_options(orm: type[BaseModelType]):
    match orm:
        case models.Visit:
            return (joinedload(models.Visit.patient),
                    joinedload(models.Visit.doctor),
                    joinedload(models.Visit.diagnose),
                    joinedload(models.Visit.purpose))
        case models.Doctor:
            return (selectinload(models.Doctor.visits),
                    joinedload(models.Doctor.section))
        case models.Patient:
            return (selectinload(models.Patient.visits),
                    joinedload(models.Patient.section))
        case models.Section:
            return (selectinload(models.Section.doctors),
                    selectinload(models.Section.patients))
        case models.Diagnose:
            return (selectinload(models.Diagnose.visits), )
        case models.Purpose:
            return (selectinload(models.Purpose.visits), )
        case _:
            return ()
