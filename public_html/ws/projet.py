#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cgi
import cgitb
import json
import os
import sys

from lib import wslib

cgitb.enable()
print('Content-type: application/json\n')

httpData = wslib.returnHttpData()

#Test validité request HTTP
errors = wslib.getErrors()
if not len(errors) == 0:
    print(json.dumps(errors))
    sys.exit()


connection, httpMethod, mail, pwd = wslib.init()

action = httpData.pop("action")

if httpMethod == "GET" and action == "get_current_patient":
    ressource = wslib.getPatient(connection, (mail,pwd)) # Done

elif httpMethod == "POST" and action == "patient_creation":
    ressource = wslib.createPatient(connection, httpData) # Done

elif httpMethod == "POST" and action == "create_data":
    ressource = wslib.createPatientData(connection, httpData, (mail,pwd)) # Done

elif httpMethod == "PUT" and action == "modify_data":
    ressource = wslib.updatePatientData(connection, httpData, (mail,pwd)) # Done

elif httpMethod == "DELETE" and action == "delete_patient_data":
    ressource = wslib.deletePatientData(connection, httpData, (mail,pwd)) # Done

elif httpMethod == "GET" and action == "get_current_doctor_data":
    ressource = wslib.getDoctor(connection, (mail,pwd)) # Done

elif httpMethod == "POST" and action == "doctor_creation":
    ressource = wslib.createDoctor(connection, httpData) # Done

elif httpMethod == "GET" and action == "get_patient_for_doctor":
    ressource = wslib.getPatientsForDoctor(connection, httpData, (mail,pwd)) # Done

elif httpMethod == "GET" and action == "get_patient_data_for_doctor":
    ressource = wslib.getPatientsDataForDoctor(connection, httpData, (mail,pwd)) # Done

elif httpMethod == "POST" and action == "patient_write_message":
    ressource = wslib.patientSendMessage(connection, httpData, (mail,pwd)) # Done

elif httpMethod == "POST" and action == "doctor_write_message":
    ressource = wslib.doctorSendMessage(connection, httpData, (mail,pwd)) # Done

elif httpMethod == "GET" and action == "patient_read_messages":
    ressource = wslib.getPatientMessage(connection, (mail,pwd)) # Done

elif httpMethod == "GET" and action == "doctor_read_message":
    ressource = wslib.getDoctorMessage(connection, (mail,pwd)) # Done

else : ressource = (httpMethod,httpData,action)

print(json.dumps(ressource))
