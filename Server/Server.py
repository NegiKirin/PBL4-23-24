import pickle
import socket
import sys
import threading
import time

from PyQt5.QtWidgets import QApplication

import HandlerClient
import Client
from Module import FaceDetector
import checkin
import dao
import serial
from New_Interface.main_gui import MainWindow

class server:

    def __init__(self):
        self.soc = None
        self.soc_UDP = None
        self.face_names = []
        self.host = "127.0.0.1"
        self.port = 9999
        self.create_socket()
        self.create_socket_UDP()
        self.binding_socket()
        self.listening_socket(1)
        t = threading.Thread(target=self.accept_socket, args=())
        t.setDaemon = True
        t.start()

        # construct detector
        self.handlerClient = HandlerClient.handlerClient()
        # self.detector = FaceDetector.face_detector(cam=0)
        self.detector = checkin.face_detector(cam=0)

        # draw gui
        app = QApplication(sys.argv)
        main_win = MainWindow(detector=self.detector)
        main_win.show()

        # load data
        self.detector.load_data()
        t1 = threading.Thread(target=self.detector.face_detection, args=[main_win])
        t1.setDaemon = True
        t1.start()

        # Arduino
        # self.arduino = serial.Serial(port="COM6", baudrate=9600, timeout=2)
        self.arduino = None
        sys.exit(app.exec())


    def create_socket(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Has been created a socket server')
        except socket.error as msg:
            print(str(msg) + ' .Trying to connecting again...')
            self.create_socket()

    def create_socket_UDP(self):
        try:
            self.soc_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.soc_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        except socket.error as msg:
            print(str(msg))
            # self.create_socket_UDP()

    def binding_socket(self):
        try:
            self.soc.bind((self.host, self.port))
            self.soc_UDP.bind((self.host, self.port))
            print('Binding id = ' + str(self.host) + ' port = ' + str(self.port))
        except socket.error as msg:
            print(str(msg) + ' .Trying to binding socket again...')
            # self.binding_socket()

    def listening_socket(self, time):
        try:
            self.soc.listen(time)
        except socket.error as msg:
            print(str(msg) + '\n' + 'Trying to listening ' + str(time) + ' s...')
            # self.listening_socket(time)

    def accept_socket(self):
        while True:
            try:
                conn, address = self.soc.accept()
                print('Establish connection with IP = ' + str(address[0]) + " | PORT = " + str(address[1]))

                # data = conn.recv(3000)
                # account = pickle.loads(data)
                # print(account)
                # if False:
                #     conn.close()
                client = Client.Client((conn, address), self.soc_UDP, self.detector, self.arduino)
                self.handlerClient.appendClient(client)
            except socket.error as msg:
                print(str(msg) + '\n' + 'Trying to accept...')

    # Function close socket
    def close_socket(self):
        try:
            self.soc.close()
        except socket.error as msg:
            print(str(msg) + ' Trying to close socket...')
            # self.close_socket()


def main():
    sv = server()


if __name__ == "__main__":
    main()
