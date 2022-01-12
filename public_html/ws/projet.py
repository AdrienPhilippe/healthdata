#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from lib import wslib

connection, httpMethod, httpData, mail, pwd = wslib.init()

if httpMethod == "GET" and httpData["action"] == "get_current_patient_data":
    ressource = wslib.getDataPatient(connection, (mail,pwd)) # Done

elif httpMethod == "POST" and httpData["action"] == "patient_creation":
    ressource = wslib.createPatient(connection, httpData) # Done

elif httpMethod == "POST" and httpData["action"] == "create_data":
    ressource = wslib.createPatientData(connection, httpData, (mail,pwd)) # ToDo

elif httpMethod == "POST" and httpData["action"] == "modify_data":
    ressource = wslib.updatePatientData(connection, httpData, (mail,pwd)) # ToDo

elif httpMethod == "GET" and httpData["action"] == "get_current_doctor_data":
    ressource = wslib.getDataDoctor(connection, (mail,pwd)) # ToDo

elif httpMethod == "GET" and httpData["action"] == "get_patient_for_doctor":
    ressource = wslib.getPatientsForDoctor(connection, httpData, (mail,pwd)) # ToDo

else : ressource = (httpMethod,httpData)

print(json.dumps(ressource))


print("\n\n================================ Done ================================")
