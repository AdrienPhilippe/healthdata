#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json
from multiprocessing.sharedctypes import Value
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

    # store the http method to use
    httpMethod = os.environ['REQUEST_METHOD']

    # get the user
    username, pwd = os.environ["HTTP_X_AUTH"].split(":")

    #Test validité request HTTP
    errors = getErrors()
    if not len(errors) == 0:
        print(json.dumps(errors))
        sys.exit()


    #Connexion database
    connection = dbhandler.connect()

    return connection, httpMethod, username, pwd

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
    if not "action" in returnHttpData().keys():
        retour["MISSING_ACTION"] = "You need to specify an action to perform"
    return retour

def userLoggedIn(connection, email, pwd, type):
    if not type in {"patient", "doctor"}:
        raise ValueError("Wrong type")

    if type == "patient":
        user = dbhandler.readPatient(connection, email, pwd)
    elif type == "doctor":
        user = dbhandler.readDoctor(connection, email, pwd)
    return bool(user)
    

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
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    datas = dbhandler.readPatient(connection, email, pwd)
    if not datas:
        response["text"] = "User not found."
    else:
        response["content"] = datas
    
    return response

def getDoctor(connection, log_info):
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    datas = dbhandler.readDoctor(connection, email, pwd)
    if not datas:
        response["text"] = "User not found."
    else:
        response["content"] = datas
    
    return response

def createPatientData(connection, httpData, log_info):
    email, pwd = log_info
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

    user = dbhandler.readPatient(connection, email, pwd)
    if not user:
        response["text"] = "You need to be logged in."
        return response

    httpData["timestamp"] = datetime.now().strftime("%Y-%m%d %H:%M:%S")

    response["content"] = dbhandler.createPatientData(connection, httpData, user["id_patient"])
    return response

def deletePatientData(connection, httpData, log_info):
    mail, pwd = log_info
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_DELETED"

    user = dbhandler.readPatient(connection, mail, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    if "id_data" not in httpData :
        response["text"] = "Which sample delete ?"
        return response
    id_data = httpData.pop("id_data")

    sample = dbhandler.getPatientDataId(connection, mail, id_data=id_data)
    if not sample:
        response["text"] = "This sample does not exist"
        return response

    if not sample["id_patient"] == user["id_patient"]:
        response["text"] = "You do not have access to this sample."
        return response

    response["content"] = sample

    dbhandler.deleteData(connection, id_data)

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

    user = dbhandler.readDoctor(connection, mail, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    datas = dbhandler.getPatientForDoctor(connection, mail, pwd)
    if datas : response["content"] = datas
    else : response["content"] = "You do not have any patient."

    return response

def getPatientsDataForDoctor(connection, httpData, log_info):
    mail,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    doctor = dbhandler.readDoctor(connection, mail, pwd)
    if not doctor:
        response["text"] = "you need to be logged in"
        return response    

    if not "id_patient" in httpData:
        response["text"] = "Patient not specify"
        return response
    
    id_patient = httpData["id_patient"]
    patient = dbhandler.readPatientId(connection, id_patient)
    patients_allowed = getPatientsForDoctor(connection, httpData, log_info)["content"]
    if patient not in patients_allowed:
        response["text"] = 'You cannot acces this patient.'
        return response

    response["content"] = dbhandler.getPatientData(connection, patient["email"])
    return response


def patientSendMessage(connection, httpData, log_info):
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "MESSAGE_SEND"

    user = dbhandler.readPatient(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    if not "body" in httpData:
        response["text"] = "The message is empty"
        return response
    if not "email_doctor" in httpData:
        response["text"] = "No dest specified"
        return response

    timestamp = datetime.now().strftime("%Y-%m%d %H:%M:%S")

    doc = dbhandler.readDoctor(connection, httpData["email_doctor"])

    id_patient = user["id_patient"]
    id_doc = doc["id_doctor"]
    body = httpData["body"]
    dbhandler.createMessage(connection, id_patient, id_doc, timestamp, body)
    
    response["content"] = "Message sended."
    return response

def doctorSendMessage(connection, httpData, log_info):
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "MESSAGE_SEND"

    user = dbhandler.readDoctor(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    if not "body" in httpData:
        response["text"] = "The message is empty"
        return response
    if not "email_patient" in httpData:
        response["text"] = "No dest specified"
        return response

    timestamp = datetime.now().strftime("%Y-%m%d %H:%M:%S")

    patient = dbhandler.readPatient(connection, httpData["email_patient"])

    id_doctor = user["id_doctor"]
    id_patient = patient["id_patient"]
    body = httpData["body"]
    dbhandler.createMessage(connection, id_patient, id_doctor, timestamp, body)
    
    response["content"] = "Message sended."
    return response

def getPatientMessage(connection, log_info):
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "MESSAGE_READ"

    user = dbhandler.readPatient(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    messages = dbhandler.getUserMessage(connection, user["id_patient"], "id_patient")
    if messages : response["content"] = messages
    else : response["content"] = "You do not have any message."  

    return response

def getDoctorMessage(connection, log_info):
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "MESSAGE_READ"

    user = dbhandler.readDoctor(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    messages = dbhandler.getUserMessage(connection, user["id_doctor"], "id_doctor")
    if messages : response["content"] = messages
    else : response["content"] = "You do not have any message."    

    return response