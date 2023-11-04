import sys, os
import numpy as np
from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QWidget
from PyQt6.QtCore import QTimer, QRect
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.uic import loadUi

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
print(current_directory)
sys.path.append(current_directory+"..\\")
import daoTest

class StudentInfo:
    def __init__(self, id= None, image =None, name = None, classes= None):
        self.id = id
        self.image = image
        self.name = name
        self.classes = classes

class Monitor_w(QMainWindow):
    def __init__(self, widget = None, gui = None):
        super(Monitor_w, self).__init__()
        loadUi(current_directory+'Monitor.ui',self)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
        self.gui = gui
    #xử lý chuyển cửa sổ
    def loadMenu2(self):
        self.gui.monitor_timer.stop()           
        self.gui.timer.stop()
        self.gui.widget.setCurrentIndex(1)
        self.gui.setTimer2()
        self.gui.displayInfo()
    def loadMenu3(self):
        self.gui.monitor_timer.stop()           
        self.gui.timer.stop()
        self.widget.setCurrentIndex(2)
        self.gui.clearLine()
    def loadMenu4(self):    
        self.gui.monitor_timer.stop()
        self.gui.timer.stop()
        self.gui.setTimer_Temperature() 
        self.widget.setCurrentIndex(5)
    def loadMenu5(self):
        sys.exit()
    #truyền dữ liệu vào để view
    def LoadingData(self,t,o):
        self.temperature.setText(str(t))
        self.wet.setText(str(o))

class CheckInOut_w(QMainWindow):
    def __init__(self, widget = None, gui =None):
        super(CheckInOut_w, self).__init__()
        loadUi(current_directory+'CheckInOut.ui',self)
        self.widget = widget
        self.gui = gui

        self.menu1.clicked.connect(self.loadMenu1)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.commitButton.clicked.connect(self.commitCheckInOut)

    #xử lý chuyển cửa sổ
    def loadMenu1(self):
        self.gui.timer.stop()
        self.gui.setTimer()
        self.gui.setTimer_Monitor()
        self.gui.widget.setCurrentIndex(0)
    def loadMenu3(self):
        self.gui.timer.stop()
        self.gui.widget.setCurrentIndex(2)
        self.gui.clearLine()
    def loadMenu4(self):    
        self.gui.timer.stop()
        self.gui.setTimer_Temperature() 
        self.widget.setCurrentIndex(5)
    def loadMenu5(self):
        sys.exit()
    def commitCheckInOut(self):
        #hiện tại chưa biết bấm nút xác nhận thì dữ liệu sẽ gởi về cơ sở dữ liệu như thế nào nên để return
        return

class AddStudent1_w(QMainWindow):
    def __init__(self, widget = None, gui =None):
        super(AddStudent1_w, self).__init__()
        loadUi(current_directory+'AddStudent1.ui',self)
        self.widget = widget
        self.gui = gui

        self.menu1.clicked.connect(self.loadMenu1)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.nextButton.clicked.connect(self.loadAddStudent2)
        self.cancelButton.clicked.connect(self.cancelAddStudent2)

    def loadMenu1(self):
        self.gui.setTimer()
        self.gui.setTimer_Monitor()
        self.gui.widget.setCurrentIndex(0)
    def loadMenu2(self):
        self.gui.widget.setCurrentIndex(1)
        self.gui.setTimer2()
        self.gui.displayInfo()
    def loadMenu4(self):    
        self.gui.setTimer_Temperature() 
        self.widget.setCurrentIndex(5)
    def loadMenu5(self):
        sys.exit()
    def loadAddStudent2(self):
        if len(self.nameLine.text())>0 and len(self.facultyLine.text())>0 and len(self.classLine.text())>0:
            self.gui.widget.setCurrentIndex(3)
            self.gui.setTimer3()
        else:
            return
    def cancelAddStudent2(self):
        self.gui.clearLine()

class AddStudent2_w(QMainWindow):
    def __init__(self, widget = None, gui =None):
        super(AddStudent2_w, self).__init__()
        loadUi(current_directory+'AddStudent2.ui',self)
        self.widget = widget
        self.gui = gui

        self.menu1.clicked.connect(self.loadMenu1)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.photoButton.clicked.connect(self.takePhoto)

    def loadMenu1(self):
        self.gui.setTimer()
        self.gui.setTimer_Monitor()
        self.gui.widget.setCurrentIndex(0)
    def loadMenu2(self):
        self.gui.widget.setCurrentIndex(1)
        self.gui.setTimer2()
        self.gui.displayInfo()
    def loadMenu4(self):    
        self.gui.setTimer_Temperature() 
        self.widget.setCurrentIndex(5)
    def loadMenu5(self):
        sys.exit()
    def takePhoto(self):
        self.gui.captureVideo()

