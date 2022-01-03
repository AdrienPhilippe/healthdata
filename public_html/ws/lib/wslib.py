#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import os

from lib import dbhandler
from lib.exceptions import DestNotSpecified, ValueNotFound


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
    if not "HTTP_X_AUTH" in data:
        retour["MISSING PASSWORD"] = "Missing identification to perform this action"
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

    try:
        status_code = dbhandler.deleteRessource(connection, dest)
        response["text"] = "Ressource delete successfull"
    except ValueNotFound :
        response["text"] = "Ressource not found"
    except DestNotSpecified:
        response["text"] = "No ressource specified"        

    response["content"] = dbhandler.readRessource(connection)

    return response

def getAccessRights(connection, user, pwd):
    user = dbhandler.getUser(connection, user, pwd)
    return user
    rights = user["rights"]
    return rights