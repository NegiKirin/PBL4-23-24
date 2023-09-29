import socket
import threading
import time
import HandlerClient
import Client
class server:

    def __init__(self):
        self.soc = socket.socket()
        self.face_names = []
        self.host = "127.0.0.1"
        self.port = 9999
        self.create_socket()
        self.binding_socket()
        self.listening_socket(1)
        self.t = threading.Thread(target=self.accept_socket, args=())
        self.t.setDaemon = True
        self.t.start()
        self.handlerClient = HandlerClient.handlerClient()

    def setFaceName(self, name):
        self.face_names = name

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
                client = Client.Client(conn)
                self.handlerClient.appendClient(client)
            except socket.error as msg:
                print(str(msg) + '\n' + 'Trying to accept...')
        # Function send message to client

    def send_socket(self, conn):
        try:
            for x in self.face_names:
                conn.sendall(x.encode("utf8"))
                # waiting response
                conn.recv(1024)
            msg = "end"
            conn.sendall(msg.encode("utf8"))
            time.sleep(3)
            print(self.face_names)
            print('Have send message to client')
        except socket.error as msg:
            print(str(msg) + ' Trying to send again...')
            self.send_socket(conn)

    # Function close socket
    def close_socket(self):
        try:
            self.soc.close()
        except socket.error as msg:
            print(str(msg) + ' Trying to close socket...')
            self.close_socket()
