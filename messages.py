#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(1, '/home/philipad_SEV5204E/public_html/ws/lib') 
# from lib import wslib
import wslib
import cgitb
import json 

# Permet d’activer les retours d’erreur du module CGI
cgitb.enable()

print("Content-type: application/json\n")

#Test validité request HTTP
wslib.getErrors()

httpMethod = os.environ['REQUEST_METHOD']
httpData = wslib.returnHttpData()

if "dest" in httpData.keys(): dest = httpData["dest"]
else: dest = None

#Connexion database
connection = wslib.connect()

#Lecture contenu table messages
if httpMethod == "GET":
    print(json.dumps(wslib.readRessource(connection, dest)))  
if httpMethod == "DELETE":
    wslib.deleteRessource(connection, dest)
        
connection.close()