#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pymysql

def connect():
    #Fonction permettant de se connecter à la base de donnée
    connection = pymysql.connect(host='localhost',
                                user='menchit_SEV5204E',
                                password='8g2DaJd4',
                                database='menchit_SEV5204E',
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection

print("Content-type: application/json\n")

def df_to_dict(file):
    #Permet de transformer un csv en dictionnaire en utilisant une bibliothèque native de python
    mylist = []
    data = csv.DictReader(open(file))

    for row in data:
        mylist.append(row)

    return mylist

def upload(table, tablestr, connection, cursor):
    #Permet d'upload un dictionnaire dans la table indiquer dans la base de donnée
    for dico in table:

        keys = ["`" + str(key) + "`" for key in dico.keys()]
        values = ["'" + str(value) + "'" for value in dico.values()]

        if "`password`" in keys:
            idx = keys.index("`password`")
            values[idx] = "PASSWORD("+values[idx]+")"

        keys = ", ".join(keys)
        values = ", ".join(values)

        query = "INSERT INTO `{}` ({}) VALUES ({});".format(tablestr,keys,values)
        query = query.replace('"', "")
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
    connection.commit()
    print("DONE")  

#On transforme les fichiers qu'on a créé au préalable
Datas = df_to_dict('Datas.csv')
Doctors = df_to_dict('Doctors.csv')
Patients = df_to_dict('Patients.csv')
Relations = df_to_dict('Relations.csv')

#On se connecte à la base SQL
connection = connect()
cursor = connection.cursor()

#On upload chaque dictionnaire dans les bonnes tables
upload(Patients,"Patients", connection, cursor)
upload(Doctors,"Doctors", connection, cursor)
upload(Datas,"Datas", connection, cursor)
upload(Relations,"Relations", connection, cursor)


connection.close()
