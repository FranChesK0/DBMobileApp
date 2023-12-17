from datetime import date

from database.database_types import VisitStatus, DoctorSpecialty, DoctorCategory, Gender
from database.schemas import BaseVisitDTO, BaseDoctorDTO, BasePatientDTO, BaseSectionDTO, BaseDiagnoseDTO, BasePurposeDTO


class VisitAddDTO(BaseVisitDTO):
    visit_number: int
    visit_date: date
    medical_card: str
    service_number: str
    diagnose_id: int | None
    purpose_id: int | None
    status: VisitStatus


class VisitDTO(VisitAddDTO):
    pass


class DoctorAddDTO(BaseDoctorDTO):
    service_number: str
    full_name: str
    specialty: DoctorSpecialty
    category: DoctorCategory
    rate: int
    section_id: int | None


class DoctorDTO(DoctorAddDTO):
    pass


class PatientAddDTO(BasePatientDTO):
    medical_card: str
    insurance_policy: str
    full_name: str
    gender: Gender
    birth_date: date
    street: str
    house: str
    section_id: int | None


class PatientDTO(PatientAddDTO):
    pass


class SectionAddDTO(BaseSectionDTO):
    addresses: str


class SectionDTO(SectionAddDTO):
    id: int


class DiagnoseAddDTO(BaseDiagnoseDTO):
    diagnose: str


class DiagnoseDTO(DiagnoseAddDTO):
    id: int


class PurposeAddDTO(BasePurposeDTO):
    purpose: str


class PurposeDTO(PurposeAddDTO):
    id: int


class VisitRelDTO(VisitDTO):
    patient: PatientDTO
    doctor: DoctorDTO
    diagnose: DiagnoseDTO
    purpose: PurposeDTO


class DoctorRelDTO(DoctorDTO):
    visits: list[VisitDTO]
    section: SectionDTO


class PatientRelDTO(PatientDTO):
    visits: list[VisitDTO]
    section: SectionDTO


class SectionRelDTO(SectionDTO):
    patients: list[PatientDTO]
    doctors: list[DoctorDTO]


class DiagnoseRelDTO(DiagnoseDTO):
    visits: list[VisitDTO]


class PurposeRelDTO(PurposeDTO):
    visits: list[VisitDTO]
