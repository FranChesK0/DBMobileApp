from datetime import date

from sqlalchemy import TextClause, text

from database.procedures_functions import InsertProcedure, Params, BaseInsertProcedure, BaseParams
from database.database_types import VisitStatus, Gender, DoctorSpecialty, DoctorCategory


class Visit(BaseInsertProcedure):
    def __init__(self,
                 number: int,
                 visit_date: date,
                 medical_card: str,
                 service_number: str,
                 diagnose: str,
                 purpose: str,
                 status: VisitStatus) -> None:
        self._params: Params = self._Params(
            number=number,
            date=visit_date,
            medical_card=medical_card,
            service_number=service_number,
            diagnose=diagnose,
            purpose=purpose,
            status=status
        )

    @property
    def sql(self) -> TextClause:
        return text(f"CALL insert_visit{self._setup_keys()};")

    class _Params(BaseParams):
        number: int
        date: date
        medical_card: str
        service_number: str
        diagnose: str
        purpose: str
        status: VisitStatus


class Doctor(BaseInsertProcedure):
    def __init__(self,
                 service_number: str,
                 full_name: str,
                 specialty: DoctorSpecialty,
                 category: DoctorCategory,
                 rate: int,
                 section: int | None = None) -> None:
        self._params: Params = self._Params(
            service_number=service_number,
            full_name=full_name,
            specialty=specialty,
            category=category,
            rate=rate,
            section=section
        )

    @property
    def sql(self) -> TextClause:
        return text(f"CALL insert_doctor{self._setup_keys()};")

    class _Params(BaseParams):
        service_number: str
        full_name: str
        specialty: DoctorSpecialty
        category: DoctorCategory
        rate: int
        section: int | None


class Patient(BaseInsertProcedure):
    def __init__(self,
                 medical_card: str,
                 insurance_policy: str,
                 full_name: str,
                 gender: Gender,
                 birth_date: date,
                 street: str,
                 house: str) -> None:
        self._params: Params = self._Params(
            medical_card=medical_card,
            insurance_policy=insurance_policy,
            full_name=full_name,
            gender=gender,
            birth_date=birth_date,
            street=street,
            house=house
        )

    @property
    def sql(self) -> TextClause:
        return text(f"CALL insert_patient{self._setup_keys()};")

    class _Params(BaseParams):
        medical_card: str
        insurance_policy: str
        full_name: str
        gender: Gender
        birth_date: date
        street: str
        house: str


class Section(BaseInsertProcedure):
    def __init__(self, addresses: list[str]) -> None:
        self._params: Params = self._Params(addresses=";".join(addresses))

    @property
    def sql(self) -> TextClause:
        return text(f"CALL insert_section{self._setup_keys()};")

    class _Params(BaseParams):
        addresses: str


class Diagnose(BaseInsertProcedure):
    def __init__(self, diagnose: str) -> None:
        self._params: Params = self._Params(diagnose=diagnose)

    @property
    def sql(self) -> TextClause:
        return text(f"CALL insert_diagnose{self._setup_keys()};")

    class _Params(BaseParams):
        diagnose: str


class Purpose(BaseInsertProcedure):
    def __init__(self, purpose: str) -> None:
        self._params: Params = self._Params(purpose=purpose)

    @property
    def sql(self) -> TextClause:
        return text(f"CALL insert_purpose{self._setup_keys()};")

    class _Params(BaseParams):
        purpose: str


class Insert:
    def __init__(self) -> None:
        self._insert_procedures: dict[str, type[InsertProcedure]] = {}

    def append(self, insert_procedure: type[InsertProcedure]) -> None:
        self._insert_procedures[insert_procedure.__name__] = insert_procedure

    def __getattr__(self, item) -> type[InsertProcedure]:
        return self._insert_procedures.get(item)


insert_procedures_list: list[type[InsertProcedure]] = [
    Visit,
    Doctor,
    Patient,
    Section,
    Diagnose,
    Purpose
]
insert_procedures: Insert = Insert()

for procedure in insert_procedures_list:
    insert_procedures.append(procedure)
