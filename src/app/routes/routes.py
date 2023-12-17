from enum import Enum


class Routes(str, Enum):
    LOGIN = "/"
    REGISTER = "/register"
    ADMIN = "/admin"
    PATIENT = "patient"
    DOCTOR = "/doctor"
    HEAD_DOCTOR = "/head_doctor"
