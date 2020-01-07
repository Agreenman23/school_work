--TO CREATE THE NEW DATABASE FOR SMALLTOWN HOSPITAL

--C:\Users\User>docker exec -it nosql-postgres /bin/bash
--root@nosql-postgres:/# su - postgres
--postgres@nosql-postgres:~$ createdb SMALLTOWN_HOSPITAL
--postgres@nosql-postgres:~$ psql SMALLTOWN_HOSPITAL

--TO CREATE THE DOCTORS TABLE WITH THE REQUIRED FIELDS
CREATE TABLE Doctors (
Doctor_ID serial PRIMARY KEY,
Doctor_Name varchar(255) NOT NULL
);

--ADD DOCTORS INTO THE Doctors TABLE
--\i /app/postgres/examples/doctorsinsert.sql


--TO CREATE THE PATIENTS TABLE WITH THE REQUIRED FIELDS
--Added a Doctor_ID field here to distinguish patients that are doctors
CREATE TABLE Patients (
Patient_ID serial PRIMARY KEY,
Doctor_ID integer,
Patient_Name varchar(255) NOT NULL
);

--TO MOVE 35 DOCTORS FROM DOCTORS TABLE TO PATIENTS TABLE WITHIN POSTGRES
INSERT INTO Patients (Doctor_ID, Patient_Name)
SELECT Doctor_ID, Doctor_Name FROM Doctors WHERE Doctor_ID < 36;

--ADD THE REST OF THE PATIENTS INTO THE Patients TABLE
--\i /app/postgres/examples/patientsinsert.sql

--TO CREATE THE ILLNESS TABLE WITH THE REQUIRED FIELDS
CREATE TABLE Illness (
Illness_ID serial PRIMARY KEY,
Illness_Name varchar(255) NOT NULL
);

--ADD ILLNESSES INTO THE Illness TABLE
--\i /app/postgres/examples/illnessinsert.sql


--TO CREATE THE TREATMENT TABLE WITH THE REQUIRED FIELDS
CREATE TABLE Treatment (
Treatment_ID serial PRIMARY KEY,
Treatment_Name varchar(255) NOT NULL,
Comment varchar(255)
);

--ADD TREATMENTS INTO THE Treatment TABLE
--\i /app/postgres/examples/treatmentsinsert.sql

CREATE TABLE Patient_Doctor_Relation(
Patient_Doctor_ID serial PRIMARY KEY,
Treating_Doctor_ID integer REFERENCES Doctors(Doctor_ID),
Patient_ID integer REFERENCES Patients(Patient_ID)
);

--ADD INTS INTO THE Doctor_Patient_Relation TABLE
--\i /app/postgres/examples/doctor_patient_insert.sql

CREATE TABLE Patient_Illness_Relation(
Patient_Illness_ID serial PRIMARY KEY,
Illness_ID integer REFERENCES Illness(Illness_ID),
Patient_ID integer REFERENCES Patients(Patient_ID)
);

--\i /app/postgres/examples/patient_illness_insert.sql

CREATE TABLE Patient_Treatment_Relation(
Patient_Treatment_ID serial PRIMARY KEY,
Patient_ID integer REFERENCES Patients(Patient_ID),
Treatment_ID integer REFERENCES Treatment(Treatment_ID)
);

--ADD INTS INTO THE Illness_Treatment_Relation TABLE
--\i /app/postgres/examples/patient_treatment_insert.sql
