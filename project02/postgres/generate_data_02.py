from faker import Faker
import names
from random import randint
import random
import string
import csv
import psycopg2
import json
import itertools
import re
import numpy as np
fake = Faker()

        #######CREATE DOCTORS, ADD TO DOCTORS TABLE IN POSTGRES#######

np.random.seed(10)
dr_names = []
for i in range(1, 101):
    dr_names.append('Dr. ' + str(fake.name()))

doctors_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\doctorsinsert.sql", "w")

doctor_insert_statement = 'INSERT INTO Doctors (Doctor_Name) VALUES '
for elements in dr_names:
    doctor_statement = doctor_insert_statement+'('+"'"+str(elements)+"'"+')'+';'
    print(doctor_statement, file = doctors_sql)

        ######CREATE PATIENTS, ADD TO PATIENTS TABLE IN POSTGRES#######
# I generated the other 35 patients from the doctors table in Postgres to ensure
# that 35% of doctors are patients using the following syntax:

# INSERT INTO Patients (Doctor_ID, Patient_Name)
# SELECT Doctor_ID, Doctor_Name FROM Doctors WHERE Doctor_ID < 36;


print(f'Name: {faker.name()}')
print(f'First name: {faker.first_name()}')
print(f'Last name: {faker.last_name()}')

customer_first_names = []
for i in range(1, 10001):
    customer_names.append(str(fake.first_name()))

customer_last_names = []
for i in range(1, 10001):
    customer_names.append(str(fake.last_name()))

customer_ages = []
for i in range(1,10001):
    customer_age = np.random.randint(0, 80)
    customer_ages.append(customer_age)

male_female=['M', 'F']
customer_genders = []
for i in range(1,10001):
    customer_gender = random.choice(male_female)
    customer_genders.append(customer_gender)

customer_handicaps = []
for i in range(1,10001):
    customer_handicap = np.random.randint(0, 35)
    customer_handicaps.append(customer_handicap)


patients_sql = open(r"C:\Users\User\Desktop\COMP-3421-1\customersinsert.sql", "w")

patient_insert_statement = 'INSERT INTO Patients (Customer_Name) VALUES '
for a,b in zip(doctor_ids, patient_names):
    patient_table_insert = patient_insert_statement+'('+"'"+str(a)+"'"+', '+"'"+str(b)+"'"+')'+';'
    print(patient_table_insert, file = patients_sql)

         ######CREATE ILLNESSES, ADD TO ILLNESS TABLE IN POSTGRES#######
