import mysql.connector

class MySQL:
    def __init__(self, host='localhost', user='root', password='', database='pbl4'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        self.mydb = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        self.mycursor = self.mydb.cursor()