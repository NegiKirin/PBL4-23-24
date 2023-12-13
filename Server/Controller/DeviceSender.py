import os
import socket
import sys

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Util.Commands import Commands


class DeviceSender:
    def __init__(self, conn):
        self.socket = conn
        self.active = True
        self.data = '../../database'

    def sendImage(self):
        print('send image')

    def run(self):
        while True:
            try:
                cm = self.socket.recv(1024).decode('utf8')

                if cm == Commands.SEND_IMAGE_FOR_DEVICE.value:
                    self.sendImage()
                # elif cm == Commands

            except socket.error as error:
                print(error)
                self.isAlive = False
            except Exception as e:
                print(str(e))