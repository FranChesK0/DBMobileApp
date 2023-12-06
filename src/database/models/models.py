from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database.database_types import int_pk, VisitStatus, DoctorSpecialty, DoctorCategory, Gender


class BaseModel(DeclarativeBase):
    pass


class Visit(BaseModel):
    __tablename__ = "visit"

    visitNumber: Mapped[int_pk]
    visitDate: Mapped[datetime] = mapped_column(primary_key=True)
    medicalCard: Mapped[int] = mapped_column(ForeignKey("patient.medicalCard", ondelete="CASCADE"))
    serviceNumber: Mapped[int] = mapped_column(ForeignKey("doctor.serviceNumber", ondelete="CASCADE"))
    diagnose: Mapped[int | None] = mapped_column(ForeignKey("diagnose.id", ondelete="SET NULL"))
    purpose: Mapped[int | None] = mapped_column(ForeignKey("purpose.id", ondelete="SET NULL"))
    status: Mapped[VisitStatus]


class Doctor(BaseModel):
    __tablename__ = "doctor"

    serviceNumber: Mapped[int_pk]
    fullName: Mapped[str]
    specialty: Mapped[DoctorSpecialty]
    category: Mapped[DoctorCategory]
    rate: Mapped[int]
    section: Mapped[int]


class Patient(BaseModel):
    __tablename__ = "patient"

    medicalCard: Mapped[int_pk]
    insurancePolicy: Mapped[int]
    fullName: Mapped[str]
    gender: Mapped[Gender]
    birthDate: Mapped[datetime]
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
