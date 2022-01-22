#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors

from lib.exceptions import DestNotSpecified, ValueNotFound, WrongPasswordOrUsername, RessourceAlreadyCreated,RessourceNotSpecified, RessourceDoesNotExist


#Connexion database
def connect():
    connection = pymysql.connect(host='localhost',
                                user='philipad_SEV5204E',
                                password='m3R84Qri',
                                database='philipad_SEV5204E',
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

#Lecture contenu table messages
def readRessource(connection, ressource=None):
    query = "SELECT * FROM `messages`"
    if ressource is not None:
        query += "WHERE `dest` = '" + ressource + "'"

    with connection.cursor() as cursor:
        cursor.execute(query)
    result = cursor.fetchall()
    return result

def deleteRessource(connection, ressource=None):
    with connection.cursor() as cursor:
        if ressource is None :
            raise DestNotSpecified("No ressource to delete.")

        res = readRessource(connection, ressource)
        if len(res) == 0:
            raise ValueNotFound("Ressource does not exist")

        query = "DELETE FROM `messages` WHERE `dest` = '" + ressource + "'"
        cursor.execute(query)

    connection.commit()
    return 1

def getUser(connection, user, password):
    with connection.cursor() as cursor:
        sql = "SELECT `rights` FROM `users` \
        WHERE `loginUser` = '" + user + "' AND `pwdUser` = PASSWORD('" + \
        password + "')"
        cursor.execute(sql)
        rights = cursor.fetchone()
    return rights

def createRessource(connection, ressource = None):
    with connection.cursor() as cursor:
        if None in ressource:
            raise RessourceNotSpecified("Ressource not specified")

        dest, message = ressource

        if readRessource(connection, dest) != 0:
            raise RessourceAlreadyCreated("Ressource already exist")

        query = "INSERT INTO `messages` VALUES ('"+ dest +'","'+message+"')"
        cursor.execute(query)

    connection.commit()
    return 1

<<<<<<< Updated upstream
def updateRessource(connection, ressource = None):
    with connection.cursor() as cursor:
        if None in ressource :
            raise DestNotSpecified("No ressource to update")

        dest, message = ressource
=======
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
>>>>>>> Stashed changes

        res = readRessource(connection, dest)
        if len(res) == 0:
            raise RessourceDoesNotExist("This ressource does not exist")
        
        query = "UPDATE messages SET `text` = '" + message + "' WHERE `dest` = '" + dest + "'"
        cursor.execute(query)

    connection.commit()
<<<<<<< Updated upstream
    return 1
=======
    return 1

def getUserMessage(connection, id, type):
    query = "SELECT * FROM `Messages` WHERE `{}` = {}".format(type, id)
    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()
    return results

def newRelation(connection, id_doctor, id_patient):
    with connection.cursor as cursor:
        query = "INSERT INTO `Relations`(`id_doctor`, `id_patient`) VALUES ({},{})".format(id_doctor, id_patient)
        cursor.execute(query)
    connection.commit()
    return "Done"
>>>>>>> Stashed changes
