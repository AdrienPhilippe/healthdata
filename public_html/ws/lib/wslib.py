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



"""
This is the main library of the project. This is where all the actions are performed and managed. The security check
of the identification is made here and all the function return a response which contains informations on the
performed action and an error message or a content with all the informations requested.
"""

# initialize the whole environment
def init():
    """Initializing the environment by activating the CGI module and gathering all crucial informations
    needed to complete an execution of the backend program

    Returns:
        connection: connection established with the SQL database
        httpMethod: which http method was used when calling the API
        username: the username of the client calling the api
        pwd: the password of the client calling the api
    """
    # Permet d’activer les retours d’erreur du module CGI
    cgitb.enable()

    # store the http method to use
    httpMethod = os.environ['REQUEST_METHOD']

    # get the user
    username, pwd = os.environ["HTTP_X_AUTH"].split(":")

    #Connexion database
    connection = dbhandler.connect()

    return connection, httpMethod, username, pwd

# Fonction retournant un dictionnaire qui contient les données envoyées via la requête http
def returnHttpData():
    """Return the http data that are contained in a body or in the headers of the request

    Returns:
        httpData: dictionnary with all the informations passed when calling the api
    """
    formData = cgi.FieldStorage()
    httpData = {}
    httpDataKeys = []
    httpDataKeys = list(formData)
    for key in httpDataKeys:
        httpData[key] = (formData[key].value)
    return httpData

#Test validité request HTTP
def getErrors(data = os.environ):
    """Checking if the API was correctly called with good values headers

    Args:
        data (dictionnary, optional): The http variable of the environment (all the headers). Defaults to os.environ.

    Returns:
        retour: dictionnary which contains all the error on the header
    """
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
    """Check if the current user exists and gave the correct authentification infos

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        email (string): current user's mail adress
        pwd (string): current user's password
        type (string): can be doctor or patient to determine of the current user is a doctor or a patient


    Returns:
        bool: if the user exists in the databse and has the correct login infos
    """
    if not type in {"patient", "doctor"}:
        raise ValueError("Wrong type")

    if type == "patient":
        user = dbhandler.readPatient(connection, email, pwd)
    elif type == "doctor":
        user = dbhandler.readDoctor(connection, email, pwd)
    return bool(user)
    

def createPatient(connection, user):
    """Create a new patient with all his informations 

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        user (dict): dictionnary containing all the informations needed to create a patient with the righ names for the keys

    Returns:
        dict: return an error in the text field or a validation in the content field
    """
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_CREATED"

    # list of all the fields that are required to create a patient
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
        response["text"] = "You need to specify a profile to create"
    except RessourceAlreadyExists:
        response["text"] = "This profile already exist in the database"   

    response["content"] = "Operation successfull"

    return response

def createDoctor(connection, user):
    """Create a new doctor with all his informations 

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        user (dict): dictionnary containing all the informations needed to create a patient with the righ names for the keys

    Returns:
        dict: return an error in the text field or a validation in the content field
    """
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_CREATED"

    # list of all the fields that are required to create a doctor
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
        response["text"] = "You need to specify a profile to create"
    except RessourceAlreadyExists:
        response["text"] = "This profile already exist in the database"   

    response["content"] = "Operation successfull"

    return response

def getPatient(connection, log_info):
    """Get all the personnal informations on the current patient

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return an error in the text field or the informations on the current patient in the content field
    """
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
    """Get all the personnal informations on the current doctor

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return an error in the text field or the informations on the current doctor in the content field
    """
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
    """Allow a patient to create personnal datas, he can ommit to specify some fields.
    Ommitted fields will have a 0-value b default.

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        httpData (dict): contains the informations needed
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return an error in the text field or the current patient's datas in the content field
    """
    email, pwd = log_info
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_CREATED"

    # only those fields can be present in the httpData dict, other fields will trigger an error message
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

def getPatientData(connection, log_info):
    """[summary]

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return an error in the text field or the current patient's datas in the content field
    """
    email, pwd = log_info
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    user = dbhandler.readPatient(connection, email, pwd)
    if not user:
        response["text"] = "You need to be logged in."
        return response

    response["content"] = dbhandler.getPatientData(connection, email)
    return response

def deletePatientData(connection, httpData, log_info):
    """Allow a patient to delete a sample of his datas

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        httpData (dict): contains the informations needed
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return an error in the text field or the sample that was destroyed in the content field
    """
    email, pwd = log_info
    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_DELETED"

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

    dbhandler.deleteData(connection, id_data)

    return response

