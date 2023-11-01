from threading import Thread, Event
import time
import datetime
import socket
from Commands import Commands
import pickle
import struct
import numpy as np
import dao
from Pageable import PageRequest
HEADERSIZE = 10
class Client:
    def __init__(self, conn, detector):
        # attribute of client
        self.socket = conn
        self.detector = detector
        self.active = True

        # run
        # self.t = Thread(target=self.run, args=())
        # self.t.setDaemon = True
        # self.t.start()
        self.run()

    def run(self):
        CommandsSender(self, self.detector)

    def close_socket(self):
        self.socket.close()


class CommandsSender:
    def __init__(self, client, detector):
        self.client = client
        self.detector = detector
        # run
        self.t = Thread(target=self.run, args=())
        self.t.setDaemon = True
        self.t.start()

        self.pageable = None

    def sendLogFaceDetector(self):
        print("function sendlogfacedetector")
        currentTime = datetime.datetime.now()
        msg = '[' + str(currentTime.year) + '-' + str(currentTime.month) + '-' + str(currentTime.day) + ' ' + str(
                currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second) + ':' + ']' + ' : '
        for name in self.detector.face_names:
            msg = msg + name
        try:
            self.client.socket.sendall(msg.encode("utf8"))
            self.client.socket.recv(1024)
        except socket.error as error:
            self.client.active = False
            print("Client disconnect")
            raise Exception("Client disconnect")
        time.sleep(1)

    def sendImage(self):
        try:
            # Serialize frame
            data = pickle.dumps(self.detector.img)

            # Send message length first
            message_size = struct.pack("L", len(data))  ### CHANGED

            # Then data
            self.client.socket.sendall(message_size + data)
        except:
            print("client disconnect")


    def sendHumidityAndTemperature(self):
        try:
            humidity = np.random.randint(10, 50, size=1)[-1]
            temperature = np.random.randint(10, 50, size=1)[-1]

            data = pickle.dumps([humidity, temperature])
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.client.socket.sendall(data)

            # msg = str(humidity) + ":" + str(temperature)
            # self.client.socket.sendall(msg.encode('utf8'))
        except socket.error as error:
            print(str(error))

    def sendPageList(self):
        try:
            # receive pageable
            pageable = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.client.socket.recv(16)
                if new_msg:
                    # print("new msg len:", msg[:HEADERSIZE])
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                # print(f"full message length: {msglen}")

                full_msg += msg
                # print(full_msg)
                #
                # print(len(full_msg))

                if len(full_msg) - HEADERSIZE == msglen:
                    # print("full msg recvd")
                    # print(full_msg[HEADERSIZE:])
                    pageable = pickle.loads(full_msg[HEADERSIZE:])
                    # print(pageable)
                    break

            # select data
            # print(pageable.page)
            list = dao.UserDAO().findPageable(pageable=pageable)
            # send data
            data = pickle.dumps(list)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.client.socket.sendall(data)

        except socket.error as msg:
            print(str(msg))

    def sendPageHistory(self):
        try:
            # receive pageable
            pageable = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.client.socket.recv(16)
                if new_msg:
                    # print("new msg len:", msg[:HEADERSIZE])
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                # print(f"full message length: {msglen}")

                full_msg += msg
                # print(full_msg)
                #
                # print(len(full_msg))

                if len(full_msg) - HEADERSIZE == msglen:
                    # print("full msg recvd")
                    # print(full_msg[HEADERSIZE:])
                    pageable = pickle.loads(full_msg[HEADERSIZE:])
                    # print(pageable)
                    break

            # select data
            print(pageable.page)
            list = dao.HistoryDAO().findPageable(pageable=pageable)
            # send data
            data = pickle.dumps(list)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            print(data)
            self.client.socket.sendall(data)

        except socket.error as msg:
            print(str(msg))

    def run(self):
        while True:
            print("Waiting command")
            try:
                cm = self.client.socket.recv(1024)
                # self.client.socket.sendall(cm)
                cm = int(cm.decode('utf8'))
                print("New command", cm)
                # self.cm = self.client.socket.recv(1024).decode('utf8')
                if cm == Commands.LOG_FACE_DETECTOR.value:
                    self.sendLogFaceDetector()
                elif cm == Commands.FRAME_AND_HT.value:
                    self.sendImage()
                    self.client.socket.recv(1024)
                    self.sendHumidityAndTemperature()
                elif cm == Commands.LIST.value:
                    self.sendPageList()
                elif cm == Commands.HISTORY.value:
                    self.sendPageHistory()
                elif cm == Commands.DIAGRAM.value:
                    self.sendHumidityAndTemperature()
            except socket.error as error:
                print(str(error))
                self.client.active = False
                break
