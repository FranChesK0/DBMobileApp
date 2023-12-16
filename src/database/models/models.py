from __future__ import annotations
from datetime import date
from typing import TypeVar

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from database.database_types import int_pk, str_pk, VisitStatus, DoctorSpecialty, DoctorCategory, Gender

BaseModelType = TypeVar("BaseModelType", bound="BaseModel")
type PkTypes = int | str | date


class BaseModel(DeclarativeBase):
    def __repr__(self) -> str:
        cols = [f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__}: {','.join(cols)}>"


class Visit(BaseModel):
    __tablename__ = "visit"

    visit_number: Mapped[int_pk]
    visit_date: Mapped[date] = mapped_column(primary_key=True)
    medical_card: Mapped[str] = mapped_column(ForeignKey("patient.medicalCard", ondelete="CASCADE"))
    service_number: Mapped[str] = mapped_column(ForeignKey("doctor.serviceNumber", ondelete="CASCADE"))
    diagnose_id: Mapped[int | None] = mapped_column(ForeignKey("diagnose.id", ondelete="SET NULL"))
    purpose_id: Mapped[int | None] = mapped_column(ForeignKey("purpose.id", ondelete="SET NULL"))
    status: Mapped[VisitStatus]


class Doctor(BaseModel):
    __tablename__ = "doctor"

    service_number: Mapped[str_pk]
    full_name: Mapped[str]
    specialty: Mapped[DoctorSpecialty]
    category: Mapped[DoctorCategory]
    rate: Mapped[int]
    section: Mapped[int]


class Patient(BaseModel):
    __tablename__ = "patient"

    medical_card: Mapped[str_pk]
    insurance_policy: Mapped[str]
    full_name: Mapped[str]
    gender: Mapped[Gender]
    birth_date: Mapped[date]
    street: Mapped[str]
    house: Mapped[str]
    section_id: Mapped[int | None] = mapped_column(ForeignKey("section.id", ondelete="SET NULL"))


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
