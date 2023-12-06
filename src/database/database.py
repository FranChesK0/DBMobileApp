from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from misc import Env
from misc import LoggerName, get_logger

logger = get_logger(LoggerName.DATABASE)

url = f"postgresql+psycopg://{Env.DB_USER}:{Env.DB_PASS}@{Env.DB_HOST}:{Env.DB_PORT}/{Env.DB_NAME}"
engine = create_engine(url=url, echo=Env.DEBUG)

session_factory: sessionmaker[Session] = sessionmaker(engine)
