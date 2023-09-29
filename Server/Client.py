
import socket

class Client:
    def __init__(self, conn):
        # attribute of client
        self.client =  conn

    def send_list(self, list):
        try:
            for x in list:
                self.client.send(x.encode("utf8"))
                # waiting response
                self.client.recv(1024)
            msg = "end"
            self.client.send(msg.encode("utf8"))
            print(list)
            print('Have send message to client')
        except socket.error as msg:
            print(str(msg) + ' Trying to send again...')
            self.send_list(list)

    def send_str(self, str):
        try:
            self.client.send(str.encode("utf8"))
            self.client.recv(1024)
        except socket.error as msg:
            print(str(msg), "Try to send again")

    def sendFacename(self, list):
        self.send_list(self, list)