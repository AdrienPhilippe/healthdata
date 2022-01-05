#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import os

from lib import dbhandler
from lib.exceptions import DestNotSpecified, ValueNotFound, RessourceAlreadyExists, RessourceDoesNotExist


# Fonction retournant un dictionnaire qui contient les données envoyées via la requête http
def returnHttpData():
    formData = cgi.FieldStorage()
    httpData = {}
    httpDataKeys = []
    try : httpDataKeys = list(formData)
    except : httpDataKeys = list([])
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
    if not data['REQUEST_METHOD'] in ["GET", "DELETE", "POST", "PUT"]: 
        retour["WRONG_METHOD"] = "Request method must be GET, POST, DELETE or PUT"
    if not "HTTP_X_AUTH" in data:
        retour["MISSING PASSWORD"] = "Missing identification to perform this action"
    return retour

def getUserRights(connection, user, pwd):
    pwd = pwd.encode('ascii', 'surrogateescape').decode('unicode-escape')
    rights = dbhandler.getUserRights(connection, user, pwd)
    return rights

def getDest(connection, rights, dest = None):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    if rights is None :
        response["text"] = "You need to be logged in order to perform this operation"
        return response

    if not ("read" in rights.values() or "all" in rights.values()):
        response["text"] = "You need higher authorization in order to perform this action"
        return response

    db_dest = dbhandler.readRessource(connection, dest)
    
    if len(db_dest) == 0:
        response["text"] = "Resource not found"
    elif dest == None:
        response["text"] = "Collection read successfull"
    else:
        response["text"] = "Dest read succesfull"

    response["content"] = db_dest
    
    return response

def deleteDest(connection, rights, dest = None):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_DELETED"

    if rights is None :
        response["text"] = "You need to be logged in order to perform this operation"
        return response

    if not ("delete" in rights.values() or "all" in rights.values()):
        response["text"] = "You need higher authorization in order to perform this action"
        return response

    try:
        status_code = dbhandler.deleteRessource(connection, dest)
        response["text"] = "Ressource delete successfully"
    except ValueNotFound :
        response["text"] = "Ressource not found"
    except DestNotSpecified:
        response["text"] = "No ressource specified"        

    response["content"] = dbhandler.readRessource(connection)

    return response

def createDest(connection, rights, dest = None, message = None):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_CREATED"

    if rights is None :
        response["text"] = "You need to be logged in order to perform this operation"
        return response

    if not ("create" in rights.values() or "all" in rights.values()):
        response["text"] = "You need higher authorization in order to perform this action"
        return response

    try:
        status_code = dbhandler.createRessource(connection, [dest, message])
        response["text"] = "Ressource created successfully"
    except DestNotSpecified:
        response["text"] = "You need to specify a dest to create"
    except RessourceAlreadyExists:
        response["text"] = "This dest already exist in the database"   

    response["content"] = dbhandler.readRessource(connection)

    return response

def updateDest(connection, rights, dest = None, message = None):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_UPDATED"

    if rights is None:
        response["text"] = "You need to be logged in order to perform this operation"
        return response
    if not ("update" in rights.values() or "all" in rights.values()):
        response["text"] = "You need higher authorization in order to perform this action"
        return response

    try:
        status_code = dbhandler.updateRessource(connection, [dest, message])
        response["text"] = "Ressource updated successfully"
    except DestNotSpecified :
        response["text"] = "Dest not defined"
    except RessourceDoesNotExist : 
        response["text"] = "This ressource does not exist"

    response["content"] = dbhandler.readRessource(connection)

    return response