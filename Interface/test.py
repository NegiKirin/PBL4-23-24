import typing
from PyQt6 import QtCore,QtGui, QtWidgets, uic
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import *
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidgetAction, QMenuBar, QMenu, QSizePolicy, QLabel, QVBoxLayout, QWidget 
from PyQt6.QtGui import QWindow, QScreen,QImage, QPixmap
from PyQt6.uic import loadUi
import sys
import numpy as np

import matplotlib 
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


# cửa sổ 
class Monitor_w(QMainWindow):
    def __init__(self, widget = None):
        super(Monitor_w, self).__init__()
        loadUi('Monitor.ui',self)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
    #xử lý chuyển cửa sổ
    def loadMenu2(self):
        self.widget.setCurrentIndex(1)
    def loadMenu3(self):
        self.widget.setCurrentIndex(2)
    def loadMenu4(self):
        self.widget.setCurrentIndex(3)
    def loadMenu5(self):
        sys.exit()
    #truyền dữ liệu vào để view
    def LoadingData(self,t,o):
        self.temperature.setText(str(t))
        self.wet.setText(str(o))

class List_w(QMainWindow):
    def __init__(self, widget=None):
        super(List_w, self).__init__()
        uic=loadUi('List.ui',self)
        self.menu1.clicked.connect(self.loadMenu1)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
        self.search.setStyleSheet("border-radius: 10px; padding: 8px;")
        #Ở màn hình List, thiết lập chiều rộng của các cột trong bảng 
        self.tableList.setColumnWidth(0,100)
        self.tableList.setColumnWidth(1,246)
        self.tableList.setColumnWidth(2,246)
        self.tableList.setColumnWidth(3,246)
        # phân trang
        self.page=0
        self.length=0
        self.previousButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)
        self.button1.clicked.connect(self.number1)
        self.button2.clicked.connect(self.number2)
        self.button3.clicked.connect(self.number3)
        self.button4.clicked.connect(self.number4)
        self.button5.clicked.connect(self.number5)
        #khởi tạo giá trị của các button số trang
        self.a1=1
        self.a2=2
        self.a3=3
        self.a4=4
        self.a5=5
        #Tìm kiếm khi nhấn nút enter
        #self.search.returnPressed.connect(self.LoadingData)

    #xử lý chuyển cửa sổ
    def loadMenu1(self):
        self.widget.setCurrentIndex(0)
    def loadMenu2(self):
        self.widget.setCurrentIndex(1)
    def loadMenu4(self):
        self.widget.setCurrentIndex(3)
    def loadMenu5(self):
        sys.exit()
    #xử lý phân trang của view
    def decreaseValueButton(self):
        self.a1= int(self.button1.text()) -1
        self.a2= int(self.button2.text()) -1
        self.a3= int(self.button3.text()) -1
        self.a4= int(self.button4.text()) -1
        self.a5= int(self.button5.text()) -1
    def increaseValueButton(self):
        self.a1= int(self.button1.text()) +1
        self.a2= int(self.button2.text()) +1
        self.a3= int(self.button3.text()) +1
        self.a4= int(self.button4.text()) +1
        self.a5= int(self.button5.text()) +1
    def previous(self):
        if self.page != 0:
            self.page-=1
            if int(self.button1.text())>1 :
                self.decreaseValueButton()
        else:
            return -1
    def next(self):
        self.page+=1
        if self.length> int(self.button5.text())*10:
            self.increaseValueButton()
    def number1(self):
        self.page = int(self.button1.text()) -1
        i= self.page+1
        if i==2:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        elif i>=3:
            self.a1= i-2
            self.a2= i-1
            self.a3= i
            self.a4= i+1
            self.a5= i+2
    def number2(self):
        self.page = int(self.button2.text())-1
        i= self.page+1
        if i==3:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        elif i>=4:
            self.a1= i-2
            self.a2= i-1
            self.a3= i
            self.a4= i+1
            self.a5= i+2
    def number3(self):
        self.page = int(self.button3.text())-1
        i= self.page+1
    def number4(self):
        self.page = int(self.button4.text())-1
        i= self.page +1
        self.a1= i-2
        self.a2= i-1
        self.a3= i
        self.a4= i+1
        self.a5= i+2    
    def number5(self):
        self.page = int(self.button5.text())-1
        i= self.page +1
        self.a1= i-2
        self.a2= i-1
        self.a3= i
        self.a4= i+1
        self.a5= i+2    
    #hàm truyền dữ liệu vào để view
    def LoadingData(self, list):
        #kiểm tra trong lineEdit search đã có thông tin gì chưa
        inf = self.search.text()
        print(inf)
        if inf =="": 
            self.tableList.setRowCount(10)
            self.length = len(list)
            row=-1
            for i in range(30*self.page,30*self.page+30,3): 
                if i<len(list):
                    row+=1
                    id = QtWidgets.QTableWidgetItem(str(int((i/3)+1)))
                    self.tableList.setItem(row, 0, id)
                    self.tableList.setItem(row, 1, QtWidgets.QTableWidgetItem(list[i]))
                    self.tableList.setItem(row, 2, QtWidgets.QTableWidgetItem(list[i+1]))
                    self.tableList.setItem(row, 3, QtWidgets.QTableWidgetItem(list[i+2]))
            self.tableList.verticalHeader().setVisible(False)
        else:
            row=-1
            #self.tableList.setRowCount(10)
            self.tableList.clearContents()            
            for i in range(0,len(list), 3): 
                if (inf in list[i]) or (inf in list[i+1]) or (inf in list[i+2]):
                    row+=1
                    id = QtWidgets.QTableWidgetItem(str((i/3)+1))
                    self.tableList.setItem(row, 0, id)
                    self.tableList.setItem(row, 1, QtWidgets.QTableWidgetItem(list[i]))
                    self.tableList.setItem(row, 2, QtWidgets.QTableWidgetItem(list[i+1]))
                    self.tableList.setItem(row, 3, QtWidgets.QTableWidgetItem(list[i+2]))
            self.tableList.verticalHeader().setVisible(False)
        #cập nhật giá trị button
        self.button1.setText(str(self.a1)) 
        self.button2.setText(str(self.a2)) 
        self.button3.setText(str(self.a3)) 
        self.button4.setText(str(self.a4)) 
        self.button5.setText(str(self.a5)) 

