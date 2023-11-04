import gui
import threading
import time
import cv2

#LUỒNG CẬP NHẬT THAY ĐỔI GIÁ TRỊ CỦA NHIỆT ĐỘ ĐỘ ẨM
def setTempThread():
    t=10
    o=50
    while True:
        gui.setTemp(t, o)
        time.sleep(5)
        t+=10
        o+=1
#LUỒNG CẬP NHẬT THAY ĐỔI FRAME THEO THỜI GIAN
def setFrameThread():
    ret, frame = video.read()
    while ret:
        ret, frame = video.read()
        gui.setFrame(frame)
        time.sleep(1/30)

gui = gui.GUI()
gui.setSize()
gui.draw()

#Ở MÀN HÌNH GIÁM SÁT
#set dữ liệu và hiển thị nhiệt độ độ ẩm
gui.setTemp(tt=20, pp= 56)
gui.setMonitor()
gui.setTimer_Monitor()
t= threading.Thread(target=setTempThread, args=[], daemon=True)
t.start()
#lấy video và tiến hành đưa vào luồng để đọc và hiển thị video
video = cv2.VideoCapture(0)
gui.setTimer()
t1 = threading.Thread(target=setFrameThread, args=(), daemon=True)
t1.start()

gui.exitWin()


