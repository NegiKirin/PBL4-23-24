import mysql.connector

host = 'localhost'
user = 'root'
password = ''
database = 'pbl4'


def getConnect():
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    return mydb
