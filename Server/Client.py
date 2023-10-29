from threading import Thread, Event
import time
import datetime
import socket
from Commands import Commands
import pickle
import struct

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




    def run(self):
        while True:
            print("Waiting command")
            try:
                cm = self.client.socket.recv(1024)
                self.client.socket.sendall(cm)
                cm = int(cm.decode('utf8'))
                print("New command", cm)
                # self.cm = self.client.socket.recv(1024).decode('utf8')
                if cm == Commands.LOG_FACE_DETECTOR.value:
                    self.sendLogFaceDetector()
                elif cm == Commands.IMAGE.value:
                    self.sendImage()
            except socket.error as error:
                print(str(error))
                self.client.active = False
                break
