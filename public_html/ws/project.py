#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# sys.path.insert(1, '/home/menchit_SEV5204E/public_html/ws/lib')
import cgi
import cgitb
import json

# from lib import dbhandler
from lib import wslib
from lib import dbhandler

# # Permet d’activer les retours d’erreur du module CGI
cgitb.enable()

print("Content-type: application/json\n")

# store the http method to use
httpMethod = os.environ['REQUEST_METHOD']

#Test validité request HTTP
errors = wslib.getErrors()
if not len(errors) == 0:
    print(json.dumps(errors))
    sys.exit()

rights = "all"

# get http data
httpData = wslib.returnHttpData()
if "dest" in httpData.keys() : 
    dest = httpData["dest"]
    httpData.pop("dest")
else: dest = None

#Connexion database
connection = dbhandler.connect()

if httpMethod == "POST" :
    ressource = wslib.createPatient(connection, httpData)
    print(json.dumps(ressource))

print("Done")