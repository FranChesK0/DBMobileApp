import os
import logging
from enum import Enum
from logging import config

from environment import Env

logs_dir: str = os.path.join(Env.ROOT_DIR, "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

config.fileConfig(os.path.join(Env.ROOT_DIR, "data", "logging.conf"))


class LoggerName(Enum):
    ROOT: str = "root"
    MAIN: str = "main"
    DEBUG: str = "debug"
    DATABASE: str = "database"


def get_logger(name: LoggerName | None = None) -> logging.Logger:
    if Env.DEBUG:
        return logging.getLogger(LoggerName.DEBUG.value)
    return logging.getLogger(name.value if name is not None else LoggerName.ROOT.value)
