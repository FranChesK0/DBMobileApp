from enum import Enum
from typing import Annotated

from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(primary_key=True)]


class VisitStatus(Enum):
    done: "done"
    waiting: "waiting"
    delayed: "delayed"
    canceled: "canceled"


class DoctorSpecialty(Enum):
    allergist: "allergist"
    dermatologist: "dermatologist"
    cardiologist: "cardiologist"
    neurologist: "neurologist"
    ophthalmologist: "ophthalmologist"
    pediatrician: "pediatrician"
    psychotherapist: "psychotherapist"
    resuscitator: "resuscitator"
    dentist: "dentist"
    surgeon: "surgeon"


class DoctorCategory(Enum):
    second: "second"
    first: "first"
    higher: "higher"


class Gender(Enum):
    male: "male"
    female: "female"
