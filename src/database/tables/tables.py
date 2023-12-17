from abc import ABC
from typing import TypeVar

from sqlalchemy.orm import joinedload, selectinload

from database import models, schemas

TableType = TypeVar("TableType", bound="BaseTable")


class BaseTable(ABC):
    ORM: type[models.BaseModelType] = models.BaseModelType
    DTO: type[schemas.BaseDTOType] = schemas.BaseDTOType
    ADD_DTO: type[schemas.BaseDTOType] = schemas.BaseDTOType
    REL_DTO: type[schemas.BaseDTOType] = schemas.BaseDTOType
    OPTIONS: tuple = tuple()


class Visit(BaseTable):
    ORM: type[models.Visit] = models.Visit
    DTO: type[schemas.VisitDTO] = schemas.VisitDTO
    ADD_DTO: type[schemas.VisitAddDTO] = schemas.VisitAddDTO
    REL_DTO: type[schemas.VisitRelDTO] = schemas.VisitRelDTO
    OPTIONS: tuple = (joinedload(models.Visit.patient),
                      joinedload(models.Visit.doctor),
                      joinedload(models.Visit.diagnose),
                      joinedload(models.Visit.purpose))


class Doctor(BaseTable):
    ORM: type[models.Doctor] = models.Doctor
    DTO: type[schemas.DoctorDTO] = schemas.DoctorDTO
    ADD_DTO: type[schemas.DoctorAddDTO] = schemas.DoctorAddDTO
    REL_DTO: type[schemas.DoctorRelDTO] = schemas.DoctorRelDTO
    OPTIONS: tuple = (selectinload(models.Doctor.visits),
                      joinedload(models.Doctor.section))


class Patient(BaseTable):
    ORM: type[models.Patient] = models.Patient
    DTO: type[schemas.PatientDTO] = schemas.PatientDTO
    ADD_DTO: type[schemas.PatientAddDTO] = schemas.PatientAddDTO
    REL_DTO: type[schemas.PatientRelDTO] = schemas.PatientRelDTO
    OPTIONS: tuple = (selectinload(models.Patient.visits),
                      joinedload(models.Patient.section))


class Section(BaseTable):
    ORM: type[models.Section] = models.Section
    DTO: type[schemas.SectionDTO] = schemas.SectionDTO
    ADD_DTO: type[schemas.PatientAddDTO] = schemas.PatientAddDTO
    REL_DTO: type[schemas.PatientRelDTO] = schemas.PatientRelDTO
    OPTIONS: tuple = (selectinload(models.Section.doctors),
                      selectinload(models.Section.patients))


class Diagnose(BaseTable):
    ORM: type[models.Diagnose] = models.Diagnose
    DTO: type[schemas.DiagnoseDTO] = schemas.DiagnoseDTO
    ADD_DTO: type[schemas.DiagnoseAddDTO] = schemas.DiagnoseAddDTO
    REL_DTO: type[schemas.DiagnoseRelDTO] = schemas.DiagnoseRelDTO
    OPTIONS: tuple = (selectinload(models.Diagnose.visits),)


class Purpose(BaseTable):
    ORM: type[models.Purpose] = models.Purpose
    DTO: type[schemas.PurposeDTO] = schemas.PurposeDTO
    ADD_DTO: type[schemas.PurposeAddDTO] = schemas.PurposeAddDTO
    REL_DTO: type[schemas.PurposeRelDTO] = schemas.PurposeRelDTO
    OPTIONS: tuple = (selectinload(models.Purpose.visits),)
