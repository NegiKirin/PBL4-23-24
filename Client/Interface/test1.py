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
cap = cv2.VideoCapture(0)
gui.setTimer()
t2 = threading.Thread(target=set_frame, args=())
t2.setDaemon(True)
t2.start()

# # HIỂN THỊ HISTORY
# history = [["0","Tín","23-12-9 8:30", "23-12-9 9:30"],
#            ["1","Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
#            ["2","Phúc", "23-12-9 8:30", "23-12-9 9:30"],
#            ["3","Tín","23-12-9 8:30", "23-12-9 9:30"],
#            ["4","Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
#            ["5","Phúc", "23-12-9 8:30", "23-12-9 9:30"],
#            ["6","Tín","23-12-9 8:30", "23-12-9 9:30"],
#            ["7","Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
#            ["8","Phúc", "23-12-9 8:30", "23-12-9 9:30"],
#            ["9","Tín","23-12-9 8:30", "23-12-9 9:30"],
#            ["10","Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
#            ["11","Phúc", "23-12-9 8:30", "23-12-9 9:30"],
#            ["12","Tín","23-12-9 8:30", "23-12-9 9:30"],
#            ["12","Hiếu", "23-12-9 8:30", "23-12-9 9:30"], 
#            ["14","Phúc", "23-12-9 8:30", "23-12-9 9:30"],
#             ]
# gui.setH(history)
# gui.setHistory()

# HIỂN THỊ LIST
# list = [["1","Tín", "21TCLC_KHDL2", "CNTT"],
#         ["2","Hiếu", "21TCLC_KHDL2", "CNTT"],
#         ["3","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["4","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["5","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["6","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["7","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["8","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["9","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["10","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["11","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["12","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["13","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["14","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["15","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["16","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["17","Phúc", "21TCLC_KHDL2", "CNTT"],
#         ["18","Phúc", "21TCLC_KHDL2", "CNTT"]
#         ]
# gui.setL(list)
# gui.setList()



#HIỂN THỊ BIỂU ĐỔ
# gui.setTemperature()
# gui.setTimer_Temperature()
gui.exitWin()


