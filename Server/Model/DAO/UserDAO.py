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
        try:
            sql = 'SELECT * FROM user'
            self.myCursor.execute(sql)
            result = self.myCursor.fetchall()
            users = []
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
                users.append(user)
            return users
        except Exception as e:
            print(e)
            return []

    def getById(self, id):
        sql = 'SELECT * FROM user WHERE id = ' + str(id)
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        item = result[0]
        user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
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
        try:
            sql = 'SELECT * FROM user INNER JOIN student_join_session AS sjs ON sjs.id_Student = user.id WHERE sjs.id_session = %s'
            self.myCursor.execute(sql, [idSession])
            result = self.myCursor.fetchall()
            users = []
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
                users.append(user)
            return users
        except Exception as e:
            print(e)
            return []

    def updateById(self, id, fullname, dateOfBirth, cccd, email, gender):
        try:
            sql = 'UPDATE user SET fullname = %s, date_of_birth = %s, cccd = %s, email = %s, gender = %s WHERE id = %s'
            self.myCursor.execute(sql, [fullname, dateOfBirth, cccd, email, gender, id])
            self.connect.commit()
        except Exception as e:
            print(e)

    def deleteById(self, userId):
        try:
            sql = 'DELETE FROM user WHERE id = %s'
            self.myCursor.execute(sql, [userId])
            self.connect.commit()
        except Exception as e:
            print(e)

    def insertStudent(self, fullname, dateOfBirth, cccd, email, gender):
        try:
            sql = 'INSERT INTO user (fullname, date_of_birth, email, gender, id_role, cccd) VALUES ( %s, %s, %s, %s, 1, %s)'
            self.myCursor.execute(sql, [fullname, dateOfBirth, email, gender, cccd])
            self.connect.commit()
            return self.myCursor.lastrowid
        except Exception as e:
            print(e)

    def deleteUserToSession(self, userId, sessionId):
        try:
            sql = 'DELETE FROM student_join_session WHERE id_session = %s AND id_student = %s'
            self.myCursor.execute(sql, [sessionId, userId])
            self.connect.commit()
        except Exception as e:
            print(e)

    def findByFullNameAndEmailNotInSession(self, msg, sessionId):
        try:
            sql = 'SELECT * FROM user WHERE (fullname LIKE %s OR email LIKE %s) AND id NOT IN (SELECT id_student FROM student_join_session WHERE id_session = %s)'
            self.myCursor.execute(sql, [msg, msg, sessionId])
            result = self.myCursor.fetchall()
            users = []
            for item in result:
                user = User(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
                users.append(user)
            return users
        except Exception as e:
            print(e)
            return []

    def insertStudentForSession(self, userId, sessionId):
        try:
            sql = 'INSERT INTO student_join_session (id_session, id_student, is_join) VALUES (%s, %s, 0)'
            self.myCursor.execute(sql, [sessionId, userId])
            self.connect.commit()
        except Exception as e:
            print(e)

    def updateStudentForSession(self, userId, sessionId):
        try:
            sql = 'UPDATE student_join_session SET is_join = 1 WHERE id_session = %s AND id_student = %s'
            self.myCursor.execute(sql, [sessionId, userId])
            self.connect.commit()
        except Exception as e:
            print(e)

if __name__ == '__main__':
     users = UserDAO().getSessionForUser(1)
     print(users[0].name)