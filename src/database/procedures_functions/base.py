from typing import TypeVar
from abc import ABC, abstractmethod

from pydantic import BaseModel
from sqlalchemy import TextClause

Procedure = TypeVar("Procedure", bound="BaseProcedure")
InsertProcedure = TypeVar("InsertProcedure", bound="BaseInsertProcedure")
UpdateProcedure = TypeVar("UpdateProcedure", bound="BaseUpdateProcedure")
DeleteProcedure = TypeVar("DeleteProcedure", bound="BaseDeleteProcedure")
Function = TypeVar("Function", bound="BaseFunction")
Params = TypeVar("Params", bound="BaseParams")
Returns = TypeVar("Returns", bound="BaseReturns")


class BaseParams(BaseModel, ABC):
    pass


class WithoutParams(BaseParams):
    pass


class BaseReturns(BaseModel, ABC):
    pass


class BaseProcedure(ABC):
    @abstractmethod
    def __init__(self, *args: list[any]) -> None:
        self._params: Params = self._Params()
        raise NotImplementedError

    @property
    @abstractmethod
    def sql(self) -> TextClause:
        raise NotImplementedError

    @property
    def params(self) -> Params:
        return self._params

    class _Params(WithoutParams):
        pass

    def _setup_keys(self) -> str:
        params_keys: list[str] = [key for key in self._params.model_dump().keys()]
        return f"(:{', :'.join(params_keys)})" if params_keys else "()"


class BaseInsertProcedure(BaseProcedure, ABC):
    pass


class BaseUpdateProcedure(BaseProcedure, ABC):
    pass


class BaseDeleteProcedure(BaseProcedure, ABC):
    pass


class BaseFunction(BaseProcedure, ABC):
    @property
    def returns(self) -> type[Returns]:
        return self._Returns

    class _Returns(BaseReturns, ABC):
        pass
