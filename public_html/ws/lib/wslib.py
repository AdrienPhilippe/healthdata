#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json
import os
import sys
from datetime import datetime

from lib import dbhandler
from lib.exceptions import (DestNotSpecified, RessourceAlreadyExists,
                            RessourceDoesNotExist, ValueNotFound)


# initialize the whole environment
def init():
    # # Permet d’activer les retours d’erreur du module CGI
    cgitb.enable()

    print("Content-type: application/json\n")

    # store the http method to use
    httpMethod = os.environ['REQUEST_METHOD']

    # get the user
    username, pwd = os.environ["HTTP_X_AUTH"].split(":")

    #Test validité request HTTP
    errors = getErrors()
    if not len(errors) == 0:
        print(json.dumps(errors))
        sys.exit()

    rights = "all"

    # get http data
    httpData = returnHttpData()

    #Connexion database
    connection = dbhandler.connect()

    return connection, httpMethod, httpData, username, pwd

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

# def getDest(connection, rights, dest = None):
#     response = {}
#     response["code"] = "OPERATION_OK"
#     response["operation"] = "RESSOURCE_READ"

#     if rights is None :
#         response["text"] = "You need to be logged in order to perform this operation"
#         return response

#     if not ("read" in rights.values() or "all" in rights.values()):
#         response["text"] = "You need higher authorization in order to perform this action"
#         return response

#     db_dest = dbhandler.readRessource(connection, dest)
    
#     if len(db_dest) == 0:
#         response["text"] = "Resource not found"
#     elif dest == None:
#         response["text"] = "Collection read successfull"
#     else:
#         response["text"] = "Dest read succesfull"

#     response["content"] = db_dest
    
#     return response

# def deleteDest(connection, rights, dest = None):
#     response = {}
#     response["code"] = "OPERATION_OK"
#     response["operation"] = "RESSOURCE_DELETED"

#     if rights is None :
#         response["text"] = "You need to be logged in order to perform this operation"
#         return response

#     if not ("delete" in rights.values() or "all" in rights.values()):
#         response["text"] = "You need higher authorization in order to perform this action"
#         return response

#     try:
#         status_code = dbhandler.deleteRessource(connection, dest)
#         response["text"] = "Ressource delete successfully"
#     except ValueNotFound :
#         response["text"] = "Ressource not found"
#     except DestNotSpecified:
#         response["text"] = "No ressource specified"        

#     response["content"] = dbhandler.readRessource(connection)

#     return response

# def createDest(connection, rights, dest = None, message = None):
#     response = {}
#     response["code"] = "OPERATION_OK"
#     response["operation"] = "RESSOURCE_CREATED"

#     if rights is None :
#         response["text"] = "You need to be logged in order to perform this operation"
#         return response

#     if not ("create" in rights.values() or "all" in rights.values()):
#         response["text"] = "You need higher authorization in order to perform this action"
#         return response

#     try:
#         status_code = dbhandler.createPatient(connection, [dest, message])
#         response["text"] = "Ressource created successfully"
#     except DestNotSpecified:
#         response["text"] = "You need to specify a dest to create"
#     except RessourceAlreadyExists:
#         response["text"] = "This dest already exist in the database"   

#     # response["content"] = dbhandler.readRessource(connection)
#     response["content"] = "greate"

#     return response

# def updateDest(connection, rights, dest = None, message = None):
#     response = {}
#     response["code"] = "OPERATION_OK"
#     response["operation"] = "RESSOURCE_UPDATED"

#     if rights is None:
#         response["text"] = "You need to be logged in order to perform this operation"
#         return response
#     if not ("update" in rights.values() or "all" in rights.values()):
#         response["text"] = "You need higher authorization in order to perform this action"
#         return response

#     try:
#         status_code = dbhandler.updateRessource(connection, [dest, message])
#         response["text"] = "Ressource updated successfully"
#     except DestNotSpecified :
#         response["text"] = "Dest not defined"
#     except RessourceDoesNotExist : 
#         response["text"] = "This ressource does not exist"

#     response["content"] = dbhandler.readRessource(connection)

#     return response


def createPatient(connection, user):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_CREATED"
    data_needed = ["name", "firstname", "email", "password", "age", "height", "birthdate", "sex"]
    user_is_complete = True
    answer = ""

    for data in data_needed:
        if data not in user.keys():
            user_is_complete = False
            answer += "{} is missing. ".format(data)
    if not user_is_complete:
        response["text"] = answer
        return response

    try:
        dbhandler.createPatient(connection, user)
        response["text"] = "Ressource created successfully"
    except DestNotSpecified:
        response["text"] = "You need to specify a dest to create"
    except RessourceAlreadyExists:
        response["text"] = "This dest already exist in the database"   

    response["content"] = "Operation successfull"

    return response

def createDoctor(connection, user):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_CREATED"
    data_needed = ["name", "firstname", "email", "password"]
    user_is_complete = True
    answer = ""

    for data in data_needed:
        if data not in user.keys():
            user_is_complete = False
            answer += "{} is missing. ".format(data)
    if not user_is_complete:
        response["text"] = answer
        return response

    try:
        dbhandler.createDoctor(connection, user)
        response["text"] = "Ressource created successfully"
    except DestNotSpecified:
        response["text"] = "You need to specify a dest to create"
    except RessourceAlreadyExists:
        response["text"] = "This dest already exist in the database"   

    response["content"] = "Operation successfull"

    return response

def getPatient(connection, log_info):
    mail,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    datas = dbhandler.readPatient(connection, mail, pwd)
    if not datas:
        response["text"] = "User not found."
    else:
        response["content"] = datas
    
    return response

def getDataDoctor(connection, log_info):
    mail,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    datas = dbhandler.readDoctor(connection, mail, pwd)
    if not datas:
        response["text"] = "User not found."
    else:
        response["content"] = datas
    
    return response

def createPatientData(connection, httpData, log_info):
    mail, pwd = log_info
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_CREATED"

    data_allowed = ["Weight", "Chest", "Abdomen", "Hip", "Heartbeat"]
    all_data_allowed = True
    answer = ""
    for data in httpData.keys() :
        if data not in data_allowed :
            all_data_allowed = False
            answer += "{} is not allowed. ".format(data)
    if not all_data_allowed :
        response["text"] = answer
        return response

    user = dbhandler.readPatient(connection, mail, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    httpData["timestamp"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    response["content"] = dbhandler.createPatientData(connection, httpData, user["id_patient"])
    return response

def updatePatientData(connection, httpData, log_info):
    mail,pwd = log_info
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_UPDATED"

    user = dbhandler.readPatient(connection, mail, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    if "id_data" not in httpData :
        response["text"] = "Which sample modify ?"
        return response
    id_data = httpData.pop("id_data")

    data_allowed = ["Weight", "Chest", "Abdomen", "Hip", "Heartbeat"]
    all_data_allowed = True
    answer = ""
    for data in httpData.keys() :
        if data not in data_allowed :
            all_data_allowed = False
            answer += "{} is not allowed. ".format(data)
    if not all_data_allowed :
        response["text"] = answer
        return response

    data = dbhandler.getPatientDataId(connection, user["email"], id_data=id_data)
    if not data : 
        response["text"] = "Wrong datas."
        return response

    response["content"] = dbhandler.updatePatientData(connection, httpData, user["id_patient"], id_data)
    return response


def getPatientsForDoctor(connection, httpData, log_info):
    mail,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    datas = dbhandler.getPatientForDoctor(connection, mail, pwd)
    if datas : response["content"] = datas
    else : response["content"] = "You do not have any patient."

    return response
