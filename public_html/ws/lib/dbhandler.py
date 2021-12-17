import pymysql
import pymysql.cursors


#Connexion database
def connect():
    connection = pymysql.connect(host='localhost',
                                user='menchit_SEV5204E',
                                password='8g2DaJd4',
                                database='menchit_SEV5204E',
                                charset='utf8mb4',
                                port=3306,
                                cursorclass=pymysql.cursors.DictCursor)
    return connection



#Lecture contenu table messages
def readRessource(connection, ressource=None):
    query = "SELECT * FROM `messages`"
    if ressource is not None:
        query += "WHERE `dest` = '" + ressource + "'"

    with connection.cursor() as cursor:
        cursor.execute(query)
    result = cursor.fetchall()
    return result

def deleteRessource(connection, ressource=None):
    with connection.cursor() as cursor:
        if ressource is None :
            # raise Exception("No ressource to delete.")
            return -1

        res = readRessource(connection, ressource)
        if len(res) == 0:
            return -2
            # raise Exception("Ressource does not exist")

        query = "DELETE FROM `messages` WHERE `dest` = '" + ressource + "'"
        cursor.execute(query)

    connection.commit()
    return 1
