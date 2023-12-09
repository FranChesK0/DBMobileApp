from datetime import date
from abc import abstractmethod

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from database.database_types import int_pk, str_pk, VisitStatus, DoctorSpecialty, DoctorCategory, Gender


class BaseModel(DeclarativeBase):
    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class Visit(BaseModel):
    __tablename__ = "visit"

    visitNumber: Mapped[int_pk]
    visitDate: Mapped[date] = mapped_column(primary_key=True)
    medicalCard: Mapped[str] = mapped_column(ForeignKey("patient.medicalCard", ondelete="CASCADE"))
    serviceNumber: Mapped[str] = mapped_column(ForeignKey("doctor.serviceNumber", ondelete="CASCADE"))
    diagnose: Mapped[int | None] = mapped_column(ForeignKey("diagnose.id", ondelete="SET NULL"))
    purpose: Mapped[int | None] = mapped_column(ForeignKey("purpose.id", ondelete="SET NULL"))
    status: Mapped[VisitStatus]

    def __str__(self) -> str:
        return (f"visitNumber: {self.visitNumber}\n"
                f"visitDate: {self.visitDate}\n"
                f"medicalCard: {self.medicalCard}\n"
                f"serviceNumber: {self.serviceNumber}\n"
                f"diagnose: {self.diagnose}\n"
                f"purpose: {self.purpose}\n"
                f"status: {self.status}\n")


class Doctor(BaseModel):
    __tablename__ = "doctor"

    serviceNumber: Mapped[str_pk]
    fullName: Mapped[str]
    specialty: Mapped[DoctorSpecialty]
    category: Mapped[DoctorCategory]
    rate: Mapped[int]
    section: Mapped[int]

    def __str__(self) -> str:
        return (f"serviceNumber: {self.serviceNumber}\n"
                f"fullName: {self.fullName}\n"
                f"specialty: {self.specialty}\n"
                f"category: {self.category}\n"
                f"rate: {self.rate}\n"
                f"section: {self.section}\n")


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

    def __str__(self) -> str:
        return (f"medicalCard: {self.medicalCard}\n"
                f"insurancePolicy: {self.insurancePolicy}\n"
                f"fullName: {self.fullName}\n"
                f"gender: {self.gender}\n"
                f"birthDate: {self.birthDate}\n"
                f"street: {self.street}\n"
                f"house: {self.house}\n"
                f"Section: {self.section}\n")


class Section(BaseModel):
    __tablename__ = "section"

    id: Mapped[int_pk]
    addresses: Mapped[str]

    def __str__(self) -> str:
        return (f"id: {self.id}\n"
                f"addresses: {self.addresses}\n")


class Diagnose(BaseModel):
    __tablename__ = "diagnose"

    id: Mapped[int_pk]
    diagnose: Mapped[str]

    def __str__(self) -> str:
        return (f"id: {self.id}\n"
                f"diagnose: {self.diagnose}\n")


class Purpose(BaseModel):
    __tablename__ = "purpose"

    id: Mapped[int_pk]
    purpose: Mapped[str]

    def __str__(self) -> str:
        return (f"id: {self.id}\n"
                f"purpose: {self.purpose}\n")
