#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 18:10:25 2020
@author: lacombea
"""
import requests
import json
# URI d’accès à l’intégralité de la collection
uri = "https://www.gaalactic.fr/~lacombea/ws/messages"
# Dictionnaire contenant les données à insérer dans l’en-tête de la requête http
# Seul l’en-tête « Accept » est obligatoire. L’en-tête "User-agent" a
# été rajouté pour illustrer la façon dont on spécifie plusieurs directives d’en-tête
customHeaders = {"Accept": "application/json", "User-agent": "my_client_agent/v0.0.1"}
# Envoi de la requête http à destination de l’agent serveur
httpReturn = requests.get(uri, headers=customHeaders)
if httpReturn.status_code == 404: print('ERROR 404'); exit()
# Extraction du contenu du corps de la réponse (httpReturn.text)
# Dans le cas présent celui-ci correspond au contenu de la collection au format json
# puisque la valeur de l’en-tête « Accept » de la requête était "application/json"
representationContent = httpReturn.text
print("\nContenu du corps de la réponse http :")
print(representationContent)
# Désérialisation de la chaîne json et créer un objet qui contient
# les données sous une forme structurée
structuredRepresentationContent = json.loads(representationContent)
# L'objet ainsi obtenu correspond un dictionnaire
print("\nType de la structure contenant les données de la collection :")
print(type(structuredRepresentationContent))
print("\nContenu structuré de la collection :")
print(structuredRepresentationContent)
print("\nContenu 1er element de la collection :")
print(structuredRepresentationContent["content"])
print("\nContenu de cats :")
print(next(e for e in structuredRepresentationContent["content"] if e["dest"] == 'cats'))
print("\nContenu du header :")
print(httpReturn.headers)
print("\nContenu du statut de la réponse :")
print(httpReturn.status_code)
