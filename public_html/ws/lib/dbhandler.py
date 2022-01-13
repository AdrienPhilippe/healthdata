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

def updateRessource(connection, ressource = None):
    with connection.cursor() as cursor:
        if None in ressource :
            raise DestNotSpecified("No ressource to update")

        dest, message = ressource

        res = readRessource(connection, dest)
        if len(res) == 0:
            raise RessourceDoesNotExist("This ressource does not exist")
        
        query = "UPDATE messages SET `text` = '" + message + "' WHERE `dest` = '" + dest + "'"
        cursor.execute(query)

    connection.commit()
    return 1