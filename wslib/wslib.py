#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import pymysql.cursors
import cgi

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
def testRequest():
    if os.environ['HTTP_ACCEPT'] == "*/*":  
        retour = {  "code": "MISSING_HEADER" ,
                    "texte": "Missing http accept header"}
        return json.dumps(retour)
    if not "application/json" in os.environ['HTTP_ACCEPT']: 
        retour = {  "code": "WRONG_FORMAT",
                    "texte": "Missing or wrong http accept format"}
        return json.dumps(retour)
    if not os.environ['REQUEST_METHOD'] == "GET": 
        retour = {  "code": "WRONG_METHOD",
                    "texte": "Request method must be GET}"}
        return json.dumps(retour)

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