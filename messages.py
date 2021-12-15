#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(1, '/home/PHILIPPE_SEV5204E/public_html/ws/lib') 
import wslib
import cgi
import cgitb

# Permet d’activer les retours d’erreur du module CGI
cgitb.enable()

print("Content-type: application/json\n")

#Test validité request HTTP
wslib.testRequest()

#Connexion database
connection = wslib.connect()

#Lecture contenu table messages
wslib.readRessource(connection)
        
connection.close()