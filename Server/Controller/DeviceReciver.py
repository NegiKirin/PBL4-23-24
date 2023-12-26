import os
import pickle
import sys
import threading
import socket
import cv2

# from Server.Util.Commands import Commands
# from Server.Model.DAO.SessionDAO import SessionDAO
# from Server.Model.DAO.UserDAO import UserDAO


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Util.Commands import Commands
from Model.DAO.SessionDAO import SessionDAO
from Model.DAO.UserDAO import UserDAO


BUFF_SIZE = 65536
HEADERSIZE = 10


class DeviceReceiver:
    def __init__(self, conn):
        self.soc = conn
        self.active = True
        self.data = '../database'

        t = threading.Thread(target=self.run, args=())
        # t.setDaemon = True
        t.start()

    def sendImage(self):
        print('send image')
        try:
            idSession = self.soc.recv(1024).decode('utf8')
            print(idSession)
            listUser = UserDAO().getListUser(idSession)
            # ex: [(1, 'Ho Duy Phuc', ...), (2, 'Pham Doan Minh Hieu', ...)]
            # load images
            images = []
            os.chdir(self.data)
            print(listUser)
            for folder in os.listdir():
                for user in listUser:
                    if int(folder) == user.id:
                        for file in os.listdir(folder):
                            image_path = os.path.join(folder, file)
                            img = cv2.imread(image_path)
                            images.append(img)
            # send image
            data = pickle.dumps(images)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.soc.sendall(data)

            self.soc.recv(1024).decode('utf8')

            data = pickle.dumps(listUser)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.soc.sendall(data)

        except socket.error as e:
            print(str(e))

    def sendSessionsOfRoom(self):
        try:
            roomNumber = self.soc.recv(1024).decode('utf8')
            print(roomNumber)
            sessions = SessionDAO().getSessionByRoomNumber(roomNumber)
            print(sessions)
            # send sessions
            data = pickle.dumps(sessions)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.soc.sendall(data)
        except socket.error as e:
            print(str(e))

    def receiverSessionIdAndUserId(self):
        try:
            list = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.soc.recv(102400)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    # print(msg)
                    new_msg = False

                full_msg += msg
                if len(full_msg) - HEADERSIZE == msglen:
                    # print(full_msg[HEADERSIZE:])
                    list = pickle.loads(full_msg[HEADERSIZE:])
                    # print(list)
                    break
            UserDAO().updateStudentForSession(list[1], list[0])
        except socket.error as e:
            print(str(e))

    def run(self):
        while True:
            try:
                print('wait command')
                cm = int(self.soc.recv(1024).decode('utf8'))
                self.soc.sendall(str(cm).encode('utf8'))
                print('new command', cm)
                if cm == Commands.SEND_IMAGES_FOR_DEVICE.value:
                    self.sendImage()
                elif cm == Commands.SEND_ROOM_NUMBER.value:
                    self.sendSessionsOfRoom()
                elif cm == Commands.SEND_SESSIONID_AND_USERID.value:
                    self.receiverSessionIdAndUserId()
            except socket.error as error:
                print(error)
                self.active = False
                break
            except Exception as e:
                print(str(e))
                self.active = False
                break