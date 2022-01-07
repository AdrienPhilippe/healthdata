#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.insert(1, '/home/philipad_SEV5204E/public_html/ws/lib') 
import wslib
import cgitb

# Permet d’activer les retours d’erreur du module CGI
cgitb.enable()

print("Content-type: application/json\n")

#Test validité request HTTP
wslib.errors_handler()

#Connexion database
connection = wslib.connect()

#Lecture contenu table messages
wslib.readRessource(connection)
        
connection.close()