class AddStudent3_w(QMainWindow):
    def __init__(self, widget = None, gui =None):
        super(AddStudent3_w, self).__init__()
        loadUi(current_directory+'AddStudent3.ui',self)
        self.widget = widget
        self.gui = gui

        self.menu1.clicked.connect(self.loadMenu1)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.commitButton.clicked.connect(self.commitData)
        self.cancelButton.clicked.connect(self.cancelData)

    def loadMenu1(self):
        self.gui.setTimer()
        self.gui.setTimer_Monitor()
        self.gui.widget.setCurrentIndex(0)
    def loadMenu2(self):
        self.gui.widget.setCurrentIndex(1)
        self.gui.setTimer2()
        self.gui.displayInfo()
    def loadMenu4(self):    
        self.gui.setTimer_Temperature() 
        self.widget.setCurrentIndex(5)
    def loadMenu5(self):
        sys.exit()

    def commitData(self):
        self.gui.widget.setCurrentIndex(2)
        self.gui.clearLine()
    def cancelData(self):
        self.gui.widget.setCurrentIndex(2)
        self.gui.clearLine()

class Temperature_w(QMainWindow):
    def __init__(self, widget=None, gui = None):
        super(Temperature_w, self).__init__()
        uic=loadUi(current_directory+'temperature.ui',self)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu1.clicked.connect(self.loadMenu1)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
        self.gui = gui
        #KHỞI TẠO ĐỐI TƯỢNG Ở MÀN HÌNH TEMPERATURE
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.temperature = MplCanvas(self.centralwidget, width=9.41, height=5.01, dpi=100)
        self.temperature.setGeometry(QRect(320, 40, 731, 181))
        self.humidity = MplCanvas(self.centralwidget, width=9.41, height=5.01, dpi=100)
        self.humidity.setGeometry(QRect(320, 260, 731, 181))
        self.X_temperature = [0]
        self.Y_temperature = [0]
        self.X_humidity = [0]
        self.Y_humidity = [0]
        Xmin, Xmax, Ymin, Ymax = 0, 20, 0, 100
        self.temperature.axes.axis([Xmin, Xmax, Ymin, Ymax])
        self.humidity.axes.axis([Xmin, Xmax, Ymin, Ymax])
        # self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

    #xử lý chuyển cửa sổ
    def loadMenu2(self):
        self.temperature.axes.clear()
        self.temperature.axes.axis([self.X_temperature[0], self.X_temperature[-1], 0, 100])

        self.X_temperature = [self.X_temperature[-1]]
        self.Y_temperature = [self.Y_temperature[-1]]
        self.gui.temperature_timer.stop()
        self.gui.widget.setCurrentIndex(1)
        self.gui.setTimer2()
        self.gui.displayInfo()
    def loadMenu3(self):
        self.temperature.axes.clear()
        self.temperature.axes.axis([self.X_temperature[0], self.X_temperature[-1], 0, 100])

        self.X = [self.X_temperature[-1]]
        self.Y = [self.Y_temperature[-1]]
        self.gui.temperature_timer.stop()
        self.gui.widget.setCurrentIndex(2)
        self.gui.clearLine()
    def loadMenu1(self):

        self.temperature.axes.clear()
        self.temperature.axes.axis([self.X_temperature[0], self.X_temperature[-1], 0, 100])

        self.X_temperature = [self.X_temperature[-1]]
        self.Y_temperature = [self.Y_temperature[-1]]
        self.gui.setTimer_Monitor()
        self.gui.setTimer()
        self.gui.temperature_timer.stop()
        self.widget.setCurrentIndex(0)
    def loadMenu5(self):
        sys.exit()

    def plotTemperature(self):
        print("print diagram Temperature")
        if (len(self.X_temperature) <= 20):
            self.X_temperature.append(self.X_temperature[-1] + 1)
            self.Y_temperature.append(np.random.randint(10, 50, size=1)[-1])
        else:
            self.X_temperature.pop(0)
            self.X_temperature.append(self.X_temperature[-1] + 1)
            self.Y_temperature.pop(0)
            self.Y_temperature.append(np.random.randint(10, 50, size=1)[-1])
            self.temperature.axes.clear()
            self.temperature.axes.axis([self.X_temperature[0], self.X_temperature[-1], 0, 100])
        self.temperature.axes.plot(self.X_temperature, self.Y_temperature, color='red')
        self.temperature.draw()
    def plotHumidity(self):
        print("print diagram Humidity")
        if (len(self.X_humidity) <= 20):
            self.X_humidity.append(self.X_humidity[-1] + 1)
            self.Y_humidity.append(np.random.randint(10, 50, size=1)[-1])
        else:
            self.X_humidity.pop(0)
            self.X_humidity.append(self.X_humidity[-1] + 1)
            self.Y_humidity.pop(0)
            self.Y_humidity.append(np.random.randint(10, 50, size=1)[-1])
            self.temperature.axes.clear()
            self.temperature.axes.axis([self.X_humidity[0], self.X_humidity[-1], 0, 100])
        self.humidity.axes.plot(self.X_humidity, self.Y_humidity, color='red')
        self.humidity.draw()

    def setPlot(self):
        self.plotTemperature()
        self.plotHumidity()

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=9.41, height=5.01, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        self.setParent(parent)

