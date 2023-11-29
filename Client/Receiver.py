import threading
import socket
import time

import cv2
import base64
import numpy as np
import struct
import pickle
from Commands import Commands

BUFF_SIZE = 65536
HEADERSIZE = 10


class Receiver:
    def __init__(self, socket, socket_UDP):
        self.socket = socket
        self.socket.settimeout(0.2)
        self.socket_UDP = socket_UDP
        self.socket_UDP.settimeout(0.2)
        # commands default
        self.cm = Commands.FRAME_AND_HT.value
        self.old_cm = None
        self.isContinue = True

        self.pageable = None
        self.gui = None

        self.sendAddrUDP()

        self.thread = None

    def setGUI(self, gui):
        self.gui = gui

    def sendAddrUDP(self):
        try:
            addr = self.socket_UDP.getsockname()
            data = pickle.dumps(addr)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            self.socket.sendall(data)
        except socket.error as msg:
            print(str(msg))

    def receiverLogFaceName(self):
        while True:
            try:
                mess = self.socket.recv(1024).decode('utf8')
                self.socket.sendall(mess.encode('utf8'))
                print(mess)
                return mess
            except socket.error as msg:
                print(str(msg))

    def receiverImage(self):
        try:

            packet, _ = self.socket_UDP.recvfrom(BUFF_SIZE)
            data = base64.b64decode(packet[HEADERSIZE:], ' /')
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)

            return frame
        except socket.error as msg:
            print(str(msg))

    def receiveHumidityAndTemperature(self):
        try:
            # receive data
            msg = b''
            # self.socket_UDP.sendto(b'Hello', ('192.168.1.8', 10000))

            msg, _ = self.socket_UDP.recvfrom(BUFF_SIZE)
            list = pickle.loads(msg[HEADERSIZE:])
            print(list)

            return list
        except Exception as e:
            print(str(e))
            # print('receiveHumidityAndTemperature')
            return [0, 0]

    def receiveHTAndImage(self):
        while self.isContinue:
            try:
                packet, _ = self.socket_UDP.recvfrom(BUFF_SIZE)
                msg = packet[:HEADERSIZE]
                print(msg.strip())
                if msg.strip() == b'1':
                    data = base64.b64decode(packet[HEADERSIZE:], ' /')
                    npdata = np.frombuffer(data, dtype=np.uint8)
                    frame = cv2.imdecode(npdata, 1)
                    self.gui.frame = frame
                elif msg.strip() == b'2':
                    msg, _ = self.socket_UDP.recvfrom(BUFF_SIZE)
                    list = pickle.loads(packet[HEADERSIZE:])
                    print(list)
                    self.gui.setTemp(list[1], list[0])
            except Exception as e:
                print(e)

    def receivePageList(self):
        try:
            # send pageable
            data = pickle.dumps(self.pageable)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            # print(msg)
            self.socket.sendall(data)

            # receive data
            list = []
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
                    print(full_msg[HEADERSIZE:])
                    list = pickle.loads(full_msg[HEADERSIZE:])
                    # print(list)
                    break

            return list
        except socket.error as msg:
            print(str(msg))

    def receivePageHistory(self):
        try:
            # send pageable
            data = pickle.dumps(self.pageable)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            # print(msg)
            self.socket.sendall(data)

            # receive data
            list = []
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
                    print(full_msg[HEADERSIZE:])
                    list = pickle.loads(full_msg[HEADERSIZE:])
                    print(list)
                    break

            return list
        except socket.error as msg:
            print(str(msg))

    def start(self):
        t = threading.Thread(target=self.run, args=())
        t.setDaemon = True
        t.start()

    def run(self):
        while True:
            try:
                if self.old_cm == Commands.FRAME_AND_HT.value:
                    self.isContinue = False
                self.socket.sendall(str(self.cm).encode('utf8'))
                self.old_cm = self.cm
                print("send command: ", self.cm)
                # self.client.recv(1024)
                if self.cm == Commands.LOG_FACE_DETECTOR.value:
                    self.receiverLogFaceName()
                elif self.cm == Commands.FRAME_AND_HT.value:
                    # self.gui.frame = self.receiverImage()
                    # self.socket.sendall('OK'.encode('utf8'))
                    # HumTem = self.receiveHumidityAndTemperature()
                    # self.gui.setTemp(HumTem[1], HumTem[0])
                    # self.gui.setTemp(20, 20)
                    self.isContinue = True
                    self.receiveHTAndImage()

                    # self.thread = threading.Thread(args=(), target=self.receiveHTAndImage).start()
                    # return
                    time.sleep(0.1)

                elif self.cm == Commands.LIST.value:
                    self.gui.List_f.tmp = self.receivePageList()
                    return
                elif self.cm == Commands.HISTORY.value:
                    self.gui.History_f.tmp = self.receivePageHistory()
                    return
                elif self.cm == Commands.DIAGRAM.value:
                    HumTem = self.receiveHumidityAndTemperature()
                    self.gui.setTemp(HumTem[1], HumTem[0])
            except socket.error as msg:
                print(str(msg))
                print("Receiver error")
