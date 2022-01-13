#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

from lib import dbhandler

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
        cursor.execute(query)
    print('Done')
    connection.commit()

Datas = df_to_dict('Datas.csv')
Doctors = df_to_dict('Doctors.csv')
Patients = df_to_dict('Patients.csv')
Relations = df_to_dict('Relations.csv')

connection = dbhandler.connect()
cursor = connection.cursor()

upload(Patients,"Patients", connection, cursor)
upload(Doctors,"Doctors", connection, cursor)
upload(Datas,"Datas", connection, cursor)
upload(Relations,"Relations", connection, cursor)

connection.close()
