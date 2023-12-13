import os
import sys

import mysql.connector
import datetime

# from Server.Model.DAO.RoleDAO import RoleDAO
# from Server.Model.DAO.SessionDAO import SessionDAO
# from Server.Util import Connection
# from Server.Model.Bean.User import User

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Model.Bean.User import User
from Util import Connection
from Model.DAO.RoleDAO import RoleDAO
from Model.DAO.SessionDAO import SessionDAO


class UserDAO:
    def __init__(self):
        self.connect = Connection.getConnect()
        self.myCursor = self.connect.cursor()

    def getAll(self):
        sql = 'SELECT * FROM user'
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        users = []
        for item in result:
            user = User(item[0], item[1], item[2], item[3], item[4], item[5])
            users.append(user)
        return users

    def getById(self, id):
        sql = 'SELECT * FROM user WHERE id = ' + str(id)
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        item = result[0]
        user = User(item[0], item[1], item[2], item[3], item[4], item[5])
        user.role = RoleDAO().getById(item[5])
        return user

    def getSessionForUser(self, idUser):
        sql = 'SELECT * FROM student_join_session WHERE id_user = ' + str(idUser)
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        sessions = []
        for item in result:
            session = SessionDAO().getById(item[0])
            sessions.append(session)
        return sessions

    def getListUser(self, idSession):
        sql = 'SELECT * FROM user INNER JOIN student_join_session AS sjs ON sjs.id_Student = user.id WHERE sjs.id_session = ' + str(idSession)
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        users = []
        for item in result:
            user = User(item[0], item[1], item[2], item[3], item[4], item[5])
            users.append(user)
        return users


if __name__ == '__main__':
     users = UserDAO().getSessionForUser(1)
     print(users[0].name)