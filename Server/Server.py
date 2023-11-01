import socket
import threading
import time
import HandlerClient
import Client
from Module import FaceDetector
import dao

class server:

    def __init__(self):
        self.soc = socket.socket()
        self.face_names = []
        self.host = "127.0.0.1"
        self.port = 9999
        self.create_socket()
        self.binding_socket()
        self.listening_socket(1)
        t = threading.Thread(target=self.accept_socket, args=())
        t.setDaemon = True
        t.start()

        # detector
        self.handlerClient = HandlerClient.handlerClient()
        self.detector = FaceDetector.face_detector(cam=1)
        self.detector.load_data()
        t1 = threading.Thread(target=self.detector.face_detection, args=())
        t1.setDaemon = True
        t1.start()

    def create_socket(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Has been created a socket server')
        except socket.error as msg:
            print(str(msg) + ' .Trying to connecting again...')
            self.create_socket()

    def binding_socket(self):
        try:
            self.soc.bind((self.host, self.port))
            print('Binding port = ' + str(self.port))
        except socket.error as msg:
            print(str(msg) + ' .Trying to binding socket again...')
            self.binding_socket()

    def listening_socket(self, time):
        try:
            self.soc.listen(time)
        except socket.error as msg:
            print(str(msg) + '\n' + 'Trying to listening ' + str(time) + ' s...')
            self.listening_socket(time)

    def accept_socket(self):
        while True:
            try:
                conn, address = self.soc.accept()
                print('Establish connection with IP = ' + str(address[0]) + " | PORT = " + str(address[1]))
                client = Client.Client(conn, self.detector)
                self.handlerClient.appendClient(client)
            except socket.error as msg:
                print(str(msg) + '\n' + 'Trying to accept...')

    # Function close socket
    def close_socket(self):
        try:
            self.soc.close()
        except socket.error as msg:
            print(str(msg) + ' Trying to close socket...')
            self.close_socket()


def main():
    sv = server()


if __name__ == "__main__":
    main()