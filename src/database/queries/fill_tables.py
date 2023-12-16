from datetime import date

from faker import Faker
from faker.providers import DynamicProvider

from misc import LoggerName, get_logger
from database import database_types, models, queries

logger = get_logger(LoggerName.DATABASE)
RAW_DATA = {
    "visit_status": list(database_types.VisitStatus),
    "doctor_specialty": list(database_types.DoctorSpecialty),
    "doctor_category": list(database_types.DoctorCategory),
    "gender": list(database_types.Gender),
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
    fake = Faker("ru_RU")
    for name, elements in RAW_DATA.items():
        fake.add_provider(DynamicProvider(provider_name=name, elements=elements))

    purposes = _get_purposes()
    diagnoses = _get_diagnoses()
    sections = _get_sections(fake, section_number, street_number)
    await queries.insert(purposes + diagnoses + sections)

    patients = await _get_patients(fake, patient_number)
    doctors = await _get_doctors(fake, doctor_number)
    logger.debug(type(patients))
    logger.debug(type(doctors))
    await queries.insert(patients + doctors)

    visits = await _get_visits(fake, visit_number)
    await queries.insert(visits)

    await queries.insert(doctors + visits)
    logger.info(f"Database filled with data")


def _get_purposes() -> list[models.Purpose]:
    purposes = []
    for purpose in RAW_DATA.get("purpose"):
        purposes.append(models.Purpose(purpose=purpose))
    return purposes


def _get_diagnoses() -> list[models.Diagnose]:
    diagnoses = []
    for diagnose in RAW_DATA.get("diagnose"):
        diagnoses.append(models.Diagnose(diagnose=diagnose))
    return diagnoses


def _get_sections(fake: Faker, section_num: int, street_num: int) -> list[models.Section]:
    sections = []
    for _ in range(section_num):
        addresses = ";".join([fake.street_name() for _ in range(street_num)])
        sections.append(models.Section(addresses=addresses))
    return sections


async def _get_patients(fake: Faker, num: int) -> list[models.Patient]:
    sections = await queries.select_all(models.Section)
    patients = []
    for _ in range(num):
        gender = fake.gender()
        last_name = fake.last_name_male() if gender == database_types.Gender.male else fake.last_name_female()
        middle_name = fake.middle_name_male() if gender == database_types.Gender.male else fake.middle_name_female()
        first_name = fake.first_name_male() if gender == database_types.Gender.male else fake.first_name_female()
        full_name = f"{last_name} {first_name} {middle_name}"
        section = fake.random_element(elements=sections)
        patients.append(models.Patient(medical_card=str(fake.numerify(text="%%%%%%%%%%%%")),
                                       insurance_policy=str(fake.numerify(text="%%%%%%%%%%%")),
                                       full_name=full_name,
                                       gender=gender,
                                       birth_date=fake.date_of_birth(),
                                       street=fake.random_element(elements=section.addresses.split(";")),
                                       house=fake.building_number(),
                                       section_id=section.id))
    return patients


async def _get_doctors(fake: Faker, num: int) -> list[models.Doctor]:
    doctors = []
    sections = await queries.select_all(models.Section)
    for _ in range(num):
        section = fake.random_element(elements=sections)
        last_name = fake.last_name()
        middle_name = fake.middle_name()
        first_name = fake.first_name()
        full_name = f"{last_name} {first_name} {middle_name}"
        doctors.append(models.Doctor(service_number=str(fake.numerify(text="%%%%%%")),
                                     full_name=full_name,
                                     specialty=fake.doctor_specialty(),
                                     category=fake.doctor_category(),
                                     rate=int(fake.numerify(text="%%%%%")),
                                     section_id=section.id))
    return doctors


async def _get_visits(fake: Faker, num: int) -> list[models.Visit]:
    visits = []
    patients = await queries.select_all(models.Patient)
    doctors = await queries.select_all(models.Doctor)
    diagnoses = await queries.select_all(models.Diagnose)
    purposes = await queries.select_all(models.Purpose)
    for _ in range(num):
        patient = fake.random_element(elements=patients)
        doctor = fake.random_element(elements=doctors)
        diagnose = fake.random_element(elements=diagnoses)
        purpose = fake.random_element(elements=purposes)
        visits.append(models.Visit(visit_number=fake.random_int(1, 40),
                                   visit_date=fake.date_between(start_date=date(2023, 1, 1),
                                                                end_date=date(2024, 12, 31)),
                                   medical_card=patient.medical_card,
                                   service_number=doctor.service_number,
                                   diagnose_id=diagnose.id,
                                   purpose_id=purpose.id,
                                   status=fake.visit_status()))
    return visits
