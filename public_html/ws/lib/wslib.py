#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cgi
import json
import os

from lib import dbhandler


# Fonction retournant un dictionnaire qui contient les données envoyées via la requête http
def getHttpData(formData = cgi.FieldStorage()):
    httpData = {}
    httpDataKeys = list(formData)
    for key in httpDataKeys:
        httpData[key] = (formData[key].value)
    return httpData

#Test validité request HTTP
def getErrors(data = os.environ):
    retour = {}
    if data['HTTP_ACCEPT'] == "*/*":  
        retour["MISSING_HEADER"] = "Missing http accept header"
    if not "application/json" in data['HTTP_ACCEPT']: 
        retour["WRONG_FORMAT"] =  "Missing or wrong http accept format"
    if not data['REQUEST_METHOD'] in ["GET", "DELETE"]: 
        retour["WRONG_METHOD"] = "Request method must be GET or DELETE"
    return retour

def getDest(connection, dest = None):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    db_dest = dbhandler.readRessource(connection, dest)
    if len(db_dest) == 0:
        response["text"] = "Resource not found"
    elif dest == None:
        response["text"] = "Collection read successfull"
    else:
        response["text"] = "Dest read succesfull"

    response["content"] = db_dest
    
    return response

def deleteDest(connection, dest = None):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_DELETED"

    status_code = dbhandler.deleteRessource(connection, dest)

    if status_code == -2: # ressource not found
        response["text"] = "Ressource not found"
    elif status_code == -1: # no ressource to delete
        reponse["text"] = "No ressource specified"
    elif status_code == 1: # everything is ok
        response["text"] = "Ressource delete successfull"

    response["content"] = dbhandler.readRessource(connection)

    return response