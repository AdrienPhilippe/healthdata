#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import json
import os

import pymysql.cursors


# Fonction retournant un dictionnaire qui contient les données envoyées via la requête http
def returnHttpData():
    formData = cgi.FieldStorage()
    httpData = {}
    httpDataKeys = []
    httpDataKeys = list(formData)
    for key in httpDataKeys:
        httpData[key] = (formData[key].value)
    return httpData

#Test validité request HTTP
def errors_handler():
    retour = {}
    if os.environ['HTTP_ACCEPT'] == "*/*":  
        retour["MISSING_HEADER"] = "Missing http accept header"
    if not "application/json" in os.environ['HTTP_ACCEPT']: 
        retour["WRONG_FORMAT"] =  "Missing or wrong http accept format"
    if not os.environ['REQUEST_METHOD'] == "GET": 
        retour["WRONG_METHOD"] = "Request method must be GET"
    return retour

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

#Lecture contenu table messages
def readRessource(connection):
    with connection:

        with connection.cursor() as cursor:
            httpData = returnHttpData()
            if not httpData:
                message = ""
            else:
                dest = httpData["dest"]
                message = "WHERE `dest` = '"+dest+"'"
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `messages` "+message
                cursor.execute(sql)
            result = cursor.fetchall()
            return result
