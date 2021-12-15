#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json
import os
import pymysql.cursors

# Permet d’activer les retours d’erreur du module CGI
cgitb.enable()
# Fonction retournant un dictionnaire qui contient les données envoyées via la requête http
def returnHttpData():
    formData = cgi.FieldStorage()
    httpData = {}
    httpDataKeys = []
    httpDataKeys = list(formData)
    for key in httpDataKeys:
        httpData[key] = (formData[key].value)
    return httpData

print("Content-type: application/json\n")

if os.environ['HTTP_ACCEPT'] == "*/*":  
    retour = {  "code": "MISSING_HEADER" ,
                "texte": "Missing http accept header"}
    print(json.dumps(retour)); exit()
if not "application/json" in os.environ['HTTP_ACCEPT']: 
    retour = {  "code": "WRONG_FORMAT",
                "texte": "Missing or wrong http accept format"}
    print(json.dumps(retour)); exit()
if not os.environ['REQUEST_METHOD'] == "GET": 
    retour = {  "code": "WRONG_METHOD",
                "texte": "Request method must be GET}"}
    print(json.dumps(retour)); exit()

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='philipad_SEV5204E',
                             password='m3R84Qri',
                             database='philipad_SEV5204E',
                             charset='utf8mb4',
                             port=3306,
                             cursorclass=pymysql.cursors.DictCursor)

with connection:

    with connection.cursor() as cursor:
        # Read a single record
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
        print(result)
    
connection.close()