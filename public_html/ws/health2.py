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

try:
    df = pd.read_csv("Health_Thomas_Adrien.csv")
except:
    exit()

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
