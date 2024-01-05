from datetime import date

from pydantic import Field
from sqlalchemy import TextClause, text

from database.database_types import VisitStatus, Gender, DoctorSpecialty, DoctorCategory
from database.procedures_functions import Function, Params, BaseFunction, BaseParams, BaseReturns


class DoctorsIdsNames(BaseFunction):
    def __init__(self) -> None:
        self._params: Params = self._Params()

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_doctors_ids_names{self._setup_keys()};")

    class _Returns(BaseReturns):
        id: str
        name: str


class PatientsIdsNames(BaseFunction):
    def __init__(self) -> None:
        self._params: Params = self._Params()

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_patients_ids_names{self._setup_keys()};")

    class _Returns(BaseReturns):
        id: str
        name: str


class VisitsByPatient(BaseFunction):
    def __init__(self, medical_card: str) -> None:
        self._params: Params = self._Params(medical_card=medical_card)

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_visits_by_patient{self._setup_keys()};")

    class _Params(BaseParams):
        medical_card: str

    class _Returns(BaseReturns):
        number: int
        date: date
        doctor_specialty: DoctorSpecialty
        doctor_full_name: str
        purpose: str
        status: VisitStatus
        diagnose: str


class VisitsByDoctor(BaseFunction):
    def __init__(self, service_number: str) -> None:
        self._params: Params = self._Params(service_number=service_number)

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_visits_by_doctor{self._setup_keys()};")

    class _Params(BaseParams):
        service_number: str

    class _Returns(BaseReturns):
        number: int
        date: date
        patient_full_name: str
        patient_gender: Gender
        patient_section: int
        purpose: str
        status: VisitStatus
        diagnose: str


class DoctorsBySection(BaseFunction):
    def __init__(self, section: int) -> None:
        self._params: Params = self._Params(section=section)

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_doctors_by_section{self._setup_keys()};")

    class _Params(BaseParams):
        section: int

    class _Returns(BaseReturns):
        service_number: str
        full_name: str
        specialty: DoctorSpecialty
        category: DoctorCategory


class PatientByMedicalCard(BaseFunction):
    def __init__(self, medical_card: str) -> None:
        self._params: Params = self._Params(medical_card=medical_card)

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_patient_by_medical_card{self._setup_keys()};")

    class _Params(BaseParams):
        medical_card: str

    class _Returns(BaseReturns):
        medical_card: str
        insurance_policy: str
        full_name: str
        gender: Gender
        birth_date: date
        street: str
        house: str
        section: int


class DoctorByServiceNumber(BaseFunction):
    def __init__(self, service_number: str) -> None:
        self._params: Params = self._Params(service_number=service_number)

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_doctor_by_service_number{self._setup_keys()};")

    class _Params(BaseParams):
        service_number: str

    class _Returns(BaseReturns):
        service_number: str
        full_name: str
        specialty: DoctorSpecialty
        category: DoctorCategory
        rate: int
        section: int


class SectionsNumbers(BaseFunction):
    def __init__(self) -> None:
        self._params: Params = self._Params()

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_sections_numbers{self._setup_keys()};")

    class _Returns(BaseReturns):
        number: int


class SectionsAddresses(BaseFunction):
    def __init__(self) -> None:
        self._params: Params = self._Params()

    @property
    def sql(self) -> TextClause:
        return text(f"SELECT * FROM select_sections_addresses{self._setup_keys()};")

    class _Returns(BaseReturns):
        addresses: list[str]


class SelectHandler:
    def __init__(self) -> None:
        self._functions: dict[str, type[Function]] = {}

    def append(self, select_function: type[Function]) -> None:
        self._functions[select_function.__name__] = select_function

    def __getattr__(self, item) -> type[Function]:
        return self._functions.get(item)


functions: list[type[Function]] = [
    DoctorsIdsNames,
    PatientsIdsNames,
    VisitsByPatient,
    VisitsByDoctor,
    DoctorsBySection,
    PatientByMedicalCard,
    DoctorByServiceNumber,
    SectionsNumbers,
    SectionsAddresses
]
select_functions: SelectHandler = SelectHandler()

for function in functions:
    select_functions.append(function)
