import threading
import socket
from Commands import Commands

class Receiver:
    def __init__(self, client):
        self.client = client

        t = threading.Thread(target=self.run, args=())
        t.setDaemon = True
        t.start()

    def receiverLogFaceName(self):
        try:
            mess = self.client.recv(1024).decode('utf8')
            self.client.sendall(mess.encode('utf8'))
            print(mess)
            return mess
        except socket.error as msg:
            print(str(msg))

    def run(self):
        while True:
            print("Waiting command")
            try:
                cm = int(self.client.recv(1024).decode('utf8'))
                self.client.sendall(str(cm).encode('utf8'))
                print("New command", cm)
                # if cm == Commands.LOG_FACE_DETECTOR.value:
                #     self.receiverLogFaceName()
            except:
                print("Receiver error")
