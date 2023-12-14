import pickle
import threading
import socket

import cv2

from Commands import Commands

BUFF_SIZE = 65536
HEADERSIZE = 10


class Sender:
    def __init__(self, conn):
        self.soc = conn
        # t = threading.Thread(target=self.run, args=())
        # t.setDaemon = True
        # t.start()

    def sendRoomNumber(self, roomNumber):
        try:
            print('send commands')
            self.soc.sendall(str(Commands.SEND_ROOM_NUMBER.value).encode('utf8'))
            self.soc.recv(1024)

            self.soc.sendall(str(roomNumber).encode('utf8'))

            list = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.soc.recv(16)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg
                if len(full_msg) - HEADERSIZE == msglen:
                    # print(full_msg[HEADERSIZE:])
                    list = pickle.loads(full_msg[HEADERSIZE:])
                    # print(list)
                    break
            return list
        except socket.error as e:
            print(str(e))
        except Exception as e:
            print(e)

    def sendIdSession(self, idSession, gui):
        try:
            print('send commands')
            self.soc.sendall(str(Commands.SEND_IMAGES_FOR_DEVICE.value).encode('utf8'))
            self.soc.recv(1024)

            self.soc.sendall(str(idSession).encode('utf8'))

            images = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.soc.recv(102400)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    print(msglen)
                    new_msg = False

                full_msg += msg
                # print(full_msg)
                gui.progress(int(((len(full_msg) - HEADERSIZE) / msglen) * 100))
                if len(full_msg) - HEADERSIZE == msglen:
                    # print(full_msg[HEADERSIZE:])
                    images = pickle.loads(full_msg[HEADERSIZE:])
                    # print(list)
                    break
            self.soc.sendall('Done'.encode('utf8'))
            
            
            
            # ===== SHOW IMAGE ====
            # for image in images:
            #     cv2.imshow("Image", image)
            #     cv2.waitKey(1000)  # waitKey(ms)
            
            users = None
            full_msg = b''
            new_msg = True
            while True:
                msg = self.soc.recv(102400)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    # print(msg)
                    new_msg = False

                full_msg += msg
                # print(full_msg)
                gui.progress(int(((len(full_msg) - HEADERSIZE) / msglen) * 100))
                if len(full_msg) - HEADERSIZE == msglen:
                    # print(full_msg[HEADERSIZE:])
                    users = pickle.loads(full_msg[HEADERSIZE:])
                    # print(list)
                    break

            
            gui.startDetector(images, users)
            return images, users
        except socket.error as e:
            print(str(e))
        except Exception as e:
            print(e)