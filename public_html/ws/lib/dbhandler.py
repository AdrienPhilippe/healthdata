#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors

from lib.exceptions import DestNotSpecified, ValueNotFound, RessourceAlreadyExists, RessourceDoesNotExist


#Connexion database
def connect():
    """[summary]

    Returns:
        pymysql.connections.Connection: connection established with the SQL database
    """
    connection = pymysql.connect(host='localhost',
                                user='menchit_SEV5204E',
                                password='8g2DaJd4',
                                database='menchit_SEV5204E',
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection


# Lecture contenu table Patients
def readPatient(connection, email, pwd=None):
    query = "SELECT * FROM `Patients` WHERE `email` = '{}'".format(email)
    if pwd is not None : query += " AND `password` = PASSWORD('{}')".format(pwd)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return result

def readPatientId(connection, id):
    query = "SELECT * FROM `Patients` WHERE `id_patient` = '{}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return result

def getAssignedDoctor(connection, email):
    patient = readPatient(connection, email)
    query = "SELECT `id_doctor` FROM `Relations` WHERE `id_patient` = {}".format(patient["id_patient"])

    with connection.cursor() as cursor:
        cursor.execute(query)
        ids_doctor = cursor.fetchall()

    result = []
    for id in ids_doctor:
        query = "SELECT * FROM `Doctors` WHERE id_doctor = {}".format(id)
        cursor.execute(query)
        result.append(cursor.fetchone())
    
    return result

def createPatient(connection, patient):
    if None in patient :
        raise DestNotSpecified("No ressource to create")

    with connection.cursor() as cursor:
        res = readPatient(connection, patient["email"])
        if res is not None:
            raise RessourceAlreadyExists("Ressource already exist")

        keys = ", ".join(["`" + str(key) + "`" for key in patient.keys()])
        values = ", ".join(["'" + str(value) + "'" for value in patient.values()])

        query = "INSERT INTO `Patients` ({}) VALUES ({});".format(keys,values)
        cursor.execute(query)
        query = "UPDATE `Patients` SET `password` = PASSWORD('{}') WHERE `email`='{}'".format(patient["password"], patient["email"])
        cursor.execute(query)

    connection.commit()
    return 1

# Lecture contenu table Doctors
def readDoctor(connection, email, pwd=None):
    query = "SELECT * FROM `Doctors` WHERE `email` = '{}'".format(email)
    if pwd is not None : query += " AND `password` = PASSWORD('{}')".format(pwd)
    with connection.cursor() as cursor:
        cursor.execute(query)
    result = cursor.fetchone()
    return result


def createDoctor(connection, doctor):
    if None in doctor :
        raise DestNotSpecified("No ressource to create")

    with connection.cursor() as cursor:
        res = readDoctor(connection, doctor["email"])
        if res is not None:
            raise RessourceAlreadyExists("Ressource already exist")

        keys = ", ".join(["`" + key + "`" for key in doctor.keys()])
        values = ", ".join(["'" + value + "'" for value in doctor.values()])

        query = "INSERT INTO `Doctors` ({}) VALUES ({});".format(keys,values)
        cursor.execute(query)
        query = "UPDATE `Doctors` SET `password` = PASSWORD('{}') WHERE `email`='{}'".format(doctor["password"], doctor["email"])
        cursor.execute(query)

    connection.commit()
    return 1

def getPatientForDoctor(connection, mail, pwd):
    with connection.cursor() as cursor:
        doc = readDoctor(connection, mail, pwd)
        doc_id = doc["id_doctor"]

        query = "SELECT * FROM `Relations` WHERE `id_doctor` = {}".format(doc_id)
        cursor.execute(query)
        id_patients = [line["id_patient"] for line in cursor.fetchall()]

        result = []
        for id_patient in id_patients:
            result.append(readPatientId(connection, id_patient))
    return result

def createPatientData(connection, httpData, user_id):
    with connection.cursor() as cursor:
        httpData["id_patient"] = user_id
        keys = ", ".join(["`" + str(key) + "`" for key in httpData.keys()])
        values = ", ".join(["'" + str(value) + "'" for value in httpData.values()])
        query = "INSERT INTO `Datas` ({}) VALUES ({});".format(keys,values)
        cursor.execute(query)
    connection.commit()
    return getPatientData(connection, readPatientId(connection,user_id)["email"])

def getPatientData(connection, mail, pwd=None):
    patient = readPatient(connection, mail, pwd)
    id_patient = patient["id_patient"]
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Datas` WHERE `id_patient` = {} ORDER BY `timestamp` DESC".format(id_patient)
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def getPatientWithoutDoctor(connection):
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Patients` WHERE `id_patient` NOT IN (SELECT `id_patient` FROM `Relations`)"
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def getPatientDataId(connection, mail, pwd=None, id_data=None):
    patient = readPatient(connection, mail, pwd)
    id_patient = patient["id_patient"]
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Datas` WHERE `id_patient` = {}".format(id_patient)
        if id_data is not None : query += " AND `id_data` = {}".format(id_data)
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def getPatientDataWithTimestamp(connection, mail, pwd=None, timestamp=None):
    patient = readPatient(connection, mail, pwd)
    id_patient = patient["id_patient"]
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Datas` WHERE `id_patient` = {}".format(id_patient)
        if timestamp is not None : query += " AND `timestamp` = '{}'".format(timestamp)
        cursor.execute(query)
        result = cursor.fetchone()
    return result

def updatePatientData(connection, httpData, user_id, data_id):
    with connection.cursor() as cursor:
        httpData["id_patient"] = user_id
        keys = ["`" + str(key) + "`" for key in httpData.keys()]
        values = ["'" + str(value) + "'" for value in httpData.values()]
        query = "UPDATE `Datas` SET "
        modif = []
        for k,v in zip(keys, values):
            modif.append("{} = {}".format(str(k),str(v)))
        modif = ", ".join(modif)
        query += modif + " WHERE `id_data` = {}".format(data_id)
        cursor.execute(query)
    connection.commit()
    return getPatientDataId(connection, readPatientId(connection,user_id)["email"], id_data=data_id)

def deleteData(connection, id_data):
    with connection.cursor() as cursor:
        query = "DELETE FROM `Datas` WHERE `id_data` = {}".format(id_data)
        cursor.execute(query)
    connection.commit()
    return 1

def createMessage(connection, id_patient, id_doctor, timestamp, body):
    with connection.cursor() as cursor:
        query = "INSERT INTO `Messages`\
            (`timestamp`, `id_patient`, `id_doctor`, `body`) \
            VALUES ('{}','{}','{}','{}')".format(timestamp, id_patient, id_doctor, body)
        cursor.execute(query)
    connection.commit()
    return 1

def getUserMessage(connection, id, type):
    query = "SELECT * FROM `Messages` WHERE `{}` = {}".format(type, id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def newRelation(connection, id_doctor, id_patient):
    with connection.cursor() as cursor:
        query = "INSERT INTO `Relations`(`id_doctor`, `id_patient`) VALUES ({},{})".format(id_doctor, id_patient)
        cursor.execute(query)
    connection.commit()
    return "Done"