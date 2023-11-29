import pickle
import socket
import threading
import time
from Receiver import Receiver
import Interface.gui as itf


class client:
    def __init__(self, host="127.0.0.1", port=9999):
        self.host = host
        self.port = port
        self.soc = None
        self.soc_UDP = None
        self.create_socket()
        self.create_socket_UDP()
        self.binding_socket_UDP()
        self.connect_socket()

        # self.login()

        self.receiver = Receiver(self.soc, self.soc_UDP)
        self.gui = itf.GUI(receiver=self.receiver)
        self.receiver.setGUI(self.gui)
        self.receiver.start()

        self.gui.draw()

    def login(self):
        username = input("username: ")
        password = input("password: ")
        data = pickle.dumps((username, password))
        self.soc.sendall(data)

    # Function create socket
    def create_socket(self):
        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Has been create socket client')
        except socket.error as msg:
            print(str(msg) + '. Trying to create socket client again...')
            self.create_socket()

    def create_socket_UDP(self):
        try:
            self.soc_UDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.soc_UDP.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 65536)
        except socket.error as msg:
            print(str(msg))
            self.create_socket_UDP()

    def binding_socket_UDP(self):
        try:
            # local_name = socket.gethostname()
            # local_ip = socket.gethostbyname(local_name)
            self.soc_UDP.bind(('0.0.0.0', 0))
        except socket.error as msg:
            print(str(msg))
            self.binding_socket_UDP()

    # Function connect socket server
    def connect_socket(self):
        try:
            self.soc.connect((self.host, self.port))
            print('Established connection with PORT = ' + str(self.port))
        except socket.error as msg:
            print(str(msg) + ' Trying to connect...')
            self.connect_socket()

    # Function close socket
    def close_socket(self):
        if self.soc != None:
            try:
                self.soc.close()
                print('Close socket')
            except socket.error as msg:
                print(str(msg) + ' Trying to close')
                self.close_socket()


def main():
    c = client()


if __name__ == '__main__':
    main()
    # gui = GUI()
