#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("Content-type: application/json\n")

import os
import random
import sys

import names
import numpy as np
import pandas as pd
import pymysql
import pymysql.cursors

from lib.exceptions import ValueNotFound
from lib import dbhandler

def random_dates(start, end, n=252):

    start_u = start.value//10**9
    end_u = end.value//10**9

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')
try:
    df = pd.read_csv("bodyfat.csv")
except:
    raise ValueNotFound("Ressource does not exist")

df["id_patient"] = df.index + 1
df["Patient_name"] = [names.get_full_name() for i in range(len(df))]
df[['patient_name','patient_firstname']] = df.Patient_name.str.split(" ",expand=True,)
df["heartbeat"] = [random.randint(50,85) for i in range(len(df))]

start = pd.to_datetime('2021-01-01')
end = pd.to_datetime('2021-12-31')
df["timestamp"] = random_dates(start, end)

doc = [names.get_full_name() for i in range(10)]
df["Doctor"] = [random.choice(doc) for i in range(len(df))]
df['id_doctor'] = df.groupby(['Doctor'], sort=False).ngroup().add(1)
df[['doctor_name','doctor_firstname']] = df.Doctor.str.split(" ",expand=True,)
df = df.drop(columns=['Patient_name', 'Density', 'BodyFat', 'Neck', 'Thigh', 'Knee', 'Ankle', 'Biceps', 'Forearm', 'Wrist', 'Doctor'])
df = df.rename(columns={"Age": "age", 
                        "Height": "height", 
                        "Weight": "weight", 
                        "Chest": "chest", 
                        "Abdomen": "abdomen", 
                        "Hip": "hip"})
column_names = ["id_patient", "patient_name", "patient_firstname", "timestamp", "age", "height", "weight", "heartbeat", "chest", "abdomen", "hip", "id_doctor", "doctor_name", "doctor_firstname"]

df = df.reindex(columns=column_names)

Datas = df[["id_patient", "timestamp", "weight", "chest", "abdomen", "hip", "heartbeat"]]
Doctors = df[["id_doctor", "doctor_name", "doctor_firstname"]]
Patients = df[["id_patient", "patient_name", "patient_firstname", "age", "height"]]
Relations = df[["id_doctor", "id_patient"]]

connection = dbhandler.connect()
cursor = connection.cursor()

#Datas
DatasD = Datas.to_dict("records")
for dico in DatasD:
    keys = ", ".join(["`" + str(key) + "`" for key in dico.keys()])
    values = ", ".join(["'" + str(value) + "'" for value in dico.values()])

    query = "INSERT INTO `Patients` ({}) VALUES ({});".format(keys,values)


# #Doctors
# colsDoctors = "`,`".join([str(i) for i in Doctors.columns.tolist()])

# for i,row in Datas.iterrows():
#     sql = "INSERT INTO `Doctors` (`" +colsDatas + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
#     cursor.execute(sql, tuple(row))

#     connection.commit()

# #Patients
# colsPatients = "`,`".join([str(i) for i in Patients.columns.tolist()])

# for i,row in Patients.iterrows():
#     sql = "INSERT INTO `Patients` (`" +colsPatients + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
#     cursor.execute(sql, tuple(row))

#     connection.commit()

# #Relations
# colsRelations = "`,`".join([str(i) for i in Relations.columns.tolist()])

# for i,row in Relations.iterrows():
#     sql = "INSERT INTO `Relations` (`" +colsRelations + "`) VALUES (" + "%s,"*(len(row)-1) + "%s)"
#     cursor.execute(sql, tuple(row))

#     connection.commit()

connection.close()
