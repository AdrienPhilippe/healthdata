#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# sys.path.insert(1, '/home/menchit_SEV5204E/public_html/ws/lib')
import cgi
import cgitb
import json

from lib import dbhandler
from lib import wslib

# # Permet d’activer les retours d’erreur du module CGI
cgitb.enable()

print("Content-type: application/json\n")

#Test validité request HTTP
errors = wslib.getErrors()
if not len(errors) == 0:
    print(json.dumps(errors))
    sys.exit()

# store the http method to use
httpMethod = os.environ['REQUEST_METHOD']

# store the user and password
username, pwd = os.environ["HTTP_X_AUTH"].split(":")

#Connexion database
connection = dbhandler.connect()

# get the rights for the user
rights = wslib.getUserRights(connection, username, pwd)


# get http data
httpData = wslib.returnHttpData()
if "dest" in httpData.keys() : 
    dest = httpData["dest"]
    httpData.pop("dest")
else: dest = None

# Lecture contenu table messages
if httpMethod == "GET" :
    ressources = wslib.getDest(connection, rights, dest)
    print(json.dumps(ressources))

elif httpMethod == "DELETE" :
    ressources = wslib.deleteDest(connection, rights, dest)
    print(json.dumps(ressources))

elif httpMethod == "POST" :
    for dest, message in httpData.items():
        ressource = wslib.createDest(connection, rights, dest, message)
        print(json.dumps(ressource))

elif httpMethod == "PUT" :
    for dest, message in httpData.items():
        ressource = wslib.updateDest(connection, rights, dest, message)
        print(json.dumps(ressource))

connection.close()