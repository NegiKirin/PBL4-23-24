import socket
import threading
import time
from Receiver import Receiver

class client:
    def __init__(self, host="127.0.0.1", port=9999):
        self.host = host
        self.port = port
        self.s = None
        self.create_socket()
        self.connect_socket()

        Receiver(self.s)
       
    #Function create socket
    def create_socket(self):
        try:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print('Has been create socket client')
        except socket.error as msg:
            print(str(msg)+'. Trying to create socket client again...')
            self.create_socket()

    #Function connect socket server
    def connect_socket(self):
        try:
            self.s.connect((self.host, self.port))
            print('Established connection with PORT = ' + str(self.port))
        except socket.error as msg:
            print(str(msg) + ' Trying to connect...')
            self.connect_socket()

    #Function close socket
    def close_socket(self):
        if self.s != None:
            try:
                self.s.close()
                print('Close socket')
            except socket.error as msg:
                print(str(msg) + ' Trying to close')
                self.close_socket()

def main():
    c = client()

if __name__ == '__main__':
    main()