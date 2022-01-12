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
def readPatient(connection, email, pwd):
    query = "SELECT * FROM `Patients` WHERE `email` = '{}' AND `password` = '{}'".format(email,pwd)
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

        keys = ", ".join(["`" + key + "`" for key in patient.keys()])
        values = ", ".join(["'" + value + "'" for value in patient.values()])

        query = "INSERT INTO `Patients` ({}) VALUES ({});".format(keys,values)
        cursor.execute(query)

    connection.commit()
    return 1

# Lecture contenu table Doctors
def readDoctor(connection, email):
    query = "SELECT * FROM `Doctors` WHERE `email` = `{}`".format(email)
    with connection.cursor() as cursor:
        cursor.execute(query)
    result = cursor.first()
    return result


def createDoctor(connection, doctor):
    if None in doctor :
        raise DestNotSpecified("No ressource to create")

    with connection.cursor() as cursor:
        res = readDoctor(connection, doctor["email"])
        if len(res) > 0:
            raise RessourceAlreadyExists("Ressource already exist")

        for key,value in doctor.items():
            query = "INSERT INTO `Doctors`(`{}`) VALUES ('{}');".format(key,value)
            cursor.execute(query)

    connection.commit()
    return 1

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