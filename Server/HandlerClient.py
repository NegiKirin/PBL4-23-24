import socket
import time
import threading
import Client

class handlerClient:
    def __init__(self):
        self.clients = []

    def appendClient(self, client):
        self.clients.append(client)

    def removeClient(self, client):
        self.clients.remove(client)

