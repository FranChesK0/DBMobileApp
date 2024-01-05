import logging
from datetime import date

from faker import Faker
from faker.providers import DynamicProvider

from misc import get_logger, LoggerName
from database.queries import insert, select
from database.database_types import VisitStatus, DoctorSpecialty, DoctorCategory, Gender
from database.procedures_functions import insert_procedures, InsertProcedure, select_functions

logger: logging.Logger = get_logger(LoggerName.DATABASE)
RAW_DATA = {
    "visit_status": list(VisitStatus),
    "doctor_specialty": list(DoctorSpecialty),
    "doctor_category": list(DoctorCategory),
    "gender": list(Gender),
    "purpose": ["Профосмотр", "Медосмотр", "Консультация", "Лечение", "Больничный лист"],
    "diagnose": ["Ангина", "Анемия", "Аппендицит", "Артроз", "Астигматизм", "Бронхит",
                 "Врожденный вывих бедра", "Гастрит", "Гипертония", "Кариес", "Катаракта", "Трахеит",
                 "Тревожность"]
}


async def fill_tables(visit_number: int = 0,
                      doctor_number: int = 0,
                      patient_number: int = 0,
                      section_number: int = 0,
                      street_number: int = 0) -> None:
    fake = _setup_faker()

    purposes: list[insert_procedures.Purpose] = _get_purposes()
    diagnoses: list[insert_procedures.Diagnose] = _get_diagnoses()
    sections: list[insert_procedures.Section] = _get_sections(fake, section_number, street_number)
    await _insert_models(purposes + diagnoses + sections)

    patients: list[insert_procedures.Patient] = await _get_patients(fake, patient_number)
    doctors: list[insert_procedures.Doctor] = await _get_doctors(fake, doctor_number)
    await _insert_models(patients + doctors)

    visits: list[insert_procedures.Visit] = await _get_visits(fake, visit_number)
    await _insert_models(visits)

    logger.info(f"Database filled with data")


def _get_purposes() -> list[insert_procedures.Prupose]:
    purposes = []
    for purpose in RAW_DATA.get("purpose"):
        purposes.append(insert_procedures.Purpose(purpose=purpose))
    return purposes


def _get_diagnoses() -> list[insert_procedures.Diagnose]:
    diagnoses = []
    for diagnose in RAW_DATA.get("diagnose"):
        diagnoses.append(insert_procedures.Diagnose(diagnose=diagnose))
    return diagnoses


def _get_sections(fake: Faker, section_num: int, street_num: int) -> list[insert_procedures.Section]:
    sections = []
    for _ in range(section_num):
        addresses = [fake.street_name() for _ in range(street_num)]
        sections.append(insert_procedures.Section(addresses=addresses))
    return sections


async def _get_patients(fake: Faker, num: int) -> list[insert_procedures.Patient]:
    patients = []
    sections: list[select_functions.SectionsAddresses.returns] = await select(select_functions.SectionsAddresses())
    for _ in range(num):
        gender = fake.gender()
        last_name = fake.last_name_male() if gender == Gender.male else fake.last_name_female()
        middle_name = fake.middle_name_male() if gender == Gender.male else fake.middle_name_female()
        first_name = fake.first_name_male() if gender == Gender.male else fake.first_name_female()
        full_name = f"{last_name} {first_name} {middle_name}"
        section = fake.random_element(elements=sections)
        patients.append(insert_procedures.Patient(medical_card=str(fake.numerify(text="%%%%%%")),
                                                  insurance_policy=str(fake.numerify(text="%%%%%%%%%%%")),
                                                  full_name=full_name,
                                                  gender=gender,
                                                  birth_date=fake.date_of_birth(),
                                                  street=fake.random_element(elements=section.addresses),
                                                  house=fake.building_number()))
    return patients


async def _get_doctors(fake: Faker, num: int) -> list[insert_procedures.Doctor]:
    doctors = []
    sections: list[select_functions.SectionsNumbers.returns] = await select(select_functions.SectionsNumbers())
    for _ in range(num):
        section = fake.random_element(elements=sections)
        last_name = fake.last_name()
        middle_name = fake.middle_name()
        first_name = fake.first_name()
        full_name = f"{last_name} {first_name} {middle_name}"
        doctors.append(insert_procedures.Doctor(service_number=str(fake.numerify(text="%%%%%")),
                                                full_name=full_name,
                                                specialty=fake.doctor_specialty(),
                                                category=fake.doctor_category(),
                                                rate=int(fake.numerify(text="%%%%%")),
                                                section=section.number))
    return doctors


async def _get_visits(fake: Faker, num: int) -> list[insert_procedures.Visit]:
    visits = []
    patients: list[select_functions.PatientsIdsNames.returns] = await select(select_functions.PatientsIdsNames())
    doctors: list[select_functions.DoctorsIdsNames.returns] = await select(select_functions.DoctorsIdsNames())
    for _ in range(num):
        patient = fake.random_element(elements=patients)
        doctor = fake.random_element(elements=doctors)
        diagnose = fake.random_element(elements=RAW_DATA.get("diagnose"))
        purpose = fake.random_element(elements=RAW_DATA.get("purpose"))
        visits.append(insert_procedures.Visit(number=fake.random_int(1, 40),
                                              visit_date=fake.date_between(start_date=date(2023, 1, 1),
                                                                           end_date=date(2024, 12, 31)),
                                              medical_card=patient.id,
                                              service_number=doctor.id,
                                              diagnose=diagnose,
                                              purpose=purpose,
                                              status=fake.visit_status()))
    return visits


def _setup_faker() -> Faker:
    fake = Faker("ru_RU")
    for name, elements in RAW_DATA.items():
        fake.add_provider(DynamicProvider(provider_name=name, elements=elements))
    return fake


async def _insert_models(ins_proc: list[InsertProcedure]) -> None:
    for procedure in ins_proc:
        await insert(procedure)
