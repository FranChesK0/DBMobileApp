from enum import Enum
from datetime import date
from typing import Annotated

from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]
str_pk = Annotated[str, mapped_column(primary_key=True)]
type PkTypes = int | str | date


class VisitStatus(Enum):
    primary = "Первичный"
    repeated = "Повторный"
    diagnose = "Диагноз"


class DoctorSpecialty(Enum):
    allergist = "Аллерголог"
    dermatologist = "Дерматолог"
    cardiologist = "Кардиолог"
    neurologist = "Невролог"
    ophthalmologist = "Офтальмолог"
    pediatrician = "Педиатр"
    psychotherapist = "Психотерапевт"
    resuscitator = "Реаниматолог"
    dentist = "Стоматолог"
    surgeon = "Хирург"


class DoctorCategory(Enum):
    second = "Вторая"
    first = "Первая"
    higher = "Высшая"


class Gender(Enum):
    male = "Мужчина"
    female = "Женщина"
