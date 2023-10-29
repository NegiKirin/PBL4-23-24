import threading
import socket
import cv2
import struct
import pickle
from Commands import Commands

class Receiver:
    def __init__(self, client):
        self.client = client
        # commands default
        self.cm = -2
        t = threading.Thread(target=self.run, args=())
        t.setDaemon = True
        t.start()

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
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
        except socket.error as msg:
            print(str(msg))


    def run(self):
        while True:
            try:
                self.client.sendall(str(self.cm).encode('utf8'))
                print("send command: ", self.cm)
                self.client.recv(1024)

                if self.cm == Commands.LOG_FACE_DETECTOR.value:
                    self.receiverLogFaceName()
                elif self.cm == Commands.IMAGE.value:
                    self.receiverImage()
            except socket.error as msg:
                print(str(msg))
                print("Receiver error")
