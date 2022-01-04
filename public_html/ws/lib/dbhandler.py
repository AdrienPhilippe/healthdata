#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import pymysql.cursors

from lib.exceptions import DestNotSpecified, ValueNotFound, WrongPasswordOrUsername, RessourceAlreadyExists


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


def getUserRights(connection, user, password):
    with connection.cursor() as cursor:
        query = "SELECT `rights` FROM `users`\
        WHERE `loginUser` = '" + user + "' AND `pwdUser` = PASSWORD('" +\
        password + "')"

        cursor.execute(query)
        rights = cursor.fetchone()

    return rights

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

def createRessource(connection, ressource = None):
    with connection.cursor() as cursor:
        if None in ressource :
            raise DestNotSpecified("No ressource to create")

        dest, message = ressource

        res = readRessource(connection, dest)
        if len(res) > 0:
            raise RessourceAlreadyExists("Ressource already exist")

        query = "INSERT INTO `messages`(`dest`, `text`) VALUES ('" + dest + "','" + message + "')"
        cursor.execute(query)

    connection.commit()
    return 1