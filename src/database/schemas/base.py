from typing import TypeVar

from pydantic import BaseModel

BaseDTOType = TypeVar("BaseDTOType", bound="BaseDTO")
BaseVisitDTOType = TypeVar("BaseVisitDTOType", bound="BaseVisitDTO")
BaseDoctorDTOType = TypeVar("BaseDoctorDTOType", bound="BaseDoctorDTO")
BasePatientDTOType = TypeVar("BasePatientDTOType", bound="BasePatientDTO")
BaseSectionDTOType = TypeVar("BaseSectionDTOType", bound="BaseSectionDTO")
BaseDiagnoseDTOType = TypeVar("BaseDiagnoseDTOType", bound="BaseDiagnoseDTO")
BasePurposeDTOType = TypeVar("BasePurposeDTOType", bound="BasePurposeDTO")


class BaseDTO(BaseModel):
    pass


class BaseVisitDTO(BaseDTO):
    pass


class BaseDoctorDTO(BaseDTO):
    pass


class BasePatientDTO(BaseDTO):
    pass


class BaseSectionDTO(BaseDTO):
    pass


class BaseDiagnoseDTO(BaseDTO):
    pass


class BasePurposeDTO(BaseDTO):
    pass
