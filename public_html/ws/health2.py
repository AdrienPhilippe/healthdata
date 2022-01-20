#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
<<<<<<< Updated upstream

from lib import dbhandler
=======
import pymysql

def connect():
    connection = pymysql.connect(host='localhost',
                                user='menchit_SEV5204E',
                                password='8g2DaJd4',
                                database='menchit_SEV5204E',
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection
>>>>>>> Stashed changes

print("Content-type: application/json\n")

def df_to_dict(file):
    mylist = []
    data = csv.DictReader(open(file))

    for row in data:
        mylist.append(row)

    return mylist

def upload(table, tablestr, connection, cursor):
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
<<<<<<< Updated upstream
        cursor.execute(query)
    print('Done')
    connection.commit()
=======
        print(query)
        try:
            cursor.execute(query)
        except Exception as e:
            print(e)
    connection.commit()
    print("DOne")  
>>>>>>> Stashed changes

Datas = df_to_dict('Datas.csv')
Doctors = df_to_dict('Doctors.csv')
Patients = df_to_dict('Patients.csv')
Relations = df_to_dict('Relations.csv')

<<<<<<< Updated upstream
connection = dbhandler.connect()
=======
connection = connect()
>>>>>>> Stashed changes
cursor = connection.cursor()

upload(Patients,"Patients", connection, cursor)
upload(Doctors,"Doctors", connection, cursor)
upload(Datas,"Datas", connection, cursor)
upload(Relations,"Relations", connection, cursor)

<<<<<<< Updated upstream
=======

>>>>>>> Stashed changes
connection.close()
