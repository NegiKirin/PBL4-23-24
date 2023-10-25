import gui
import time
import threading
import cv2

#   HÀM CHẠY REAL-TIME NHIỆT ĐỘ ĐỘ ẨM
def setT():                          
    t=10
    o=50
    while True:
        gui.setTemp(t, o)
        time.sleep(5)
        t+=10
        o+=1
# HÀM CHẠY REAL TIME PHÁT VIDEO
def set_frame():            
    # time.sleep(5)          
    ret, frame = cap.read()
    while ret:
        ret, frame = cap.read()
        gui.setCapture(frame)
        time.sleep(1/24)

#   HIỂN THỊ MÀN HÌNH
gui = gui.GUI()
gui.draw()
gui.setSize()

#HIỂN THỊ NHIỆT ĐỘ ĐỘ ẨM - REAL TIME
gui.setTemp('22','56%')
gui.setMonitor()
gui.setTimer_Monitor()
t = threading.Thread(target=setT, args=[])
t.setDaemon(True)
t.start()

#HIỂN THỊ VIDEO
cap = cv2.VideoCapture('video.mp4')
gui.setTimer()
t2 = threading.Thread(target=set_frame, args=())
t2.setDaemon(True)
t2.start()

# HIỂN THỊ HISTORY
history = [["Tín","23-12-9 8:30", "23-12-9 9:30"],
           ["Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
           ["Phúc", "23-12-9 8:30", "23-12-9 9:30"],
           ["Tín","23-12-9 8:30", "23-12-9 9:30"],
           ["Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
           ["Phúc", "23-12-9 8:30", "23-12-9 9:30"],
           ["Tín","23-12-9 8:30", "23-12-9 9:30"],
           ["Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
           ["Phúc", "23-12-9 8:30", "23-12-9 9:30"],
           ["Tín","23-12-9 8:30", "23-12-9 9:30"],
           ["Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
           ["Phúc", "23-12-9 8:30", "23-12-9 9:30"],
           ["Tín","23-12-9 8:30", "23-12-9 9:30"],
           ["Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
           ["Phúc", "23-12-9 8:30", "23-12-9 9:30"],
            ]
gui.setH(history)
gui.setHistory()
# gui.setTimer_History()
# HIỂN THỊ LIST
list = [["Tín", "21TCLC_KHDL2", "CNTT"],
        ["Hiếu", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"],
        ["Phúc", "21TCLC_KHDL2", "CNTT"]
        ]
gui.setL(list)
gui.setList()
# gui.setTimer_List()
#Xử lý Timer:
# gui.setTotalTimer()

#HIỂN THỊ BIỂU ĐỔ
# gui.setTemperature()
# gui.setTimer_Temperature()
gui.exitWin()