# illness = 'illness'
# list_of_illnesses = []
# for i in range(1,1001):
#     list_of_illnesses.append(illness+'_'+str(i))
#
# illness_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\illnessinsert.sql", "w")
#
# illness_insert_statement = 'INSERT INTO Illness (Illness_Name) VALUES '
#
# for elements in list_of_illnesses:
#     illness_statement = illness_insert_statement+'('+"'"+str(elements)+"'"+')'+';'
#     print(illness_statement, file = illness_sql)
# #
# #             ####CREATE INTS FOR THE Patient_Doctor_Relation TABLE####
# first_35_doctor_ids = []
# for i in range(1,72):
#     first_35_doctor_ids.append(i)
#
# first_34_patient_ids = []
# for i in range(1,35):
#     first_34_patient_ids.append(i)
#
# next_36_patient_ids = []
# for i in range(1,37):
#     next_36_patient_ids.append(i)
# first_34_patient_ids = first_34_patient_ids[::-1]
# next_36_patient_ids = next_36_patient_ids[::-1]
#
# first_70_patients = first_34_patient_ids+next_36_patient_ids
#
# doctor_patient_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\doctor_patient_insert.sql", "w")
#
# dp_insert_statement = 'INSERT INTO Patient_Doctor_Relation (Treating_Doctor_ID, Patient_ID) VALUES '
#
# for (a, b) in zip(first_35_doctor_ids, first_70_patients):
#     dp_print = dp_insert_statement + '(' + "'" + str(a) + "'" + ', ' +  "'" + str(b) + "'" + ')'+';'
#     print(dp_print, file = doctor_patient_sql)
#
# list_of_patient_ids = []
# for i in range(36,10001):
#         patient_multiplier = np.random.randint(1,5)
#         list_of_patient_ids.append([i]*patient_multiplier)
#
# unpack_remaining_patient_ids = [item for sublist in list_of_patient_ids for item in sublist]
# list_of_doctor_ids = []
# for i in range(1,len(unpack_remaining_patient_ids)):
#     list_of_doctor_ids.append(np.random.randint(1,101))
#
#
# doctor_patient_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\doctor_patient_insert.sql", "a")
#
# dp_insert_statement = 'INSERT INTO Patient_Doctor_Relation (Treating_Doctor_ID, Patient_ID) VALUES '
#
# for (a, b) in zip(list_of_doctor_ids, unpack_remaining_patient_ids):
#     dp_print = dp_insert_statement + '(' + "'" + str(a) + "'" + ', ' +  "'" + str(b) + "'" + ')'+';'
#     print(dp_print, file = doctor_patient_sql)
#
#         ####CREATE INTS FOR THE Patient_Illness_Relation TABLE####
#
# patient_illnesses =[]
# list_of_illnesses_ints = []
# for i in range(1,1001):
#     list_of_illnesses_ints.append(i)
# for i in range(1,9800):
#     number_of_illnesses = np.random.randint(0, 4)
#     illness_selection = np.random.choice(list_of_illnesses_ints, number_of_illnesses, replace=False)
#     patient_illnesses.append(illness_selection)
#
# unpack_patient_illnesses = [item for sublist in patient_illnesses for item in sublist]
#
# patient_id_nums = []
# for i in range(1,len(unpack_patient_illnesses)):
#     patient_id_multiplier = np.random.randint(0, 4)
#     patient_id_nums.append([i]*patient_id_multiplier)
#     unpack_patient_id_nums = [item for sublist in patient_id_nums for item in sublist]
#     if len(unpack_patient_id_nums) == len(unpack_patient_illnesses):
#         break
# patient_illness_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\patient_illness_insert.sql", "w")
#
# pi_insert_statement = 'INSERT INTO Patient_Illness_Relation (Illness_ID, Patient_ID) VALUES '
#
# for (a, b) in zip(unpack_patient_illnesses, unpack_patient_id_nums):
#     pi_print = pi_insert_statement + '(' + "'" + str(a) + "'" + ', ' +  "'" + str(b) + "'" + ')'+';'
#     print(pi_print, file = patient_illness_sql)
#
#     ####CREATE INTS AND TREATMENTS FOR THE Patient_Treatment_Relation TABLE####
#
# treatment_id_nums=[]
# for i in range(1,len(unpack_patient_id_nums)+1):
#     treatment_id_nums.append(i)
#
# patient_treatment_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\patient_treatment_insert.sql", "w")
#
# pt_insert_statement = 'INSERT INTO Patient_Treatment_Relation (Patient_ID, Treatment_ID) VALUES '
#
# for (a, b) in zip(unpack_patient_id_nums,treatment_id_nums):
#     pt_print = pt_insert_statement + '(' + "'" + str(a) + "'" + ', ' +  "'" + str(b) + "'" + ')'+';'
#     print(pt_print, file = patient_treatment_sql)
#
#         #######CREATE TREATMENTS, ADD TO TREATMENTS TABLE IN POSTGRES#######
#
# treatment = 'Magical_Beans'
# list_of_treatments = []
# list_of_comments = []
#
# for i in range(1,len(unpack_patient_id_nums)+1):
#     list_of_treatments.append(treatment+'_'+str(i))
#
# comment_1 = 'take twice daily'
# comment_2 = 'take with food'
# comment_3 = 'do not mix with alcohol'
# comment_4 = 'shot adminstered in arm'
# comment_5 = 'over the counter'
# comments = [comment_1, comment_2, comment_3, comment_4, comment_5]
# for i in range(1,len(unpack_patient_id_nums)+1):
#     list_of_comments.append(comments[np.random.randint(0,5)])
#
#
# treatments_sql = open(r"C:\Users\User\nosql-db\docker\postgres\postgres\examples\treatmentsinsert.sql", "w")
#
# treatment_insert_statement = 'INSERT INTO Treatment (Treatment_Name, Comment) VALUES '
#
# for (a, b) in zip(list_of_treatments, list_of_comments):
#     treatment_print = treatment_insert_statement + '(' + "'" + str(a) + "'" + ', ' +  "'" + str(b) + "'" + ')'+';'
#     print(treatment_print, file = treatments_sql)
