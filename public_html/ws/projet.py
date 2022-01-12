#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from lib import wslib

connection, httpMethod, httpData, mail, pwd = wslib.init()

if httpMethod == "GET" and httpData["action"] == "get_current_patient_data":
    ressource = wslib.getData(connection, (mail,pwd))

elif httpMethod == "POST" and httpData["action"] == "patient_creation":
    ressource = wslib.createPatient(connection, httpData)

elif httpMethod == "POST" and httpData["action"] == "create_data":
    print("create_data")
    ressource = wslib.createPatientData(connection, httpData, (mail,pwd))

elif httpMethod == "POST" and httpData["action"] == "modify_data":
    print("modify_data")
    ressource = wslib.updatePatientData(connection, httpData, (mail,pwd))

else : ressource = {"response" : "Action not found."}

print(json.dumps(ressource))


print("\n\n================================ Done ================================")
