from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database.database_types import int_pk, VisitStatus, DoctorSpecialty, DoctorCategory, Gender


class BaseModel(DeclarativeBase):
    pass


class Visit(BaseModel):
    __tablename__ = "visit"

    VisitNumber: Mapped[int_pk]
    VisitDate: Mapped[datetime] = mapped_column(primary_key=True)
    MedicalCard: Mapped[int] = mapped_column(ForeignKey("patient.MedicalCard", ondelete="CASCADE"))
    ServiceNumber: Mapped[int] = mapped_column(ForeignKey("doctor.ServiceNumber", ondelete="CASCADE"))
    Diagnose: Mapped[int | None] = mapped_column(ForeignKey("diagnose.id", ondelete="SET NULL"))
    Purpose: Mapped[int | None] = mapped_column(ForeignKey("purpose.id", ondelete="SET NULL"))
    Status: Mapped[VisitStatus]


class Doctor(BaseModel):
    __tablename__ = "doctor"

    ServiceNumber: Mapped[int_pk]
    FullName: Mapped[str]
    Specialty: Mapped[DoctorSpecialty]
    Category: Mapped[DoctorCategory]
    Rate: Mapped[int]
    Section: Mapped[int]


class Patient(BaseModel):
    __tablename__ = "patient"

    MedicalCard: Mapped[int_pk]
    InsurancePolicy: Mapped[int]
    FullName: Mapped[str]
    Gender: Mapped[Gender]
    BirthDate: Mapped[datetime]
    Street: Mapped[str]
    House: Mapped[str]
    Section: Mapped[int | None] = mapped_column(ForeignKey("section.id", ondelete="SET NULL"))


class Section(BaseModel):
    __tablename__ = "section"

    id: Mapped[int_pk]
    Addresses: Mapped[str]


class Diagnose(BaseModel):
    __tablename__ = "diagnose"

    id: Mapped[int_pk]
    Name: Mapped[str]


class Purpose(BaseModel):
    __tablename__ = "purpose"

    id: Mapped[int_pk]
    Name: Mapped[str]
