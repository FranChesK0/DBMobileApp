from typing import TypeVar

from pydantic import BaseModel

BaseDTOType = TypeVar("BaseDTOType", bound="BaseDTO")


class BaseDTO(BaseModel):
    pass
