/* DROP */
DROP FUNCTION IF EXISTS select_doctors_ids_names();
DROP FUNCTION IF EXISTS select_patients_ids_names();
DROP FUNCTION IF EXISTS select_visits_by_patient(CHAR(6));
DROP FUNCTION IF EXISTS select_visits_by_doctor(CHAR(5));
DROP FUNCTION IF EXISTS select_doctors_by_section(integer);
DROP FUNCTION IF EXISTS select_patient_by_medical_card(CHAR(6));
DROP FUNCTION IF EXISTS select_doctor_by_service_number(CHAR(5));
DROP FUNCTION IF EXISTS select_sections_numbers();
DROP FUNCTION IF EXISTS select_sections_addresses();

DROP PROCEDURE IF EXISTS insert_section(VARCHAR);
DROP PROCEDURE IF EXISTS insert_diagnose(VARCHAR);
DROP PROCEDURE IF EXISTS insert_purpose(VARCHAR);
DROP PROCEDURE IF EXISTS insert_doctor(CHAR(5), VARCHAR, doctorspecialty, doctorcategory, integer, integer);
DROP PROCEDURE IF EXISTS insert_patient(CHAR(6), CHAR(11), VARCHAR, gender, date, VARCHAR, VARCHAR);
DROP PROCEDURE IF EXISTS insert_visit(integer, date, CHAR(6), CHAR(6), VARCHAR, VARCHAR, visitstatus);

DROP PROCEDURE IF EXISTS delete_section(integer);
DROP PROCEDURE IF EXISTS delete_diagnose(integer);
DROP PROCEDURE IF EXISTS delete_purpose(integer);
DROP PROCEDURE IF EXISTS delete_doctor(CHAR(5));
DROP PROCEDURE IF EXISTS delete_patient(CHAR(6));
DROP PROCEDURE IF EXISTS delete_visit(integer, date);

DROP VIEW IF EXISTS "statisticalTicket";

DROP TABLE IF EXISTS "visits";
DROP TABLE IF EXISTS "doctors";
DROP TABLE IF EXISTS "patients";
DROP TABLE IF EXISTS "sections";
DROP TABLE IF EXISTS "diagnoses";
DROP TABLE IF EXISTS "purposes";

DROP SEQUENCE IF EXISTS "section_id_seq";
DROP SEQUENCE IF EXISTS "diagnose_id_seq";

DROP TYPE IF EXISTS "gender";
DROP TYPE IF EXISTS "doctorspecialty";
DROP TYPE IF EXISTS "doctorcategory";
DROP TYPE IF EXISTS "visitstatus";

/* TYPES */
CREATE TYPE gender AS ENUM ('мужчина', 'женщина');
CREATE TYPE doctorspecialty AS ENUM (
	'аллерголог',
	'дерматолог',
	'кардиолог',
	'невролог',
	'офтальмолог',
	'педиатр',
	'психотерапевт',
	'реаниматолог',
	'стоматолог',
	'хирург'
);
CREATE TYPE doctorcategory AS ENUM ('вторая', 'первая', 'высшая');
CREATE TYPE visitstatus AS ENUM ('первичный', 'повторный', 'диагноз');

