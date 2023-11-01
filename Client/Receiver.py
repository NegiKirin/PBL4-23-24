import threading
import socket
import cv2
import struct
import pickle
from Commands import Commands
HEADERSIZE = 10
class Receiver:
    def __init__(self, client):
        self.client = client
        # commands default
        self.cm = -2

        self.pageable = None

    def setGUI(self, gui):
        self.gui = gui

    def receiverLogFaceName(self):
        while True:
            try:
                mess = self.client.recv(1024).decode('utf8')
                self.client.sendall(mess.encode('utf8'))
                print(mess)
                return mess
            except socket.error as msg:
                print(str(msg))


    def receiverImage(self):
        data = b''  ### CHANGED
        payload_size = struct.calcsize("L")  ### CHANGED
        try:
            # Retrieve message size
            while len(data) < payload_size:
                data += self.client.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0]  ### CHANGED

            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += self.client.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Extract frame
            frame = pickle.loads(frame_data)

            # Display
            # cv2.imshow('frame', frame)
            # cv2.waitKey(1)
            return frame
        except socket.error as msg:
            print(str(msg))

    def receiveHumidityAndTemperature(self):
        try:
            # receive data
            list = []
            full_msg = b''
            new_msg = True
            while True:
                msg = self.client.recv(16)
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
                    list = pickle.loads(full_msg[HEADERSIZE:])
                    # print(list)
                    break

            return list
        except socket.error as error:
            print(str(error))

    def receivePageList(self):
        try:
            # send pageable
            data = pickle.dumps(self.pageable)
            data = bytes(f"{len(data):<{HEADERSIZE}}", 'utf-8') + data
            # print(msg)
            self.client.sendall(data)

            # receive data
            list = []
            full_msg = b''
            new_msg = True
            while True:
                msg = self.client.recv(16)
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
            self.client.sendall(data)

            # receive data
            list = []
            full_msg = b''
            new_msg = True
            while True:
                msg = self.client.recv(16)
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
                self.client.sendall(str(self.cm).encode('utf8'))
                # print("send command: ", self.cm)
                # self.client.recv(1024)
                if self.cm == Commands.LOG_FACE_DETECTOR.value:
                    self.receiverLogFaceName()
                elif self.cm == Commands.FRAME_AND_HT.value:
                    self.gui.frame = self.receiverImage()
                    self.client.sendall('OK'.encode('utf8'))
                    HumTem = self.receiveHumidityAndTemperature()
                    self.gui.setTemp(HumTem[1], HumTem[0])
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
