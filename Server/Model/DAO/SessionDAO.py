import os
import sys

import mysql.connector
import datetime

# from Server.Util import Connection
# from Server.Model.Bean.Session import Session
# from Server.Model.Bean.Room import Room

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Util import Connection
from Model.Bean.Session import Session
from Model.Bean.Room import Room


class SessionDAO:
    def __init__(self):
        self.connect = Connection.getConnect()
        self.myCursor = self.connect.cursor()

    def getAll(self):
        sql = 'SELECT * FROM session'
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        sessions = []
        for item in result:
            session = Session(item[0], item[1], item[2], item[3], item[4], item[4])
            sessions.append(session)
        return sessions

    def getById(self, id):
        sql = 'SELECT * FROM session WHERE id = ' + id
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        item = result[0]
        session = Session(item[0], item[1], item[2], item[3], item[4], item[5])
        return session


    def getStudentForSession(self, idSession):
        sql = 'SELECT * FROM student_join_session WHERE id_session = ' + str(idSession)
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        users = []
        from Server.Model.DAO.UserDAO import UserDAO
        for item in result:
            user = UserDAO().getById(item[1])
            users.append(user)
        return users

    def getSessionByRoomNumber(self, roomNumber):
        sql = 'SELECT * FROM session INNER JOIN room ON room.id = session.id_room WHERE room_number = %s'
        self.myCursor.execute(sql, [roomNumber])
        result = self.myCursor.fetchall()
        sessions = []
        for item in result:
            session = Session(item[0], item[1], item[2], item[3], item[4], item[5])
            room = Room(item[6], item[7])
            session.room = room
            sessions.append(session)
        return sessions



if __name__ == '__main__':
    sessions = SessionDAO().getStudentForSession(1)
    print(sessions)