class History_w(QMainWindow):
    def __init__(self, widget=None):
        super(History_w, self).__init__()
        uic=loadUi('History.ui',self)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu1.clicked.connect(self.loadMenu1)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
        self.search.setStyleSheet("border-radius: 10px; padding: 8px;")
        # Ở màn hình History, định dạng kích thước cột trong table
        self.tableHistory.setColumnWidth(0,100)
        self.tableHistory.setColumnWidth(1,246)
        self.tableHistory.setColumnWidth(2,246)
        self.tableHistory.setColumnWidth(3,246)
        # phân trang
        self.page=0
        self.length=0
        self.previousButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)
        self.button1.clicked.connect(self.number1)
        self.button2.clicked.connect(self.number2)
        self.button3.clicked.connect(self.number3)
        self.button4.clicked.connect(self.number4)
        self.button5.clicked.connect(self.number5)
        #khởi tạo giá trị của các button số trang
        self.a1=1
        self.a2=2
        self.a3=3
        self.a4=4
        self.a5=5
        #Tìm kiếm khi nhấn nút enter
        #self.search.returnPressed.connect(self.LoadingData)
    #xử lý chuyển cửa sổ
    def loadMenu3(self):
        self.widget.setCurrentIndex(2)
    def loadMenu1(self):
        self.widget.setCurrentIndex(0)
    def loadMenu4(self):
        self.widget.setCurrentIndex(3)
    def loadMenu5(self):
        sys.exit()
    #xử lý phân trang của view
    def decreaseValueButton(self):
        self.a1= int(self.button1.text()) -1
        self.a2= int(self.button2.text()) -1
        self.a3= int(self.button3.text()) -1
        self.a4= int(self.button4.text()) -1
        self.a5= int(self.button5.text()) -1
    def increaseValueButton(self):
        self.a1= int(self.button1.text()) +1
        self.a2= int(self.button2.text()) +1
        self.a3= int(self.button3.text()) +1
        self.a4= int(self.button4.text()) +1
        self.a5= int(self.button5.text()) +1
    def previous(self):
        if self.page != 0:
            self.page-=1
            if int(self.button1.text())>1 :
                self.decreaseValueButton()
        else:
            return -1
    def next(self):
        self.page+=1
        if self.length> int(self.button5.text())*10:
            self.increaseValueButton()
    def number1(self):
        self.page = int(self.button1.text()) -1
        i= self.page+1
        if i==2:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        elif i>=3:
            self.a1= i-2
            self.a2= i-1
            self.a3= i
            self.a4= i+1
            self.a5= i+2
    def number2(self):
        self.page = int(self.button2.text())-1
        i= self.page+1
        if i==3:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        elif i>=4:
            self.a1= i-2
            self.a2= i-1
            self.a3= i
            self.a4= i+1
            self.a5= i+2
    def number3(self):
        self.page = int(self.button3.text())-1
        i= self.page+1
    def number4(self):
        self.page = int(self.button4.text())-1
        i= self.page +1
        self.a1= i-2
        self.a2= i-1
        self.a3= i
        self.a4= i+1
        self.a5= i+2    
    def number5(self):
        self.page = int(self.button5.text())-1
        i= self.page +1
        self.a1= i-2
        self.a2= i-1
        self.a3= i
        self.a4= i+1
        self.a5= i+2    
        
   #hàm truyền dữ liệu vào để view
    def LoadingData(self, history):
        #kiểm tra trong lineEdit search đã có thông tin gì chưa
        inf = self.search.text()
        print(inf)
        if inf =="": 
            self.tableHistory.setRowCount(10)
            self.length = len(history)
            row=-1
            for i in range(30*self.page,30*self.page+30,3): 
                if i<len(history):
                    row+=1
                    id = QtWidgets.QTableWidgetItem(str(int((i/3)+1))) #sua
                    self.tableHistory.setItem(row, 0, id)
                    self.tableHistory.setItem(row, 1, QtWidgets.QTableWidgetItem(history[i]))
                    self.tableHistory.setItem(row, 2, QtWidgets.QTableWidgetItem(history[i+1]))
                    self.tableHistory.setItem(row, 3, QtWidgets.QTableWidgetItem(history[i+2]))
            self.tableHistory.verticalHeader().setVisible(False)
        else:
            row=-1
            #self.tableHistory.setRowCount(10)
            self.tableHistory.clearContents()            
            for i in range(0,len(history),3): 
                if (inf in history[i]) or (inf in history[i+1]) or (inf in history[i+2]):
                    row+=1
                    id = QtWidgets.QTableWidgetItem(str((i/3)+1)) 
                    self.tableHistory.setItem(row, 0, id)
                    self.tableHistory.setItem(row, 1, QtWidgets.QTableWidgetItem(history[i]))
                    self.tableHistory.setItem(row, 2, QtWidgets.QTableWidgetItem(history[i+1]))
                    self.tableHistory.setItem(row, 3, QtWidgets.QTableWidgetItem(history[i+2]))
            self.tableHistory.verticalHeader().setVisible(False)
        #cập nhật giá trị button
        self.button1.setText(str(self.a1)) 
        self.button2.setText(str(self.a2)) 
        self.button3.setText(str(self.a3)) 
        self.button4.setText(str(self.a4)) 
        self.button5.setText(str(self.a5)) 

