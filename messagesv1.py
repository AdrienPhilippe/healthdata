#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json
import os

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

index = [ {'dest' :"Thomas", 'text' : "Hello Thomas !"},
        {'dest' :"Adrien", 'text' : "Hello Adrien !"},
        {'dest' :"cat", 'text' : "Meow"},
        {'dest' :"world", 'text' : "Hello plèbe !"}
]

#print message en fonction des urls
httpData = returnHttpData()
if not httpData:
    print(json.dumps(index)); exit()
else:
    l = [data for data in index if data['dest'] == httpData['dest']]
    if len(l) == 0:
        retour = {  "code": "WRONG_DEST",
                    "texte": "Only 'Thomas', 'Adrien', 'cat', 'world' are allowed"}
                    #changer quand données confidentielles
        print(json.dumps(retour)); exit()
    else:
        print(json.dumps(l[0])); exit() 
