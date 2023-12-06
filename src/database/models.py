from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .database import session_factory, Base
from database.database_types import int_pk, VisitStatus, DoctorSpecialty, DoctorCategory, Gender


class Visit(Base):
    __tablename__ = "visit"

    VisitNumber: Mapped[int_pk]
    VisitDate: Mapped[datetime] = mapped_column(primary_key=True)
    MedicalCard: Mapped[int] = mapped_column(ForeignKey("patient.MedicalCard", ondelete="CASCADE"))
    ServiceNumber: Mapped[int] = mapped_column(ForeignKey("doctor.ServiceNumber", ondelete="CASCADE"))
    Diagnose: Mapped[int | None] = mapped_column(ForeignKey("diagnose.id", ondelete="SET NULL"))
    Purpose: Mapped[int | None] = mapped_column(ForeignKey("purpose.id", ondelete="SET NULL"))
    Status: Mapped[VisitStatus]


class Doctor(Base):
    __tablename__ = "doctor"

    ServiceNumber: Mapped[int_pk]
    FullName: Mapped[str]
    Specialty: Mapped[DoctorSpecialty]
    Category: Mapped[DoctorCategory]
    Rate: Mapped[int]
    Section: Mapped[int]


class Patient(Base):
    __tablename__ = "patient"

    MedicalCard: Mapped[int_pk]
    InsurancePolicy: Mapped[int]
    FullName: Mapped[str]
    Gender: Mapped[Gender]
    BirthDate: Mapped[datetime]
    Street: Mapped[str]
    House: Mapped[str]
    Section: Mapped[int | None] = mapped_column(ForeignKey("section.id", ondelete="SET NULL"))


class Section(Base):
    __tablename__ = "section"

    id: Mapped[int_pk]
    Addresses: Mapped[str]


class Diagnose(Base):
    __tablename__ = "diagnose"

    id: Mapped[int_pk]
    Name: Mapped[str]


class Purpose(Base):
    __tablename__ = "purpose"

    id: Mapped[int_pk]
    Name: Mapped[str]
