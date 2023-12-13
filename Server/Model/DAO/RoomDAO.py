import os
import sys

import mysql.connector
import datetime

# from Server.Util import Connection
# from Server.Model.Bean.Room import Room

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Util import Connection
from Model.Bean.Room import Room


class RoomDAO:
    def __init__(self):
        self.connect = Connection.getConnect()
        self.myCursor = self.connect.cursor()

    def getAll(self):
        sql = 'SELECT * FROM room'
        self.myCursor.execute(sql)
        result = self.myCursor.fetchall()
        rooms = []
        for item in result:
            room = Room(item[0], item[1])
            rooms.append(room)
        return rooms

if __name__ == '__main__':
    rooms = RoomDAO().getAll()
    print(rooms[0].roomNumber)