class Temperature_w(QMainWindow):
    def __init__(self, widget=None):
        super(Temperature_w, self).__init__()
        uic=loadUi('temperature.ui',self)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu1.clicked.connect(self.loadMenu1)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget

        #KHỞI TẠO ĐỐI TƯỢNG Ở MÀN HÌNH TEMPERATURE
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=9.41, height=5.01, dpi=100)
        self.sc.move(280,10)
        self.X = [0]
        self.Y = [0]
        Xmin, Xmax, Ymin, Ymax = 0, 20, 0, 100
        self.sc.axes.axis([Xmin, Xmax, Ymin, Ymax])
        # self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

    #xử lý chuyển cửa sổ
    def loadMenu2(self):
        self.widget.setCurrentIndex(1)
    def loadMenu3(self):
        self.widget.setCurrentIndex(2)
    def loadMenu1(self):
        self.widget.setCurrentIndex(0)
    def loadMenu5(self):
        sys.exit()

    def setPlot(self):
        if(len(self.X) <= 20):
            self.X.append(self.X[-1] + 1)
            self.Y.append(np.random.randint(10, 50, size=1)[-1])
        else:
            self.Y.pop(0)
            self.Y.append(np.random.randint(10, 50, size=1)[-1])
            self.sc.axes.clear()
            self.sc.axes.axis([self.X[0], self.X[-1], 0, 100])
        self.sc.axes.plot(self.X, self.Y, color='red')
        self.sc.draw()

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=9.41, height=5.01, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class GUI:
    #HÀM KHỞI TẠO
    def __init__(self):

        # new một cửa số và widget
        self.app = QApplication(sys.argv)
        self.widget =QtWidgets.QStackedWidget()

        #Lưu 4 hàm cửa sổ widget trên về biến
        self.Monitor_f= Monitor_w(widget=self.widget)
        self.History_f = History_w(widget=self.widget)
        self.List_f = List_w(widget=self.widget)
        self.Temperature_f = Temperature_w(widget=self.widget)
        #add widget vào 
        self.widget.addWidget(self.Monitor_f)      #index0
        self.widget.addWidget(self.History_f)      #index1
        self.widget.addWidget(self.List_f)         #index2
        self.widget.addWidget(self.Temperature_f)  #index3

        #tạo một widget Timer để cập nhật dữ liệu
        self.monitor_timer = QTimer()
        self.timer = QTimer()
        self.history_timer = QTimer()
        self.list_timer = QTimer()
        self.temperature_timer = QTimer()
        
        #KHỞI TẠO ĐỐI TƯỢNG Ở MÀN HÌNH MONITOR     
        #Tạo một Label để load hình ảnh ở Monitor
        self.imagine = QLabel(self.Monitor_f)
        self.imagine.move(270,110)
        self.imagine.resize(981,481)
        #tạo 1 frame
        self.frame = None
        
        
    #HÀM SET DỮ LIỆU
    def setTemp(self, tt, pp):
        self.t= tt
        self.o = pp
    def setCapture(self, frame):
        self.frame = frame
    def setL(self, list):
        self.list = list
    def setH(self, list):
        self.history= list

    #HÀM THIẾT LẬP KÍCH THƯỚC CỬA SỔ
    def setSize(self):
        #cố định kích thước
        self.widget.setFixedHeight(650)
        self.widget.setFixedWidth(1300)

    #CÁC HÀM HIỂN THỊ DỮ LIỆU LÊN MÀN HÌNH
    #
    def setMonitor(self):
        # #truyền dữ liệu vào hàm 1
        self.Monitor_f.LoadingData(self.t,self.o)
        self.widget.show()
    #
    def updateCapture(self):
        # Tạo một video capture 
        try:
            height, width, channel = self.frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.imagine.setPixmap(pixmap)
        except:
            print("error")
    #
    def setHistory(self):
        self.History_f.LoadingData(self.history)
        self.widget.show()
    #
    def setList(self):
        self.List_f.LoadingData(self.list)
        self.widget.show()
    #
    def setTemperature(self):
        self.Temperature_f.setPlot()
        self.widget.show()

    #CÁC HÀM THIẾT LẬP THỜI GIAN ĐỂ CẬP NHẬT LẠI DỮ LIỆU
    #ở màn hình Monitor
    def setTimer_Monitor(self):
        i0= self.widget.currentIndex()
        if i0 ==0:
            self.monitor_timer.timeout.connect(self.setMonitor)
            self.monitor_timer.start(2000) #cập nhật giao diện 
    def setTimer(self):
        i0= self.widget.currentIndex()
        if i0 ==0:
            self.monitor_timer.timeout.connect(self.updateCapture)
            self.monitor_timer.start(16)
    #ở màn hình history
    def setTimer_History(self):
        i1= self.widget.currentIndex()
        if i1 ==1:
            self.monitor_timer.timeout.connect(self.setHistory)
            self.monitor_timer.start(100) #cập nhật giao diện
    #ở màn hình list 
    def setTimer_List(self):
        i2= self.widget.currentIndex()
        if i2 ==2:
            self.monitor_timer.timeout.connect(self.setList)
            self.monitor_timer.start(2000) #cập nhật giao diện 5 giây
    #ở màn hình Temperture
    def setTimer_Temperature(self):
        i3= self.widget.currentIndex()
        if i3 ==3:
            self.temperature_timer.timeout.connect(self.setTemperature)
            self.temperature_timer.start(1000)
    
    

    #HÀM CHÍNH
    def draw(self):
        #chọn widget khi chương trình khởi chạy
        self.widget.setCurrentIndex(0)
    def exitWin(self):
        # thoát khi xong việc
        self.app.exec()


