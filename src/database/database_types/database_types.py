from enum import Enum
from datetime import date
from typing import Annotated

from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_pk = Annotated[str, mapped_column(primary_key=True)]
type PkTypes = int | str | date


class VisitStatus(str, Enum):
    primary = "первичный"
    repeated = "повторный"
    diagnose = "диагноз"


class DoctorSpecialty(str, Enum):
    allergist = "аллерголог"
    dermatologist = "дерматолог"
    cardiologist = "кардиолог"
    neurologist = "невролог"
    ophthalmologist = "офтальмолог"
    pediatrician = "педиатр"
    psychotherapist = "психотерапевт"
    resuscitator = "реаниматолог"
    dentist = "стоматолог"
    surgeon = "хирург"


class DoctorCategory(str, Enum):
    second = "вторая"
    first = "первая"
    higher = "высшая"


class Gender(str, Enum):
    male = "мужчина"
    female = "женщина"
