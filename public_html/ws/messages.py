#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(1, '/home/menchit_SEV5204E/public_html/ws/lib') 
import cgi
import cgitb
import json

import wslib

# Permet d’activer les retours d’erreur du module CGI
cgitb.enable()

print("Content-type: application/json\n")

#Test validité request HTTP
errors = wslib.errors_handler()
if not len(errors) == 0:
    print(json.dumps(errors))

httpMethod = os.environ['REQUEST_METHOD']

#Connexion database
connection = wslib.connect()

#Lecture contenu table messages
if httpMethod == "GET" :
    print(json.dumps(wslib.readRessource(connection)))

if httpMethod == "DELETE" :
    print(wslib.deleteRessource(connection))
        
connection.close()
