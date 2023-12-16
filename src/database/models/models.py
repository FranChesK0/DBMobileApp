from datetime import date
from typing import TypeVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database.database_types import int_pk, str_pk, VisitStatus, DoctorSpecialty, DoctorCategory, Gender

BaseModelType = TypeVar("BaseModelType", bound="BaseModel")
type PkTypes = int | str | date


class BaseModel(DeclarativeBase):
    def __repr__(self) -> str:
        cols = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__}: {','.join(cols)}>"


class Visit(BaseModel):
    __tablename__ = "visit"

    visitNumber: Mapped[int_pk]
    visitDate: Mapped[date] = mapped_column(primary_key=True)
    medicalCard: Mapped[str] = mapped_column(ForeignKey("patient.medicalCard", ondelete="CASCADE"))
    serviceNumber: Mapped[str] = mapped_column(ForeignKey("doctor.serviceNumber", ondelete="CASCADE"))
    diagnose: Mapped[int | None] = mapped_column(ForeignKey("diagnose.id", ondelete="SET NULL"))
    purpose: Mapped[int | None] = mapped_column(ForeignKey("purpose.id", ondelete="SET NULL"))
    status: Mapped[VisitStatus]


class Doctor(BaseModel):
    __tablename__ = "doctor"

    serviceNumber: Mapped[str_pk]
    fullName: Mapped[str]
    specialty: Mapped[DoctorSpecialty]
    category: Mapped[DoctorCategory]
    rate: Mapped[int]
    section: Mapped[int]


class Patient(BaseModel):
    __tablename__ = "patient"

    medicalCard: Mapped[str_pk]
    insurancePolicy: Mapped[str]
    fullName: Mapped[str]
    gender: Mapped[Gender]
    birthDate: Mapped[date]
    street: Mapped[str]
    house: Mapped[str]
    section: Mapped[int | None] = mapped_column(ForeignKey("section.id", ondelete="SET NULL"))


class Section(BaseModel):
    __tablename__ = "section"

    id: Mapped[int_pk]
    addresses: Mapped[str]


class Diagnose(BaseModel):
    __tablename__ = "diagnose"

    id: Mapped[int_pk]
    diagnose: Mapped[str]


class Purpose(BaseModel):
    __tablename__ = "purpose"

    id: Mapped[int_pk]
    purpose: Mapped[str]
