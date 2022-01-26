#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json
import os
import sys

from lib import wslib

"""
This file is the main file of the project. It purpose is to manage the working environment and to recover crucial
informations such as the current user, the http method used, and the action that the client which to perform.
Using those informations, it will then use the right function to perform the action. All the functions are
contained in the wslib which will return a response containing a content or on error message.
"""

cgitb.enable()
print('Content-type: application/json\n')

# storing httpData
httpData = wslib.returnHttpData()

#Test validité request HTTP
errors = wslib.getErrors()
if not len(errors) == 0:
    print(json.dumps(errors))
    sys.exit()

# initializing environment and important variable such as the login info
connection, httpMethod, mail, pwd = wslib.init()

# storing which action the client want to perform
action = httpData.pop("action")

# returning infos on the current patient
if httpMethod == "GET" and action == "get_current_patient":
    ressource = wslib.getPatient(connection, (mail,pwd)) # Done

# create a new patient
elif httpMethod == "POST" and action == "patient_creation":
    ressource = wslib.createPatient(connection, httpData) # Done

# returning all the data bind to the current patient
elif httpMethod == "GET" and action == "get_data":
    ressource = wslib.getPatientData(connection, (mail,pwd)) # ToDo

# adding data to the current patient
elif httpMethod == "POST" and action == "create_data":
    ressource = wslib.createPatientData(connection, httpData, (mail,pwd)) # Done

# allow the current patient to modify data that belongs to him
elif httpMethod == "PUT" and action == "modify_data":
    ressource = wslib.updatePatientData(connection, httpData, (mail,pwd)) # Done

# allow the current patient to modify his data using the time of data's record
elif httpMethod == "PUT" and action == "modify_data_time":
    ressource = wslib.updatePatientDataWithTimestamp(connection, httpData, (mail,pwd)) # Done

# allow current patient to delete his datas
elif httpMethod == "DELETE" and action == "delete_patient_data":
    ressource = wslib.deletePatientData(connection, httpData, (mail,pwd)) # Done

# returning infos on the current doctor
elif httpMethod == "GET" and action == "get_current_doctor_data":
    ressource = wslib.getDoctor(connection, (mail,pwd)) # Done

# create a new doctor
elif httpMethod == "POST" and action == "doctor_creation":
    ressource = wslib.createDoctor(connection, httpData) # Done

# returning the list of the patients bound to the current doctor
elif httpMethod == "GET" and action == "get_patient_for_doctor":
    ressource = wslib.getPatientsForDoctor(connection, (mail,pwd)) # Done

# allow a doctor to check the data of one of his patient
elif httpMethod == "GET" and action == "get_patient_data_for_doctor":
    ressource = wslib.getPatientsDataForDoctor(connection, httpData, (mail,pwd)) # Done

# allow a patient to write a message to his doctor
elif httpMethod == "POST" and action == "patient_write_message":
    ressource = wslib.patientSendMessage(connection, httpData, (mail,pwd)) # Done

# allow a doctor to write a message to a patient
elif httpMethod == "POST" and action == "doctor_write_message":
    ressource = wslib.doctorSendMessage(connection, httpData, (mail,pwd)) # Done

# allow a patient to read all his messages
elif httpMethod == "GET" and action == "patient_read_messages":
    ressource = wslib.getPatientMessage(connection, (mail,pwd)) # Done

# allow a doctor to read all his messages
elif httpMethod == "GET" and action == "doctor_read_message":
    ressource = wslib.getDoctorMessage(connection, (mail,pwd)) # Done

# returning the list of patients that does not have any bind doctor
elif httpMethod == "GET" and action == "get_patient_without_doc":
    ressource = wslib.getPatientWithoutDoctor(connection, (mail,pwd)) # Done

# allow a doctor to bind a patient to himself
elif httpMethod == "POST" and action == "add_patient_to_doc":
    ressource = wslib.addPatientToDoc(connection, httpData, (mail,pwd))

# if the action and the method does not correspond to anything in the list above, simply return the current method and action
else : ressource = (httpMethod,httpData,action)

print(json.dumps(ressource))
