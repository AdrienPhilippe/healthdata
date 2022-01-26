#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors

from lib.exceptions import DestNotSpecified, ValueNotFound, RessourceAlreadyExists, RessourceDoesNotExist

"""
This file is our library to exchange with the database. Our script will establish a connection and use this connection through their entire
lifetime. The functions below are extracting and changing informations in our database by constructing SQL queries and sending
them through the pymysql API.
"""

#Connexion database
def connect():
    """Establish a connection with the SQL database

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
    """Get the personnal informations on a patient with the given mail adress

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        email (string): mail adress of the requested user
        pwd (string, optional): password of the requested user, will not be used if not specified. Defaults to None.

    Returns:
        dict: personnal informations on the given patient
    """
    query = "SELECT * FROM `Patients` WHERE `email` = '{}'".format(email)
    if pwd is not None : query += " AND `password` = PASSWORD('{}')".format(pwd)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return result

def readPatientId(connection, id):
    """Get the personnal informations on a patient with the given id

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        id (int): id of the requested patient

    Returns:
        dict: personnal informations on the given patient
    """
    query = "SELECT * FROM `Patients` WHERE `id_patient` = '{}'".format(id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchone()
    return result

def getAssignedDoctor(connection, email):
    """Get the doctor bind to the given patient

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        email (string): email of the patient that will be bind to a new doctor

    Returns:
        dict: personnal informations on the doctor that is newly bind to the given patient
    """
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
    """Create a new patient in the database

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        patient (dict): contains all the informations needed to create a brand new patient in the database

    Raises:
        DestNotSpecified: if the dict patient is empty
        RessourceAlreadyExists: if the email given is already used

    Returns:
        int: status code
    """
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
    """Return personnal informations on the given doctor

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        email (string): email of the requested doctor
        pwd (string, optional): password of the requested doctor, not used if not specified. Defaults to None.

    Returns:
        dict: personnal informations on the requested doctor
    """
    query = "SELECT * FROM `Doctors` WHERE `email` = '{}'".format(email)
    if pwd is not None : query += " AND `password` = PASSWORD('{}')".format(pwd)
    with connection.cursor() as cursor:
        cursor.execute(query)
    result = cursor.fetchone()
    return result


def createDoctor(connection, doctor):
    """Create a new doctor in the database

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        doctor (dict): dict containing all the informations needed to create a brand new doctor

    Raises:
        DestNotSpecified: if the doctor dict is empty
        RessourceAlreadyExists: if the given mail adress is already used

    Returns:
        int: status code
    """
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
    """Get all the patients binded to the current doctor

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        mail (string): mail adress of the current doctor
        pwd (string): password of the current doctor

    Returns:
        list: list containing all the patients bind to the current doctor, a patient is a dict of personnal informations
    """
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

def createPatientData(connection, data, user_id):
    """Allow a patient to create data

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        data (dict): dict containing the values of the data's sample that needs to be added
        user_id (int): id of the current patient that is adding datas

    Returns:
        list: list of all the current patient's datas, a patient's data is a dict
    """
    with connection.cursor() as cursor:
        data["id_patient"] = user_id
        keys = ", ".join(["`" + str(key) + "`" for key in data.keys()])
        values = ", ".join(["'" + str(value) + "'" for value in data.values()])
        query = "INSERT INTO `Datas` ({}) VALUES ({});".format(keys,values)
        cursor.execute(query)
    connection.commit()
    return getPatientData(connection, readPatientId(connection,user_id)["email"])

def getPatientData(connection, mail, pwd=None):
    """Get all the given patient's data

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        mail (string): mail adress of the requested patient
        pwd (string, optional): password of the requested patient, not used if not specified. Defaults to None.

    Returns:
        list: list of requested patient's datas, a patient's data is a dict
    """
    patient = readPatient(connection, mail, pwd)
    id_patient = patient["id_patient"]
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Datas` WHERE `id_patient` = {} ORDER BY `timestamp` DESC".format(id_patient)
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def getPatientWithoutDoctor(connection):
    """Get all the patients that are not bind to a doctor

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database

    Returns:
        list: list of patients, a patients is a dict
    """
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Patients` WHERE `id_patient` NOT IN (SELECT `id_patient` FROM `Relations`)"
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def getPatientDataId(connection, mail, pwd=None, id_data=None):
    """Get a sample from a patient or all the samples of the patient

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        mail (string): mail adress of the requested patient
        pwd (string, optional): password of the requested patient, not used if not specified. Defaults to None.
        id_data (int, optional): id of the sample if we want to select only one sample, select all samples if not specified. Defaults to None.

    Returns:
        list: list of sample(s), a sample is a dict
    """
    patient = readPatient(connection, mail, pwd)
    id_patient = patient["id_patient"]
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Datas` WHERE `id_patient` = {}".format(id_patient)
        if id_data is not None : query += " AND `id_data` = {}".format(id_data)
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def getPatientDataWithTimestamp(connection, mail, pwd=None, timestamp=None):
    """Get a sample from a patient or all the samples of the patient

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        mail (string): mail adress of the requested patient
        pwd (string, optional): password of the requested patient, not used if not specified. Defaults to None.
        timestamp (int, optional): timestamp of the sample if we want to select only one sample, select all samples if not specified. Defaults to None.

    Returns:
        list: list of sample(s), a sample is a dict
    """
    patient = readPatient(connection, mail, pwd)
    id_patient = patient["id_patient"]
    with connection.cursor() as cursor:
        query = "SELECT * FROM `Datas` WHERE `id_patient` = {}".format(id_patient)
        if timestamp is not None : query += " AND `timestamp` = '{}'".format(timestamp)
        cursor.execute(query)
        result = cursor.fetchone()
    return result

def updatePatientData(connection, data, user_id, data_id):
    """Allow a patient to update his own samples

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        data (dict): contains the new values of the requested fields to update
        user_id (int): the id of the patient that wants to modify his datas
        data_id (int): the id of the sample that needs to be modified

    Returns:
        list: all the given patient's samples, a patient's sample is a dict
    """
    with connection.cursor() as cursor:
        data["id_patient"] = user_id
        keys = ["`" + str(key) + "`" for key in data.keys()]
        values = ["'" + str(value) + "'" for value in data.values()]
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
    """Allows a patient to delete his own samples

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        id_data (int): id of the sample that needs to be destroyed

    Returns:
        int: status code
    """
    with connection.cursor() as cursor:
        query = "DELETE FROM `Datas` WHERE `id_data` = {}".format(id_data)
        cursor.execute(query)
    connection.commit()
    return 1

def createMessage(connection, id_patient, id_doctor, timestamp, body):
    """Create a message in the message table

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        id_patient (int): id of the patient linked to the message
        id_doctor (int): if of the doctor linked to the message
        timestamp (string): date of the message
        body (string): text of the message

    Returns:
        int: status code
    """
    with connection.cursor() as cursor:
        query = "INSERT INTO `Messages`\
            (`timestamp`, `id_patient`, `id_doctor`, `body`) \
            VALUES ('{}','{}','{}','{}')".format(timestamp, id_patient, id_doctor, body)
        cursor.execute(query)
    connection.commit()
    return 1

def getUserMessage(connection, id, type):
    """return the messages of the given user

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        id (int): id of the user requesting his messages
        type (string): if the user is a "doctor" or a "patient"

    Returns:
        list: all the messages of the user, a message is a dict
    """
    query = "SELECT * FROM `Messages` WHERE `{}` = {}".format(type, id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def newRelation(connection, id_doctor, id_patient):
    """Bind a patient to the given doctor

    Args:
        connection (pymysql.connections.Connection): connection established with the SQL database
        id_doctor (int): id of the doctor implies in the binding
        id_patient (int): id of the patient that needs to be bind

    Returns:
        string: Done
    """
    with connection.cursor() as cursor:
        query = "INSERT INTO `Relations`(`id_doctor`, `id_patient`) VALUES ({},{})".format(id_doctor, id_patient)
        cursor.execute(query)
    connection.commit()
    return "Done"