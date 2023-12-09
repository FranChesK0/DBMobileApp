from datetime import date

from faker import Faker
from faker.providers import DynamicProvider

from misc import LoggerName, get_logger
from database import database_types, models, queries

logger = get_logger(LoggerName.DATABASE)
RAW_DATA = [("visit_status", list(database_types.VisitStatus)),
            ("doctor_specialty", list(database_types.DoctorSpecialty)),
            ("doctor_category", list(database_types.DoctorCategory)),
            ("gender", list(database_types.Gender)),
            ("purpose", ["Scheduled examination", "Pains", "Emergency hospitalization"]),
            ("diagnose", ["Appendicitis", "Headaches", "Stomachaches"])]


def fill_tables(visit_number: int = 0,
                doctor_number: int = 0,
                patient_number: int = 0,
                section_number: int = 0,
                street_number: int = 0,
                diagnose_number: int = 0,
                purpose_number: int = 0) -> None:
    fake = Faker("ru_RU")
    for name, elements in RAW_DATA:
        fake.add_provider(DynamicProvider(provider_name=name, elements=elements))

    _fill_purpose_table(fake, purpose_number)
    _fill_diagnose_table(fake, diagnose_number)
    _fill_section_table(fake, section_number, street_number)
    _fill_patient_table(fake, patient_number)
    _fill_doctor_table(fake, doctor_number)
    _fill_visit_table(fake, visit_number)


def _fill_purpose_table(fake: Faker, num: int) -> None:
    purposes = []
    for _ in range(num):
        purposes.append(models.Purpose(purpose=fake.purpose()))
    queries.insert(purposes)


def _fill_diagnose_table(fake: Faker, num: int) -> None:
    diagnoses = []
    for _ in range(num):
        diagnoses.append(models.Diagnose(diagnose=fake.diagnose()))
    queries.insert(diagnoses)


def _fill_section_table(fake: Faker, section_num: int, street_num: int) -> None:
    sections = []
    for _ in range(section_num):
        addresses = ";".join([fake.street_name() for _ in range(street_num)])
        sections.append(models.Section(addresses=addresses))
    queries.insert(sections)


def _fill_patient_table(fake: Faker, num: int) -> None:
    patients = []
    for _ in range(num):
        gender = fake.gender()
        full_name = fake.name_male() if gender == database_types.Gender.male else fake.name_female()
        section = fake.random_element(elements=queries.select_all(models.Section))
        patients.append(models.Patient(medicalCard=str(fake.numerify(text="%%%%%%%%%%%%")),
                                       insurancePolicy=str(fake.numerify(text="%%%%%%%%%%%")),
                                       fullName=full_name,
                                       gender=gender,
                                       birthDate=fake.date_of_birth(),
                                       street=fake.random_element(elements=section.addresses.split(";")),
                                       house=fake.building_number(),
                                       section=section.id))
    queries.insert(patients)


def _fill_doctor_table(fake: Faker, num: int) -> None:
    doctors = []
    for _ in range(num):
        section = fake.random_element(elements=queries.select_all(models.Section))
        doctors.append(models.Doctor(serviceNumber=str(fake.numerify(text="%%%%%%")),
                                     fullName=fake.name(),
                                     specialty=fake.doctor_specialty(),
                                     category=fake.doctor_category(),
                                     rate=fake.numerify(text="%%%%%"),
                                     section=section.id))
    queries.insert(doctors)


def _fill_visit_table(fake: Faker, num: int) -> None:
    visits = []
    for _ in range(num):
        patient = fake.random_element(elements=queries.select_all(models.Patient))
        doctor = fake.random_element(elements=queries.select_all(models.Doctor))
        diagnose = fake.random_element(elements=queries.select_all(models.Diagnose))
        purpose = fake.random_element(elements=queries.select_all(models.Purpose))
        visits.append(models.Visit(visitNumber=fake.random_int(1, 40),
                                   visitDate=fake.date_between(start_date=date(2023, 1, 1),
                                                               end_date=date(2024, 12, 31)),
                                   medicalCard=patient.medicalCard,
                                   serviceNumber=doctor.serviceNumber,
                                   diagnose=diagnose.id,
                                   purpose=purpose.id,
                                   status=fake.visit_status()))
    queries.insert(visits)
