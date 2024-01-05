import os
import sys
from abc import ABC
from typing import Final

from dotenv import load_dotenv

debug: bool = "-d" in sys.argv or "--debug" in sys.argv

root_dir: str = str(os.path.dirname(os.path.abspath(__file__))).removesuffix(os.path.join("src", "environment"))
os.environ["ROOT_DIR"] = root_dir

load_dotenv(os.path.join(root_dir, "data", ".env"))


class Env(ABC):
    ROOT_DIR: Final[str] = root_dir
    DEBUG: Final[bool] = debug
    DB_HOST: Final[str] = os.environ.get("DB_HOST", "DB_HOST is undefined")
    DB_PORT: Final[str] = os.environ.get("DB_PORT", "DB_PORT is undefined")
    DB_USER: Final[str] = os.environ.get("DB_USER", "DB_USER is undefined")
    DB_PASS: Final[str] = os.environ.get("DB_PASS", "DB_PASS is undefined")
    DB_NAME: Final[str] = os.environ.get("DB_NAME", "DB_NAME is undefined")
