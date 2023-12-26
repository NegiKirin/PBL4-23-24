import os
import sys
import threading
import time

# from Server.Controller.DeviceReciver import DeviceReceiver


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Controller.DeviceReciver import DeviceReceiver
# from Server.Controller.DeviceReciver import DeviceReceiver


class HandlerDevice:
    def __init__(self):
        self.devices = []
        #run
        t = threading.Thread(target=self.checkActive, args=())
        t.start()

    def appendDevice(self, conn):
        device = DeviceReceiver(conn)
        self.devices.append(device)

    def removeDevice(self, device):
        self.devices.remove(device)

    def checkActive(self):
        while True:
            for device in self.devices:
                if device.active == False:
                    self.removeDevice(device)
                    print("remove device")
            time.sleep(1)
