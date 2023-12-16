from sqlalchemy import select

from database import engine, session_factory
from database import models
from database.models import BaseModel, BaseModelType, PkTypes
from misc import LoggerName, get_logger

logger = get_logger(LoggerName.DATABASE)


def create_tables() -> None:
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)


def insert(orm: BaseModelType | list[BaseModelType]) -> None:
    with session_factory() as session:
        if isinstance(orm, BaseModel):
            session.add(orm)
        elif isinstance(orm, list):
            session.add_all(orm)
        session.commit()


def select_all(orm: type[BaseModelType]) -> list[BaseModelType]:
    with session_factory() as session:
        query = select(orm)
        return list(session.execute(query).scalars().all())


def select_by_pk(orm: type[BaseModelType], pk: PkTypes | tuple[PkTypes]) -> BaseModelType:
    with session_factory() as session:
        return session.get(orm, pk)


def select_visits_by_patient(patient_medical_card: str) -> list[models.Visit]:
    with session_factory() as session:
        query = select(models.Visit).filter_by(medical_card=patient_medical_card)
    return list(session.execute(query).scalars().all())


def select_visits_by_doctor(doctor_service_number: str) -> list[models.Visit]:
    with session_factory() as session:
        query = select(models.Visit).filter_by(service_number=doctor_service_number)
    return list(session.execute(query).scalars().all())


def select_doctors_by_section(section: int) -> list[models.Doctor]:
    with session_factory() as session:
        query = select(models.Doctor).filter_by(section=section)
    return list(session.execute(query).scalars().all())


def select_patients_by_section(section: int) -> list[models.Patient]:
    with session_factory() as session:
        query = select(models.Patient).filter_by(section=section)
    return list(session.execute(query).scalars().all())
