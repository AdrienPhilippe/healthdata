#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 18:10:25 2020
@author: lacombea
"""
import requests
import json
# URI d’accès à l’intégralité de la collection
uri = "https://gaalactic.fr/~menchit_SEV5204E/ws/messages"
# Dictionnaire contenant les données à insérer dans l’en-tête de la requête http
# Seul l’en-tête « Accept » est obligatoire. L’en-tête "User-agent" a
# été rajouté pour illustrer la façon dont on spécifie plusieurs directives d’en-tête
loginPwd = 'Mary:Passiflore812'
customHeaders = {'Accept' : 'application/json', 'X-Auth' : loginPwd, 'Content-type' : 'application/x-www-form-urlencoded'}

# Envoi de la requête http à destination de l’agent serveur
httpReturn = requests.get(uri, headers=customHeaders)
# Extraction du contenu du corps de la réponse (httpReturn.text)
# Dans le cas présent celui-ci correspond au contenu de la collection au format json
# puisque la valeur de l’en-tête « Accept » de la requête était "application/json"
representationContent = httpReturn.text
print("\nContenu du corps de la réponse http :")
print(representationContent)

# handling ressource not found
if httpReturn.status_code not in [200,201] : 
    print(f"Error with status code : {httpReturn.status_code}")
    exit()


# Désérialisation de la chaîne json et créer un objet qui contient
# les données sous une forme structurée
structuredRepresentationContent = json.loads(representationContent)
# L'objet ainsi obtenu correspond un dictionnaire

print("\nType de la structure contenant les données de la collection :")
print(type(structuredRepresentationContent))

print("\nContenu structuré de la collection :")
print(structuredRepresentationContent)

print("\nDonnées du premier élément de la structure de données :")
print(structuredRepresentationContent["content"][0])

dest = "ducks"
print(f"\nDonnées de l'élément {dest} :")
try : el = next(content for content in structuredRepresentationContent["content"] if content["dest"] == dest)
except : el = f"{dest} not found"
print(el)

print("\nEntête du serveur : ")
print(httpReturn.headers)

print("\nCode de statut du serveur : ")
print(httpReturn.status_code)

# r = requests.delete(uri, headers=customHeaders)
# print(r.text)
