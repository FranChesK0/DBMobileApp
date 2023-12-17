from sqlalchemy import select

from database import engine, session_factory
from database.database_types import PkTypes
from database.tables import TableType, BaseTable
from database.models import BaseModel, BaseModelType
from misc import LoggerName, get_logger

logger = get_logger(LoggerName.DATABASE)


async def create_tables() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.drop_all)
        logger.warning("Database was dropped")
        await connection.run_sync(BaseModel.metadata.create_all)
        logger.warning("Database was created")


async def insert(orm: BaseModelType | list[BaseModelType]) -> None:
    async with session_factory() as session:
        if isinstance(orm, BaseModel):
            session.add(orm)
        elif isinstance(orm, list):
            session.add_all(orm)
        await session.commit()


async def select_all(table: type[TableType], relationships: bool = False) -> list[BaseTable.DTO | BaseTable.REL_DTO]:
    dto = table.REL_DTO if relationships else table.DTO
    async with session_factory() as session:
        query = select(table.ORM).options(*table.OPTIONS) if relationships else select(table.ORM)
        return [dto.model_validate(row, from_attributes=True)
                for row in (await session.execute(query)).unique().scalars().all()]


async def select_by_column(table: type[TableType], column: str, value: any,
                           relationships: bool = False) -> list[BaseTable.DTO | BaseTable.REL_DTO]:
    dto = table.REL_DTO if relationships else table.DTO
    async with session_factory() as session:
        query = (select(table.ORM).options(*table.OPTIONS).filter_by(**{column: value})
                 if relationships else
                 select(table.ORM).filter_by(**{column: value}))
        return [dto.model_validate(row, from_attributes=True)
                for row in (await session.execute(query)).unique().scalars().all()]


async def update(table: type[TableType], pk: PkTypes | tuple[PkTypes], column: str, value: any) -> None:
    async with session_factory() as session:
        orm = await session.get(table.ORM, pk)
        orm.__setattr__(column, value)
        await session.commit()


async def delete(table: type[TableType], pk: PkTypes | tuple[PkTypes]) -> None:
    async with session_factory() as session:
        orm = await session.get(table.ORM, pk)
        await session.delete(orm)
        await session.commit()
