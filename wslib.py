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
def getErrors():
    if os.environ['HTTP_ACCEPT'] == "*/*":  
        retour = {  "code": "MISSING_HEADER" ,
                    "texte": "Missing http accept header"}
        print(json.dumps(retour)); exit()
    if not "application/json" in os.environ['HTTP_ACCEPT']: 
        retour = {  "code": "WRONG_FORMAT",
                    "texte": "Missing or wrong http accept format"}
        print(json.dumps(retour)); exit()
    if not os.environ['REQUEST_METHOD'] in ["GET", "DELETE"]: 
        retour = {  "code": "WRONG_METHOD",
                    "texte": "Request method must be GET}"}
        print(json.dumps(retour)); exit()

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
def readRessource(connection, dest=None):
    with connection:
        if dest is None:
            message = ""
        else:
            message = "WHERE `dest` = '"+dest+"'"
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `messages` "+message
            cursor.execute(sql)
        result = {"content": cursor.fetchall()}
        return result

#Delete contenu table messages
def deleteRessource(connection, dest=None):
    with connection:
        if dest is None:
            raise Exception("DELETE")
        else:
            message = "WHERE `dest` = '"+dest+"'"
        with connection.cursor() as cursor:
            sql = "DELETE * FROM `messages` "+message
            cursor.execute(sql)
    connection.commit(sql)