from threading import Thread, Event
import time
import datetime
import socket
from Commands import Commands


class Client:
    def __init__(self, conn, detector):
        # attribute of client
        self.socket = conn
        self.detector = detector
        self.active = True

        # run
        self.t = Thread(target=self.run, args=())
        self.t.setDaemon = True
        self.t.start()

    def run(self):
        CommandsSender(self, self.detector)

    def close_socket(self):
        self.client.close()


class CommandsSender:
    def __init__(self, client, detector):
        self.client = client
        self.detector = detector

        # run
        self.t = Thread(target=self.sendLogFaceDetector, args=())
        # self.t.setDaemon = True
        self.t.start()

    def sendLogFaceDetector(self):
        while True:
            msg = ''
            currentTime = datetime.datetime.now()
            msg = '[' + str(currentTime.year) + '-' + str(currentTime.month) + '-' + str(currentTime.day) + ' ' + str(
                currentTime.hour) + ':' + str(currentTime.minute) + ':' + str(currentTime.second) + ':' + ']' + ' : '
            for name in self.detector.face_names:
                msg = msg + name
            try:
                self.client.socket.sendall(str(Commands.LOG_FACE_DETECTOR.value).encode('utf8'))
                self.client.socket.recv(1024)
                self.client.socket.sendall(msg.encode("utf8"))
                self.client.socket.recv(1024)
            except socket.error as error:
                self.client.active = False
                print("Client disconnect")
                break
            time.sleep(1)
