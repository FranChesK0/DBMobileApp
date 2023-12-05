import os
from abc import ABC
from typing import Final

from dotenv import load_dotenv

load_dotenv("data\\.env")


class Env(ABC):
    DEBUG: Final[int] = int(os.environ.get("DEBUG", "DEBUG is undefined"))
