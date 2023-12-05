import base64
import datetime
import pickle
import socket
import threading
import time
from threading import Thread

import cv2
import imutils

import dao
from Commands import Commands

HEADERSIZE = 10
class Client:
    def __init__(self, conn, UDP, detector, arduino):
        # attribute of client
        self.socket = conn[0]
        self.addr_TCP = conn[1]
        self.socket_UDP = UDP
        self.detector = detector
        self.active = True
        self.arduino = arduino
        # run
        # self.t = Thread(target=self.run, args=())
        # self.t.setDaemon = True
        # self.t.start()
        self.run()

    def run(self):
        CommandsSender(self, self.detector, self.arduino)

    def close_socket(self):
        self.socket.close()


class CommandsSender:
    def __init__(self, client, detector, arduino):
        self.client = client
        self.socket = client.socket
        self.socket_UDP = client.socket_UDP
        self.socket_UDP.settimeout(0.2)
        self.detector = detector
        self.arduino = arduino

        self.addr_UDP = (self.client.addr_TCP[0], self.getAddrUDP()[1])
        print(self.addr_UDP)
        # run
        self.t = Thread(target=self.run, args=())
        self.t.setDaemon = True
        self.t.start()

        self.pageable = None

    def getAddrUDP(self):
        try:
            # receive data
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(16)
                if new_msg:
                    msg_len = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg

                if len(full_msg) - HEADERSIZE == msg_len:
                    list = pickle.loads(full_msg[HEADERSIZE:])
                    break
            return list
        except socket.error as msg:
            print(str(msg))
            self.client.active = False

    def sendLogFaceDetector(self):
        print("function sendlogfacedetector")
        currentTime = datetime.datetime.now()
        msg = '[' + str(currentTime.year) + '-' + str(currentTime.month) + '-' + str(currentTime.day) + ' ' + str(
                currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second) + ':' + ']' + ' : '
        for name in self.detector.face_names:
            msg = msg + name
        try:
            self.socket.sendall(msg.encode("utf8"))
            self.socket.recv(1024)
        except socket.error as error:
            self.client.active = False
            print("Client disconnect")
            raise Exception("Client disconnect")
        time.sleep(1)

    def sendImage(self):
        try:
            frame = imutils.resize(self.detector.img, width=400)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 20])
            data = base64.b64encode(buffer)
            data = bytes(f"{1:<{HEADERSIZE}}", 'utf-8') + data
            self.socket_UDP.sendto(data, self.addr_UDP)


        except:
            print("client disconnect")


    def sendHumidityAndTemperature(self):
        try:
            # humidity = self.arduino.readline().decode()
            # temperature = self.arduino.readline().decode()
            # if humidity != "" and temperature != "":
            #     humidity = float(humidity)
            #     temperature = float(temperature)
            # else:
            #     humidity = 0
            #     temperature = 0

            humidity = 0
            temperature = 0

            data = pickle.dumps([humidity, temperature])
            data = bytes(f"{2:<{HEADERSIZE}}", 'utf-8') + data
            self.socket_UDP.sendto(data, self.addr_UDP)

        except socket.error as error:
            print(str(error))
            print('error function ht')
        except Exception as e:
            print(str(e))

    def sendPageList(self):
        try:
            # receive pageable
            pageable = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(16)
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
            self.socket.sendall(data)

        except socket.error as msg:
            print(str(msg))

    def sendPageHistory(self):
        try:
            # receive pageable
            pageable = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.socket.recv(16)
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
            self.socket.sendall(data)

        except socket.error as msg:
            print(str(msg))

    def sendHTAndImage(self):
        while self.isContinue:
            self.sendImage()
            self.sendHumidityAndTemperature()
            # print('send')

    def run(self):
        old_cm = None
        thread = None
        while True:
            # print("Waiting command")
            try:
                if old_cm == Commands.FRAME_AND_HT.value:
                    self.isContinue = False
                cm = self.socket.recv(1024)
                old_cm = cm
                # self.client.socket.sendall(cm)
                cm = int(cm.decode('utf8'))
                print("New command", cm)
                # self.cm = self.client.socket.recv(1024).decode('utf8')
                if cm == Commands.LOG_FACE_DETECTOR.value:
                    self.sendLogFaceDetector()
                elif cm == Commands.FRAME_AND_HT.value:
                    self.isContinue = True
                    # thread = threading.Thread(target=self.sendHTAndImage, args=()).start()
                    self.sendHTAndImage()
                    # self.sendImage()
                    # self.socket.recv(1024)
                    # self.sendHumidityAndTemperature()
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
            except Exception as e:
                print(str(e))
