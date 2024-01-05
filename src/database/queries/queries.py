from misc import LoggerName, get_logger
from database import session_factory
from database.procedures_functions import InsertProcedure, Function, Returns

logger = get_logger(LoggerName.DATABASE)


async def insert(procedure: InsertProcedure) -> None:
    params_dict: dict[str, any] = procedure.params.model_dump()
    async with session_factory() as session:
        await session.execute(procedure.sql, params=params_dict)
        await session.commit()


async def update() -> None:
    async with session_factory() as session:
        await session.commit()


async def delete() -> None:
    async with session_factory() as session:
        await session.commit()


async def select(function: Function) -> list[Returns]:
    params_dict: dict[str, any] = function.params.model_dump()
    async with session_factory() as session:
        return [function.returns(**{key: value for key, value in zip(function.returns.__fields__.keys(), row)})
                for row in (await session.execute(function.sql, params=params_dict)).all()]
