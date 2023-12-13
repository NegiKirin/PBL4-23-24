import os
import sys

import mysql.connector
import datetime

# from Server.Util import Connection
# from Server.Model.Bean.Role import Role

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Util import Connection
from Model.Bean.Role import Role


class RoleDAO:
    def __init__(self):
        self.connect = Connection.getConnect()
        self.myCursor = self.connect.cursor()

    def getAll(self):
        sql = 'SELECT * FROM role'
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        roles = []
        for item in result:
            role = Role(item[0], item[1], item[2])
            roles.append(role)
        return roles

    def getById(self, id):
        sql = 'SELECT * FROM role WHERE id = ' + str(id)
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        item = result[0]
        role = Role(item[0], item[1], item[2])
        return role


if __name__ == '__main__':
    roles = RoleDAO().getById(1)
    print(roles.name)