class GUI:
    #hàm khởi tạo 
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.widget = QtWidgets.QStackedWidget()

        self.Monitor_f = Monitor_w(widget=self.widget, gui= self)
        self.CheckInOut_f = CheckInOut_w(widget=self.widget, gui= self)
        self.AddStudent1_f= AddStudent1_w(widget=self.widget, gui= self)
        self.AddStudent2_f= AddStudent2_w(widget=self.widget, gui= self)
        self.AddStudent3_f= AddStudent3_w(widget=self.widget, gui= self)
        self.Temperature_f = Temperature_w(widget=self.widget, gui=self)
        #add widget vào
        self.widget.addWidget(self.Monitor_f)           #index0
        self.widget.addWidget(self.CheckInOut_f)        #index1
        self.widget.addWidget(self.AddStudent1_f)       #index2
        self.widget.addWidget(self.AddStudent2_f)       #index3
        self.widget.addWidget(self.AddStudent3_f)       #index4
        self.widget.addWidget(self.Temperature_f)       #index5

        self.student = StudentInfo(id=None, image=None, name=None, classes=None)

    #KHỞI TẠO DỮ LIỆU Ở MÀN HÌNH GIÁM SÁT
        #tạo một widget Timer để cập nhật dữ liệu
        self.monitor_timer = QTimer()
        self.timer = QTimer()
        #tạo một 1 lable để hiển thị hình ảnh
        self.imagine = QLabel(parent=self.Monitor_f)
        self.imagine.move(270,110)
        self.imagine.resize(981,481)
        #tạo 1 frame để làm biến tạm đọc dữ liệu từ video
        self.frame = None
    #KHỞI TẠO DỮ LIỆU Ở MÀN HÌNH NHIỆT ĐỘ ĐỘ ẨM
        self.temperature_timer = QTimer()

    #Ở MÀN HÌNH GIÁM SÁT
        #ĐỐI VỚI HIỂN THỊ NHIỆT ĐỘ ĐỘ ẨM
    #set dữ liệu
    def setTemp(self, tt, pp):
        self.t= tt
        self.o = pp
    #hiển thị dữ liệu
    def setMonitor(self):
        self.Monitor_f.LoadingData(t=self.t, o=self.o)
        self.widget.show()
    #cập nhật real-time
    def setTimer_Monitor(self):
        self.monitor_timer.timeout.connect(self.setMonitor)
        self.monitor_timer.start(2000)
    #ĐỐI VỚI HIỂN THỊ HÌNH ẢNH
        #set dữ liệu vào là 1 hình ảnh
    def setFrame(self, frame):
        self.frame=frame
        #hiển thị hình ảnh lên màn hình
    def displayFrame(self):
        try:
            height, width, channel = self.frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(q_image)
            self.imagine.setPixmap(pixmap)
        except:
            print("error")
        #cập nhật ảnh liên tục sau 1/60s để kết quả là 1 video
    def setTimer(self):
        self.timer.timeout.connect(self.displayFrame)
        self.timer.start(16)

    #Ở MÀN HÌNH GIÁM SÁT CHECK IN CHECK OUT

        #HIỂN THỊ CAMERA
    #hiển thị hình ảnh lên màn hình
    def displayFrame2(self):
        try:
            height, width, channel = self.frame.shape
            bytes_per_line = 3 * width
            q_image2 = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap2 = QPixmap.fromImage(q_image2)
            self.CheckInOut_f.frameLabel_2.setPixmap(pixmap2)
        except:
            print("error")
    #hiển thị avatar
    def displayFrame3(self):
        try:
            height, width, channel = self.frame2.shape
            bytes_per_line = 3 * width
            q_image3 = QImage(self.frame2.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap3 = QPixmap.fromImage(q_image3)
            pixmap3 = pixmap3.scaled(201, 201)
            self.CheckInOut_f.frameLabel.setPixmap(pixmap3)
        except:
            print("error")
    #cập nhật ảnh liên tục sau 1/60s để kết quả là 1 video
    def setTimer2(self):
        self.timer.timeout.connect(self.displayFrame2)
        self.timer.start(16)

        #HIỂN THỊ THÔNG TIN SINH VIÊN
    #hàm hiển thị hình ảnh
    def displayInfo(self):
        #thuật toán nhận dạng cho biết học sinh và id của học sinh
        self.student.id = daoTest.get_id()

        #truy cập vào cơ sở dữ liệu lấy ra thông tin của học sinh có id tương ứng
        list = daoTest.select_userInfo(student=self.student)
        #hiển thị thông tin học sinh
        self.CheckInOut_f.nameLabel.setText(str(list[1]))
        self.CheckInOut_f.classLabel.setText(str(list[2]))

        ##truy cập vào cơ sở dữ liệu lấy ra ảnh của học sinh có id tương ứng
        self.frame2 = daoTest.select_userAvatar(student=self.student)
        self.displayFrame3()
        
    #Ở MÀN HÌNH ADD STUDENT 1

    #hàm xóa dữ liệu ở các dòng 
    def clearLine(self):
        self.AddStudent1_f.nameLine.setText("")
        self.AddStudent1_f.facultyLine.setText("")
        self.AddStudent1_f.classLine.setText("")

    #Ở MÀN HÌNH ADD STUDENT 2
    #hàm hiển thị camera
    def displayFrame4(self):
        try:
            height, width, channel = self.frame.shape
            bytes_per_line = 3 * width
            q_image4 = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap4 = QPixmap.fromImage(q_image4)
            self.AddStudent2_f.frameLabel.setPixmap(pixmap4)
        except:
            print("error")
    def setTimer3(self):
        self.timer.timeout.connect(self.displayFrame4)
        self.timer.start(16)

    #Ở MÀN HÌNH ADD STUDENT 3
        #chụp ảnh
    #hàm lấy 1 frame
    def captureVideo(self):
        self.timer.stop()
        self.frame2 = self.frame
        self.widget.setCurrentIndex(4)
        self.displayFrame5()
        self.displayInfo2()
    #hàm hiển thị hình ảnh
    def displayFrame5(self):
        try:
            height, width, channel = self.frame2.shape
            bytes_per_line = 3 * width
            q_image5 = QImage(self.frame2.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap5 = QPixmap.fromImage(q_image5)
            pixmap5 = pixmap5.scaled(541, 381)
            self.AddStudent3_f.frameLabel.setPixmap(pixmap5)
        except:
            print("error")
    
    def displayInfo2(self):
        name = self.AddStudent1_f.nameLine.text()
        classes = self.AddStudent1_f.classLine.text()
        faculty = self.AddStudent1_f.facultyLine.text()

        self.AddStudent3_f.nameLabel.setText(name)
        self.AddStudent3_f.facultyLabel.setText(faculty)
        self.AddStudent3_f.classLabel.setText(classes)

    #Ở MÀN HÌNH HIỂN THỊ NHIỆT ĐỘ, ĐỘ ẨM
    def setTemperature(self):
        self.Temperature_f.setPlot()
        self.widget.show()

    def setTimer_Temperature(self):
        self.temperature_timer.timeout.connect(self.setTemperature)
        self.temperature_timer.start(1000)
        
    #HÀM CHÍNH
    #Thiết lập kích thước cửa sổ
    def setSize(self):
        self.widget.setFixedHeight(650)
        self.widget.setFixedWidth(1300)
    #Chọn cửa sổ để hiển thị
    def draw(self):
        self.widget.setCurrentIndex(0)
    #Thoát khỏi phần mềm khi xong
    def exitWin(self):
        self.app.exec()
    
        