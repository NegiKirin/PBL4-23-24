import socket
import sys
import jpysocket

class client:
    def __init__(self, host='', port=9999):
        self.host = host
        self.port = port
        self.s = None
       
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

    #Function cecieve data from socket server
    def recieve_socket(self):
        try:
            mess = self.s.recv(1024).decode('utf8')
            print(mess)
        except socket.error as msg:
            print(str(msg) + ' Trying to recieve')
            self.recieve_socket()
            
    #Function close socket
    def close_socket(self):
        if self.s != None:
            try:
                self.s.close()
                print('Close socket')
            except socket.error as msg:
                print(str(msg) + ' Trying to close')
                self.close_socket()

    #Function send data to socket server
    def send_socket(self, mess):
        try:
            mess_encode = jpysocket.jpyencode(mess)
            self.s.send(mess_encode)
            print('Send data to server successfully')
        except socket.error as msg:
            print(str(msg)+' .Trying to sending again...')
            self.send_socket()

