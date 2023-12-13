import socket
import sys
import threading

from PyQt5.QtWidgets import QApplication

from New_Interface.main_gui import MainWindow
from Receiver import Receiver
import checkin
from Sender import Sender


class Device:
    def __init__(self):
        self.soc = None
        self.host = "127.0.0.1"
        self.port = 9999

        self.create_socket()
        self.connect_socket()

        self.sender = Sender(self.soc)

        self.detector = checkin.face_detector(cam=0)

        # draw gui
        app = QApplication(sys.argv)
        main_win = MainWindow(detector=self.detector, sender=self.sender)
        main_win.show()

        # self.detector.load_data()
        # t1 = threading.Thread(target=self.detector.face_detection, args=[main_win])
        # t1.setDaemon = True
        # t1.start()

        self.arduino = None
        sys.exit(app.exec())


    def create_socket(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Has been created a socket server')
        except socket.error as msg:
            print(str(msg) + ' .Trying to connecting again...')
            self.create_socket()

    def connect_socket(self):
        try:
            self.soc.connect((self.host, self.port))
            print('Established connection with PORT = ' + str(self.port))
            self.soc.sendall(str(0).encode('utf8'))
        except socket.error as msg:
            print(str(msg) + ' Trying to connect...')
            self.connect_socket()

    def close_socket(self):
        if self.soc is not None:
            try:
                self.soc.close()
                print('Close socket')
            except socket.error as msg:
                print(str(msg) + ' Trying to close')
                self.close_socket()


if __name__ == '__main__':
    d = Device()