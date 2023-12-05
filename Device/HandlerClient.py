import socket
import time
import threading
import Client

class handlerClient:
    def __init__(self):
        self.clients = []

        #run
        t = threading.Thread(target=self.checkActive, args=())
        t.setDaemon = True
        t.start()

    def appendClient(self, client):
        self.clients.append(client)

    def removeClient(self, client):
        self.clients.remove(client)

    def checkActive(self):
        while True:
            for client in self.clients:
                if client.active == False:
                    self.removeClient(client)
                    print("remove client")
            time.sleep(1)

    def sendListForAllClient(self, list):
        for client in self.clients:
            client.send_list(list)