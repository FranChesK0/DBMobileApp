import logging
from enum import Enum
from logging import config

from . import Env

config.fileConfig(f"{Env.ROOT_DIR}\\data\\logging.conf")


class LoggerName(Enum):
    MAIN = "main"
    ROOT = "root"
    DEBUG = "debug"
    DATABASE = "database"
    NONE = None


def get_logger(name: LoggerName = LoggerName.NONE) -> logging.Logger:
    if Env.DEBUG:
        return logging.getLogger(LoggerName.DEBUG.value)
    return logging.getLogger(name.value if name.value is not None else LoggerName.ROOT.value)
