#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(1, '/home/menchit_SEV5204E/public_html/ws/wslib') 
import wslib
import cgi
import cgitb

# Permet d’activer les retours d’erreur du module CGI
cgitb.enable()

print("Content-type: application/json\n")

#Test validité request HTTP
print(wslib.testRequest())

#Connexion database
connection = wslib.connect()

#Lecture contenu table messages
print(wslib.readRessource(connection))
        
connection.close()