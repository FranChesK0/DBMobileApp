import os
from abc import ABC
from typing import Final

from dotenv import load_dotenv

root_dir = str(os.path.dirname(os.path.abspath(__file__))).removesuffix("\\src\\misc")
load_dotenv(f"{root_dir}\\data\\.env")


class Env(ABC):
    ROOT_DIR: Final[str] = root_dir
    DEBUG: Final[int] = int(os.environ.get("DEBUG", "DEBUG is undefined"))
    DB_HOST: Final[str] = os.environ.get("DB_HOST", "DB_HOST is undefined")
    DB_PORT: Final[str] = os.environ.get("DB_PORT", "DB_PORT is undefined")
    DB_USER: Final[str] = os.environ.get("DB_USER", "DB_USER is undefined")
    DB_PASS: Final[str] = os.environ.get("DB_PASS", "DB_PASS is undefined")
    DB_NAME: Final[str] = os.environ.get("DB_NAME", "DB_NAME is undefined")