def updatePatientData(connection, httpData, log_info):
    """Allow a patient to update a sample in his own datas

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        httpData (dict): contains the informations needed
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return an error in the text field or the updated sample in the content field
    """
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

    # list of fields allowed in the httpData dict, adding fields will trigger an error
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
    """Allow a patient to update a sample in his own datas by specifying the timestamp of the datas instead of the id

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        httpData (dict): contains the informations needed
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return an error in the text field or the sample that was destroyed in the content field
    """
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

    # list of fields allowed in the httpData dict, adding fields will trigger an error
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
    """Return the list of all the patients that does not have an binded doctor

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return an error in the text field or a list of dicts, each dict is a patient that does not have an binded doctor
    """
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


def getPatientsForDoctor(connection, log_info):
    """Return a list of all the patients binded to the current doctor

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return the error in the text field or a list of dicts, each dict is a patient bind to the current doctor
    """
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
    """Return the datas of a specified patient bind to the current doctor

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        httpData (dict): contains the informations needed
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return the error in the text field or the datas of the requested patient in the content field
    """
    mail,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "RESSOURCE_READ"

    doctor = dbhandler.readDoctor(connection, mail, pwd)
    if not doctor:
        response["text"] = "you need to be logged in"
        return response    

    # httpData needs to contain the id of the requested patient
    if not "id_patient" in httpData:
        response["text"] = "Patient not specify"
        return response
    
    id_patient = httpData["id_patient"]
    patient = dbhandler.readPatientId(connection, id_patient)
    patients_allowed = getPatientsForDoctor(connection, log_info)["content"]
    # the doctor needs to be bind with the requested patient
    if patient not in patients_allowed:
        response["text"] = 'You cannot acces this patient.'
        return response

    response["content"] = dbhandler.getPatientData(connection, patient["email"])
    return response


def patientSendMessage(connection, httpData, log_info):
    """Allow a patient to send a message to a doctor using the doctor's mail adress

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        httpData (dict): contains the informations needed
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return the error in the text field or a validation message \"Message sended.\" in the content field
    """
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

    timestamp = datetime.now().strftime("%d-%m-%Y")

    doc = dbhandler.readDoctor(connection, httpData["email_doctor"])

    id_patient = user["id_patient"]
    id_doc = doc["id_doctor"]
    body = httpData["body"]
    dbhandler.createMessage(connection, id_patient, id_doc, timestamp, body)
    
    response["content"] = "Message sended."
    return response

def doctorSendMessage(connection, httpData, log_info):
    """Allow a doctor to send a message to a patient using the patient's mail adress

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        httpData (dict): contains the informations needed
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return the error in the text field or a validation message \"Message sended.\" in the content field
    """
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

    timestamp = datetime.now().strftime("%d-%m-%Y")

    patient = dbhandler.readPatient(connection, httpData["email_patient"])

    id_doctor = user["id_doctor"]
    id_patient = patient["id_patient"]
    body = httpData["body"]
    dbhandler.createMessage(connection, id_patient, id_doctor, timestamp, body)
    
    response["content"] = "Message sended."
    return response

def getPatientMessage(connection, log_info):
    """Return the list of the current patient's messages

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return the error in the text field or a list of dicts, a dict if a message with the text in the body field, in the content field
    """
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
    """Return the list of the current doctor's messages

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return the error in the text field or a list of dicts, a dict if a message with the text in the body field, in the content field
    """
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

def addPatientToDoc(connection, httpData, log_info):
    """Bind a patient to the current doctor

    Args:
        connection (pymysql.connections.Connection): connection with the SQL database
        httpData (dict): contains the informations needed
        log_info (tuple): must contain (email,password) info on the current user

    Returns:
        dict: return the error in the text field or the validation message \"Done.\" in the content field.
    """
    email,pwd = log_info

    response = {}
    response["code"] = "OPERATION_OK"
    response["operation"] = "PATIENT_ADDED"

    user = dbhandler.readDoctor(connection, email, pwd)
    if not user :
        response["text"] = "You need to be logged in."
        return response

    if not "id_patient" in httpData:
        response["text"] = "You need to specify id_patient"
        return response

    patient = dbhandler.readPatientId(connection, httpData["id_patient"])
    if not patient:
        response["text"] = "Patient not found"
        return response

    response["content"] = dbhandler.newRelation(connection, user["id_doctor"], patient["id_patient"])
    return response