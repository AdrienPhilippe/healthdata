#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import os

from lib import dbhandler
from lib.exceptions import DestNotSpecified, ValueNotFound, RessourceNotSpecified, RessourceAlreadyCreated, RessourceDoesNotExist


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
    if not data['REQUEST_METHOD'] in ["GET", "DELETE", "POST", "PUT"]: 
        retour["WRONG_METHOD"] = "Request method must be GET, DELETE, POST"
    if not "HTTP_X_AUTH" in data:
        retour["MISSING PASSWORD"] = "Missing identification to perform this action"
    return retour

def getDest(connection, rights, dest = None):
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    if "read" in rights.values() or "all" in rights.values():

        db_dest = dbhandler.readRessource(connection, dest)
        if len(db_dest) == 0:
            response["text"] = "Resource not found"
        elif dest == None:
            response["text"] = "Collection read successfull"
        else:
            response["text"] = "Dest read succesfull"

        response["content"] = db_dest
    else:
        response["text"] = "User don't have rights to read database"
    
    return response

<<<<<<< Updated upstream
def deleteDest(connection, rights, dest = None):
=======
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

    httpData["timestamp"] = datetime.now().strftime("%d-%m-%Y")

    response["content"] = dbhandler.createPatientData(connection, httpData, user["id_patient"])
    return response

def deletePatientData(connection, httpData, log_info):
    mail, pwd = log_info
>>>>>>> Stashed changes
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_DELETED"

<<<<<<< Updated upstream
    if "all" in rights.values():
=======
    user = dbhandler.readPatient(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    if "id_data" not in httpData :
        response["text"] = "Which sample delete ?"
        return response
    id_data = httpData.pop("id_data")

    sample = dbhandler.getPatientDataId(connection, email, id_data=id_data)[0]
    if not sample:
        response["text"] = "This sample does not exist"
        return response

    if not sample["id_patient"] == user["id_patient"]:
        response["text"] = "You do not have access to this sample."
        return response

    response["content"] = sample
>>>>>>> Stashed changes

        try:
            status_code = dbhandler.deleteRessource(connection, dest)
            response["text"] = "Ressource delete successfull"
        except ValueNotFound :
            response["text"] = "Ressource not found"
        except DestNotSpecified:
            response["text"] = "No ressource specified"        

<<<<<<< Updated upstream
        response["content"] = dbhandler.readRessource(connection)
    else:
        response["text"] = "User don't have rights to delete database"
=======
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

def updatePatientDataWithTimestamp(connection, httpData, log_info):
    mail,pwd = log_info
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_UPDATED"

    user = dbhandler.readPatient(connection, mail, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    if "timestamp" not in httpData :
        response["text"] = "Which sample modify ?"
        return response
    timestamp = httpData.pop("timestamp")

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

    data = dbhandler.getPatientDataWithTimestamp(connection, user["email"], timestamp=timestamp)
    if not data : 
        response["text"] = "Wrong datas."
        return response

    response["content"] = dbhandler.updatePatientData(connection, httpData, user["id_patient"], data["id_data"])
    return response

def getPatientWithoutDoctor(connection, log_info):
    email, pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    user = dbhandler.readDoctor(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    datas = dbhandler.getPatientWithoutDoctor(connection)
    if datas : response["content"] = datas
    else : response["content"] = "You do not have any patient."

    return response    


def getPatientsForDoctor(connection, httpData, log_info):
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    user = dbhandler.readDoctor(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    datas = dbhandler.getPatientForDoctor(connection, email, pwd)
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
>>>>>>> Stashed changes

    return response

def getAccessRights(connection, user, pwd):
    pwd = pwd.encode("ascii", "surrogateescape").decode("unicode-escape")

    user = dbhandler.getUser(connection, user, pwd)
    return user

def createDest(connection, rights, dest = None, message = None):
    response = {}
    response["code"] = "OPERATION_OK"
<<<<<<< Updated upstream
    response["operation"] = "RESSOURCE_DELETED"
=======
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

    timestamp = datetime.now().strftime("%d-%m-%Y")

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
>>>>>>> Stashed changes

    if rights is None:
        response["text"] = "You need to be logged in order to perform this operation"
        return response
    if not ("create" in rights.values() or "all" in rights.values()):
        response["text"] = "You need higher authorization in order to perform this action"
        return response

<<<<<<< Updated upstream
    try:
        status_code = dbhandler.createRessource(connection, [dest, message])
        response["text"] = "Ressource delete successfull"
    except RessourceNotSpecified :
        response["text"] = "Ressource not specified"
    except RessourceAlreadyCreated:
        response["text"] = "Ressource already exist"        

        response["content"] = dbhandler.readRessource(connection)
    else:
        response["text"] = "User don't have rights to delete database"
=======
    timestamp = datetime.now().strftime("%d-%m-%Y")

    patient = dbhandler.readPatient(connection, httpData["email_patient"])
>>>>>>> Stashed changes

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

def addPatientToDoc(connection, httpData, log_info):
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "PATIENT_ADDED"

    user = dbhandler.readDoctor(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    if not "id_patient" in httpData:
        response["text"] = "No dest specified"
        return response

    patient = dbhandler.readPatientId(connection, httpData["id_patient"])
    if not patient:
        response["text"] = "Patient not found"
        return response

    response["content"] = dbhandler.newRelation(connection, user["id_doctor"], patient["id_patient"])
    return response