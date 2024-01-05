from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from environment import Env

url = f"postgresql+asyncpg://{Env.DB_USER}:{Env.DB_PASS}@{Env.DB_HOST}:{Env.DB_PORT}/{Env.DB_NAME}"
engine = create_async_engine(url=url, echo=Env.DEBUG)

session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(engine)
