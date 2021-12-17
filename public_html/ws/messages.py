#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(1, '/home/menchit_SEV5204E/public_html/ws/lib') 
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

httpMethod = os.environ['REQUEST_METHOD']

#Connexion database
connection = dbhandler.connect()

# get http data
httpData = wslib.getHttpData()
if "dest" in httpData.keys() : dest = httpData["dest"]
else: dest = None


# Lecture contenu table messages
if httpMethod == "GET" :
    ressources = wslib.getDest(connection, dest)
    print(json.dumps(ressources))

elif httpMethod == "DELETE" :
    ressources = wslib.deleteDest(connection, dest)
    print(json.dumps(ressources))
        
connection.close()