/* TABLES */
CREATE SEQUENCE section_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
CREATE TABLE "public"."sections" (
	"id" integer DEFAULT nextval('section_id_seq') NOT NULL,
	"addresses" VARCHAR NOT NULL,
	CONSTRAINT "sections_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE SEQUENCE diagnose_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
CREATE TABLE "public"."diagnoses" (
	"id" integer DEFAULT nextval('diagnose_id_seq') NOT NULL,
	"diagnose" VARCHAR NOT NULL,
	CONSTRAINT "diagnoses_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

DROP SEQUENCE IF EXISTS "purpose_id_seq";
CREATE SEQUENCE purpose_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;
CREATE TABLE "public"."purposes" (
	"id" integer DEFAULT nextval('purpose_id_seq') NOT NULL,
	"purpose" VARCHAR NOT NULL,
	CONSTRAINT "purposes_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE TABLE "public"."doctors" (
	"serviceNumber" CHAR(5) NOT NULL,
	"fullName" VARCHAR NOT NULL,
	"specialty" doctorspecialty NOT NULL,
	"category" doctorcategory NOT NULL,
	"rate" integer NOT NULL,
	"sectionId" integer,
	CONSTRAINT "doctors_pkey" PRIMARY KEY ("serviceNumber")
) WITH (oids = false);

CREATE TABLE "public"."patients" (
	"medicalCard" CHAR(6) NOT NULL,
	"insurancePolicy" CHAR(11) NOT NULL,
	"fullName" VARCHAR NOT NULL,
	"gender" gender NOT NULL,
	"birthDate" date NOT NULL,
	"street" VARCHAR NOT NULL,
	"house" VARCHAR NOT NULL,
	"sectionId" integer,
	CONSTRAINT "patients_pkey" PRIMARY KEY ("medicalCard")
) WITH (oids = false);

CREATE TABLE "public"."visits" (
	"number" integer NOT NULL,
	"date" date NOT NULL,
	"medicalCard" CHAR(6) NOT NULL,
	"serviceNumber" CHAR(5) NOT NULL,
	"diagnoseId" integer,
	"purposeId" integer,
	"status" visitstatus NOT NULL,
	CONSTRAINT "visits_pkey" PRIMARY KEY ("number", "date")
) WITH (oids = false);

/* FOREIGN KEYS */
ALTER TABLE ONLY "public"."doctors" ADD CONSTRAINT "doctors_sectionId_fkey" FOREIGN KEY ("sectionId") REFERENCES sections("id") ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."patients" ADD CONSTRAINT "patients_sectionId_fkey" FOREIGN KEY ("sectionId") REFERENCES sections("id") ON DELETE SET NULL NOT DEFERRABLE;

ALTER TABLE ONLY "public"."visits" ADD CONSTRAINT "visits_diagnoseId_fkey" FOREIGN KEY ("diagnoseId") REFERENCES diagnoses("id") ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."visits" ADD CONSTRAINT "visits_medicalCard_fkey" FOREIGN KEY ("medicalCard") REFERENCES patients("medicalCard") ON DELETE CASCADE NOT DEFERRABLE;
ALTER TABLE ONLY "public"."visits" ADD CONSTRAINT "visits_purposeId_fkey" FOREIGN KEY ("purposeId") REFERENCES purposes("id") ON DELETE SET NULL NOT DEFERRABLE;
ALTER TABLE ONLY "public"."visits" ADD CONSTRAINT "visits_serviceNumber_fkey" FOREIGN KEY ("serviceNumber") REFERENCES doctors("serviceNumber") ON DELETE CASCADE NOT DEFERRABLE;

/* VIEWS */
CREATE VIEW "public"."statisticalTicket"
	AS SELECT v."number", v."date", v."medicalCard", pat."fullName" as "patientFullName", pat."street", pat."house", pat."sectionId", v."serviceNumber", doc."fullName" as "doctorFullName", v."purposeId", pur."purpose", v."status", v."diagnoseId", diag."diagnose"
	FROM visits v, doctors doc, patients pat, purposes pur, diagnoses diag
	WHERE v."medicalCard" = pat."medicalCard" and v."serviceNumber" = doc."serviceNumber" and v."purposeId" = pur."id" and v."diagnoseId" = diag."id";

/* Procedures */
	/* INSERT */
CREATE PROCEDURE insert_section(addresses VARCHAR)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			INSERT INTO sections
			("addresses")
			VALUES (addresses);
		END;
	$$;

CREATE PROCEDURE insert_diagnose(new_diagnose VARCHAR)
	LANGUAGE plpgsql
	AS $$
		DECLARE
			diagnose_exists boolean;
		BEGIN
			SELECT EXISTS INTO diagnose_exists (SELECT 1 FROM diagnoses WHERE "diagnose" = new_diagnose LIMIT 1);

			IF NOT diagnose_exists THEN
				INSERT INTO diagnoses ("diagnose") VALUES (new_diagnose);
			END IF;
		END;
	$$;

CREATE PROCEDURE insert_purpose(new_purpose VARCHAR)
	LANGUAGE plpgsql
	AS $$
		DECLARE
			purpose_exists boolean;
		BEGIN
			SELECT EXISTS INTO purpose_exists (SELECT 1 FROM purposes WHERE "purpose" = new_purpose LIMIT 1);

			IF NOT purpose_exists THEN
				INSERT INTO purposes ("purpose") VALUES (new_purpose);
			END IF;
		END;
	$$;

CREATE PROCEDURE insert_doctor(
		service_number CHAR(5),
		full_name VARCHAR,
		specialty doctorspecialty,
		category doctorcategory,
		rate integer,
		section_id integer
	)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			INSERT INTO doctors
			("serviceNumber", "fullName", "specialty", "category", "rate", "sectionId")
			VALUES (service_number, full_name, specialty, category, rate, section_id);
		END;
	$$;

CREATE PROCEDURE insert_patient(
		medical_card CHAR(6),
		insurance_policy CHAR(11),
		full_name VARCHAR,
		patient_gender gender,
		birth_date date,
		street VARCHAR,
		house VARCHAR
	)
	LANGUAGE plpgsql
	AS $$
		DECLARE
			section_id integer;
		BEGIN
			SELECT s."id" INTO section_id from sections s WHERE street = ANY(string_to_array(s."addresses", ';'));

			INSERT INTO patients
			("medicalCard", "insurancePolicy", "fullName", "gender", "birthDate", "street", "house", "sectionId")
			VALUES (medical_card, insurance_policy, full_name, patient_gender, birth_date, street, house, section_id);
		END;
	$$;

CREATE PROCEDURE insert_visit(
		visit_number integer,
		visit_date date,
		medical_card CHAR(6),
		service_number CHAR(5),
		visit_diagnose VARCHAR,
		visit_purpose VARCHAR,
		status visitstatus
	)
	LANGUAGE plpgsql
	AS $$
		DECLARE
			diagnose_exists boolean;
			purpose_exists boolean;
			diagnose_id integer;
			purpose_id integer;
		BEGIN
			SELECT EXISTS INTO diagnose_exists (SELECT 1 FROM diagnoses WHERE "diagnose" = visit_diagnose LIMIT 1);
			SELECT EXISTS INTO purpose_exists (SELECT 1 FROM purposes WHERE "purpose" = visit_purpose LIMIT 1);

			IF NOT diagnose_exists  THEN
				CALL insert_diagnose(visit_diagnose);
			END IF;
			IF NOT purpose_exists THEN
				CALL insert_purpose(visit_purpose);
			END IF;

			SELECT "id" INTO diagnose_id FROM diagnoses WHERE visit_diagnose = "diagnose";
			SELECT "id" INTO purpose_id FROM purposes WHERE visit_purpose = "purpose";

			INSERT INTO visits
			("number", "date", "medicalCard", "serviceNumber", "diagnoseId", "purposeId", "status")
			VALUES (visit_number, visit_date, medical_card, service_number, diagnose_id, purpose_id, status);
		END;
	$$;

	/* DELETE */
CREATE PROCEDURE delete_section(section_id integer)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			DELETE FROM sections WHERE "id" = section_id;
		END;
	$$;

CREATE PROCEDURE delete_diagnose(diagnose_id integer)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			DELETE FROM diagnoses WHERE "id" = diagnose_id;
		END;
	$$;

CREATE PROCEDURE delete_purpose(purpose_id integer)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			DELETE FROM purposes WHERE "id" = purpose_id;
		END;
	$$;

CREATE PROCEDURE delete_doctor(service_number CHAR(6))
	LANGUAGE plpgsql
	AS $$
		BEGIN
			DELETE FROM doctors WHERE "serviceNumber" = service_number;
		END;
	$$;

CREATE PROCEDURE delete_patient(medical_card CHAR(6))
	LANGUAGE plpgsql
	AS $$
		BEGIN
			DELETE FROM patients WHERE "medicalCard" = medical_card;
		END;
	$$;

CREATE PROCEDURE delete_visit(visit_number integer, visit_date date)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			DELETE FROM visits WHERE "number" = visit_number and "date" = visit_date;
		END;
	$$;

/* Functions */
CREATE FUNCTION select_doctors_ids_names()
	RETURNS TABLE (
				"number" CHAR(5),
				"name" VARCHAR
			)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			RETURN QUERY SELECT "serviceNumber" as "number", "fullName" as "name" FROM doctors;
		END;
	$$;

CREATE FUNCTION select_patients_ids_names()
	RETURNS TABLE (
					"number" CHAR(6),
					"name" VARCHAR
				)
		LANGUAGE plpgsql
		AS $$
			BEGIN
				RETURN QUERY SELECT "medicalCard" AS "number", "fullName" as "name" FROM patients;
			END;
		$$;

CREATE OR REPLACE FUNCTION select_visits_by_patient(medical_card CHAR(6))
	RETURNS TABLE(
		"visit_number" integer,
		"visit_date" date,
		"doctor_specialty" doctorspecialty,
		"doctor_full_name" VARCHAR,
		"visit_purpose" VARCHAR,
		"visit_status" visitstatus,
		"visit_diagnose" VARCHAR
		)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			RETURN QUERY SELECT v."number" as "visit_number", v."date" as "visit_date", doc."specialty" as "doctor_specialty", doc."fullName" as "doctor_full_name", p."purpose" as "visit_purpose", v."status" as "visit_status", diag."diagnose" as "visit_diagnose"
				FROM visits v, doctors doc, purposes p, diagnoses diag
				WHERE v."medicalCard" = medical_card and v."serviceNumber" = doc."serviceNumber" and v."purposeId" = p."id" and v."diagnoseId" = diag."id"
				ORDER BY "visit_date", "visit_number";
		END;
	$$;

CREATE OR REPLACE FUNCTION select_visits_by_doctor(service_number CHAR(5))
	RETURNS TABLE(
		"visit_number" integer,
		"visit_date" date,
		"patient_full_name" VARCHAR,
		"patient_gender" gender,
		"patient_section" integer,
		"visit_purpose" VARCHAR,
		"visit_status" visitstatus,
		"visit_diagnose" VARCHAR
		)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			RETURN QUERY SELECT v."number" as "visit_number", v."date" as "visit_date", pat."fullName" as "patient_full_name", pat."gender" as "patient_gender", pat."sectionId" as "patient_section", pur."purpose" as "visit_purpose", v."status" as "visit_status", d."diagnose" as "visit_diagnose"
				FROM visits v, patients pat, purposes pur, diagnoses d
				WHERE v."serviceNumber" = service_number and v."medicalCard" = pat."medicalCard" and v."purposeId" = pur."id" and v."diagnoseId" = d."id"
				ORDER BY "visit_date", "visit_number";
		END;
	$$;

CREATE OR REPLACE FUNCTION select_doctors_by_section(section_id integer)
	RETURNS TABLE(
		"service_number" CHAR(5),
		"full_name" VARCHAR,
		"doctor_specialty" doctorspecialty,
		"doctor_category" doctorcategory
		)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			RETURN QUERY SELECT "serviceNumber" as "service_number", "fullName" as "full_name", "specialty" as "doctor_specialty", "category" as "doctor_category"
				FROM doctors
				WHERE "sectionId" = section_id
				ORDER BY "doctor_specialty", "full_name";
		END;
	$$;

CREATE OR REPLACE FUNCTION select_patient_by_medical_card(patient_medical_card CHAR(6))
	RETURNS TABLE(
		"medical_card" CHAR(6),
		"insurance_policy" CHAR(11),
		"full_name" VARCHAR,
		"patient_gender" gender,
		"birth_date" date,
		"patient_street" VARCHAR,
		"patient_house" VARCHAR,
		"section" integer
		)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			RETURN QUERY SELECT "medicalCard" as "medical_card", "insurancePolicy" as "insurance_policy", "fullName" as "full_name", "gender" as "patient_gender", "birthDate" as "birth_date", "street" as "patient_street", "house" as "patient_house", "sectionId" as "section"
				FROM patients WHERE "medicalCard" = patient_medical_card;
		END;
	$$;

CREATE OR REPLACE FUNCTION select_doctor_by_service_number(doctor_service_number CHAR(5))
	RETURNS TABLE(
		"service_number" CHAR(5),
		"full_name" VARCHAR,
		"doctor_specialty" doctorspecialty,
		"doctor_category" doctorcategory,
		"doctor_rate" integer,
		"section" integer
		)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			RETURN QUERY SELECT "serviceNumber" as "service_number", "fullName" as "full_name", "specialty" as "doctor_specialty", "category" as "doctor_category", "rate" as "doctor_rate", "sectionId" as "section" 
				FROM doctors WHERE "serviceNumber" = doctor_service_number;
		END;
	$$;

CREATE OR REPLACE FUNCTION select_sections_numbers()
	RETURNS TABLE(
		"number" integer
		)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			RETURN QUERY SELECT "id" as "number" FROM sections ORDER BY "number";
		END;
	$$;

CREATE OR REPLACE FUNCTION select_sections_addresses()
	RETURNS TABLE(
		"section_addresses" TEXT[]
		)
	LANGUAGE plpgsql
	AS $$
		BEGIN
			RETURN QUERY SELECT string_to_array("addresses", ';') as "sectoin_addresses" FROM sections;
		END;
	$$;