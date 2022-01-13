#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors

from lib.exceptions import DestNotSpecified, ValueNotFound, RessourceAlreadyExists, RessourceDoesNotExist


#Connexion database
def connect():
    connection = pymysql.connect(host='localhost',
                                user='menchit_SEV5204E',
                                password='8g2DaJd4',
                                database='menchit_SEV5204E',
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection


# def getUserRights(connection, user, password):
#     with connection.cursor() as cursor:
#         query = "SELECT `rights` FROM `users`\
#         WHERE `loginUser` = '" + user + "' AND `pwdUser` = PASSWORD('" +\
#         password + "')"

#         cursor.execute(query)
#         rights = cursor.fetchone()

#     return rights



# def deleteRessource(connection, ressource=None):
#     with connection.cursor() as cursor:
#         if ressource is None :
#             raise DestNotSpecified("No ressource to delete.")

#         res = readRessource(connection, ressource)
#         if len(res) == 0:
#             raise ValueNotFound("Ressource does not exist")

#         query = "DELETE FROM `messages` WHERE `dest` = '" + ressource + "'"
#         cursor.execute(query)

#     connection.commit()
#     return 1

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

    connection.commit()
    return 1

def getPatientForDoctor(connection, mail, pwd):
    with connection.cursor() as cursor:
        doc = readDoctor(connection, mail, pwd)
        if doc is None : return "You need to be logged in."
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
    if not patient:
        return "You need to be logged in."
    id_patient = patient["id_patient"]
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Datas` WHERE `id_patient` = {}".format(id_patient)
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def getPatientDataId(connection, mail, pwd=None, id_data=None):
    patient = readPatient(connection, mail, pwd)
    if not patient:
        return "You need to be logged in."
    id_patient = patient["id_patient"]
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Datas` WHERE `id_patient` = {}".format(id_patient)
        if id is not None : query += " AND `id_data` = {}".format(id_data)
        cursor.execute(query)
        result = cursor.fetchall()
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





# def updateRessource(connection, ressource = None):
#     with connection.cursor() as cursor:
#         if None in ressource :
#             raise DestNotSpecified("No ressource to update")

#         dest, message = ressource

#         res = readRessource(connection, dest)
#         if len(res) == 0:
#             raise RessourceDoesNotExist("This ressource does not exist")
        
#         query = "UPDATE messages SET `text` = '" + message + "' WHERE `dest` = '" + dest + "'"
#         cursor.execute(query)

#     connection.commit()
#     return 1