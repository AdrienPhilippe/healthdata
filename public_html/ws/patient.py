#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from lib import wslib

connection, httpMethod, httpData, mail, pwd = wslib.init()

if httpMethod == "GET" :
    ressource = wslib.getData(connection, httpData, (mail,pwd))

if httpMethod == "POST" and httpData["action"] == "patient_creation":
    ressource = wslib.createPatient(connection, httpData)

if httpMethod == "POST" and httpData["action"] == "create_data":
    print("create_data")
    ressource = None

if httpMethod == "POST" and httpData["action"] == "modify_data":
    print("modify_data")
    ressource = None



print(json.dumps(ressource))


print("\n\n======== Done ========")
