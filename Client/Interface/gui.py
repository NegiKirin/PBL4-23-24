from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer, QRect
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.uic import loadUi
import sys, os
import numpy as np
import math

import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from Pageable import PageRequest
# sys.path.append(current_directory+"..\\")
# import daoTest



# cửa sổ 
class Monitor_w(QMainWindow):
    def __init__(self, widget=None, gui=None, receiver=None):
        super(Monitor_w, self).__init__()
        loadUi(current_directory+'Monitor.ui',self)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
        self.gui = gui
        self.receiver = receiver
    #xử lý chuyển cửa sổ
    def loadMenu2(self):
        self.receiver.cm = -3
        self.gui.setHistory()
        self.gui.monitor_timer.stop()           
        self.gui.timer.stop()
        self.gui.widget.setCurrentIndex(1)
    def loadMenu3(self):
        self.receiver.cm = -4
        self.gui.monitor_timer.stop()           
        self.gui.timer.stop()
        self.gui.setList()
        self.widget.setCurrentIndex(2)
    def loadMenu4(self):
        self.receiver.cm = -5
        self.gui.setTimer_Temperature()     
        self.gui.monitor_timer.stop()
        self.gui.timer.stop()
        self.widget.setCurrentIndex(3)
    def loadMenu5(self):
        sys.exit()
    #truyền dữ liệu vào để view
    def LoadingData(self,t,o):
        self.temperature.setText(str(t))
        self.wet.setText(str(o))

class List_w(QMainWindow):
    def __init__(self, widget=None, gui=None, receiver=None):
        super(List_w, self).__init__()
        uic=loadUi(current_directory+'List.ui',self)
        self.menu1.clicked.connect(self.loadMenu1)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
        self.gui = gui
        self.receiver = receiver
        self.searchInfo.setStyleSheet("border-radius: 10px; padding: 8px;")
        #Ở màn hình List, thiết lập chiều rộng của các cột trong bảng
        self.tableList.setColumnWidth(0,100)
        self.tableList.setColumnWidth(1,246)
        self.tableList.setColumnWidth(2,246)
        self.tableList.setColumnWidth(3,246)
        #làm mới
        self.refreshButton.clicked.connect(self.refresh)
        # phân trang
        self.pageable= PageRequest(page=1, maxPageItem=10)
        self.pageable.searcher.searchName = "name"
        self.length=0
        self.previousButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)
        self.button1.clicked.connect(self.number1)
        self.button2.clicked.connect(self.number2)
        self.button3.clicked.connect(self.number3)
        self.button4.clicked.connect(self.number4)
        self.button5.clicked.connect(self.number5)

        #Tìm kiếm khi nhấn nút enter
        self.searchInfo.returnPressed.connect(self.search)

        self.tmp = True

    def setPage(self, totalItem):
        self.numberOfPage = totalItem / 10
        maxPage = math.ceil(self.numberOfPage)
        if self.numberOfPage <= 5:
            self.a1 = 1
            self.a2 = 2
            self.a3 = 3
            self.a4 = 4
            self.a5 = 5
        else:
            self.a1 = 1
            self.a2 = 2
            self.a3 = 3
            self.a4 = 4
            self.a5 = maxPage
    #xử lý chuyển cửa sổ
    def loadMenu1(self):
        self.receiver.cm = -2
        self.receiver.start()
        self.gui.setTimer_Monitor()
        self.gui.setTimer()
        self.widget.setCurrentIndex(0)
    def loadMenu2(self):
        self.receiver.cm = -3
        self.receiver.start()
        self.widget.setCurrentIndex(1)
        self.gui.setHistory()
    def loadMenu3(self):
        self.receiver.cm = -4
        self.receiver.start()
        self.widget.setCurrentIndex(2)
        self.gui.setList()
    def loadMenu4(self):
        self.receiver.cm = -5
        self.receiver.start()
        self.gui.setTimer_Temperature()
        self.widget.setCurrentIndex(3)
    def loadMenu5(self):
        sys.exit()

    #làm mới
    def refresh(self):
        self.pageable.searcher.search = None
        # client send: currentPage, server return List
        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue
        # insert into table
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True


    #tìm kiếm
    def search(self):
        self.pageable.searcher.search = self.searchInfo.text()
        # client send: currentPage, server return List
        # list = daoTest.select_user(pageable=self.pageable)
        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue
        # insert into table
        self.insert_table(list=self.tmp[:-1])
        self.tmp = True

    #xử lý phân trang của view
    def insert_table(self, list):
        row = -1
        self.tableList.clearContents()
        for eachList in list:
            row += 1
            self.tableList.setItem(row, 0, QtWidgets.QTableWidgetItem(eachList[0]))
            self.tableList.setItem(row, 1, QtWidgets.QTableWidgetItem(eachList[1]))
            self.tableList.setItem(row, 2, QtWidgets.QTableWidgetItem(eachList[2]))
            self.tableList.setItem(row, 3, QtWidgets.QTableWidgetItem(eachList[3]))
        self.tableList.verticalHeader().setVisible(False)
        self.pagigation()

    def update_index_page(self):
        # func
        self.button1.setText(str(self.a1))
        self.button2.setText(str(self.a2))
        self.button3.setText(str(self.a3))
        self.button4.setText(str(self.a4))
        self.button5.setText(str(self.a5))
    
    # phân trang
    def pagigation(self):
        self.numberOfPage = self.tmp[-1] / 10
        print(self.numberOfPage)
        if self.numberOfPage <=1:
            self.button1.setVisible(True)
            self.button1.move(670, 510)
            self.button2.setVisible(False)
            self.button3.setVisible(False)
            self.button4.setVisible(False)
            self.button5.setVisible(False)
            self.previousButton.setVisible(False)
            self.nextButton.setVisible(False)
            self.label.setVisible(False)
        elif self.numberOfPage <=2:
            self.button1.setVisible(True)
            self.button1.move(620, 510)
            self.button2.setVisible(True)
            self.button2.move(720, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(520, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(820, 510)
            self.button3.setVisible(False)
            self.button4.setVisible(False)
            self.button5.setVisible(False)
            self.label.setVisible(False)
        elif self.numberOfPage <=3:
            print("ham3")
            self.button1.setVisible(True)
            self.button1.move(570, 510)
            self.button2.setVisible(True)
            self.button2.move(670, 510)
            self.button3.setVisible(True)
            self.button3.move(770, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(470, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(870, 510)
            self.button4.setVisible(False)
            self.button5.setVisible(False)
            self.label.setVisible(False)
        elif self.numberOfPage <=4:
            print("ham4")
            self.button1.setVisible(True)
            self.button1.move(520, 510)
            self.button2.setVisible(True)
            self.button2.move(620, 510)
            self.button3.setVisible(True)
            self.button3.move(720, 510)
            self.button4.setVisible(True)
            self.button4.move(820, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(420, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(920, 510)
            self.button5.setVisible(False)
            self.label.setVisible(False)
        elif self.numberOfPage <=5:
            self.button1.setVisible(True)
            self.button1.move(470, 510)
            self.button2.setVisible(True)
            self.button2.move(570, 510)
            self.button3.setVisible(True)
            self.button3.move(670, 510)
            self.button4.setVisible(True)
            self.button4.move(770, 510)
            self.button5.setVisible(True)
            self.button5.move(870, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(370, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(970, 510)
            self.label.setVisible(False)
        else: 
            self.button1.setVisible(True)
            self.button1.move(470, 510)
            self.button2.setVisible(True)
            self.button2.move(570, 510)
            self.button3.setVisible(True)
            self.button3.move(670, 510)
            self.button4.setVisible(False)
            self.label.setVisible(True)
            self.button5.setVisible(True)
            self.button5.move(870, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(370, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(970, 510)

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
        if self.pageable.page != 1:
            self.pageable.page -=1
            if int(self.button1.text())>=2 :
                self.decreaseValueButton()
                self.update_index_page()
            # client send: currentPage, server return List
            # list = daoTest.select_user(pageable=self.pageable)
            self.receiver.start()
            self.receiver.pageable = self.pageable
            while self.tmp == True: continue
            # insert into table
            row = -1
            print(len(self.tmp[:-1]))
            if len(self.tmp[:-1]) ==0:
                return
            self.insert_table(list=self.tmp[:-1])
            self.update_index_page()
            self.tmp = True
        else:
            return

    def next(self):
        self.pageable.page+=1
        print(self.pageable.page)
        if self.pageable.page>=5:          
            self.increaseValueButton()
            self.update_index_page()
        self.tableList.clearContents()
        # client send: currentPage, server return List
        # list = daoTest.select_user(pageable=self.pageable)
        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue
        print(self.tmp[:-1])
        # insert into table
        row = -1
        print(len(self.tmp[:-1]))
        if len(self.tmp[:-1]) ==0:
            return
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True

    def number1(self):
        self.pageable.page = int(self.button1.text())
        i= self.pageable.page

        # client send: currentPage, server return List
        # list = daoTest.select_user(pageable=self.pageable)
        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp[-1] / 10
        maxPage= math.ceil(self.numberOfPage)
        if maxPage<=5:
            self.a1=1           
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        # else:
        #     if i==1:
        #         self.a1=1           
        #         self.a2=2
        #         self.a3=3
        #         self.a4=4
        #         self.a5=maxPage
        #     if i==maxPage-4:
        #         #hiện tất cả
        #         self.a1=maxPage-4           
        #         self.a2=maxPage-3
        #         self.a3=maxPage-2
        #         self.a4=maxPage-1
        #         self.a5=maxPage
        #         self.button4.setVisible(True)
        #         self.label.setVisible(False)
        #     else: 
        #         self.a1= i-1
        #         self.a2= i
        #         self.a3= i+1
        #         self.a4= i+2
        #         self.a5= maxPage

        # insert into table
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True

    def number2(self):
        self.pageable.page = int(self.button2.text())
        i= self.pageable.page

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp[-1] / 10
        maxPage= math.ceil(self.numberOfPage)
        if self.numberOfPage <=5:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        # else:
        #     if i == maxPage-3:
        #         #hiện tất cả
        #         self.a1=maxPage-4           
        #         self.a2=maxPage-3
        #         self.a3=maxPage-2
        #         self.a4=maxPage-1
        #         self.a5=maxPage
        #         self.button4.setVisible(True)
        #         self.label.setVisible(False)
        #     elif i==2:
        #         self.a1=1
        #         self.a2=2
        #         self.a3=3
        #         self.a4=4
        #         self.a5=maxPage
        #     else:
        #         self.a1= i-1
        #         self.a2= i
        #         self.a3= i+1
        #         self.a4= i+2
        #         self.a5= maxPage
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True

    def number3(self):
        self.pageable.page = int(self.button3.text())
        i= self.pageable.page

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp[-1] / 10
        maxPage= math.ceil(self.numberOfPage)
        if self.numberOfPage <=5:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        # else:
        #     if i == maxPage-2:
        #         #hiện tất cả
        #         self.a1=maxPage-4           
        #         self.a2=maxPage-3
        #         self.a3=maxPage-2
        #         self.a4=maxPage-1
        #         self.a5=maxPage
        #         self.button4.setVisible(True)
        #         self.label.setVisible(False)
        #     elif i>=3:
        #         self.a1= i-1
        #         self.a2= i
        #         self.a3= i+1
        #         self.a4= i+2
        #         self.a5= maxPage
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True

    def number4(self):
        self.pageable.page = int(self.button4.text())
        i= self.pageable.page

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp-1 / 10
        maxPage= math.ceil(self.numberOfPage)
        if self.numberOfPage <=5:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        # else:
        #     if i==maxPage-1:
        #         #hiện tất cả
        #         self.a1=maxPage-4           
        #         self.a2=maxPage-3
        #         self.a3=maxPage-2
        #         self.a4=maxPage-1
        #         self.a5=maxPage
        #         self.button4.setVisible(True)
        #         self.label.setVisible(False)
        #     elif i>=3:
        #         self.a1= i-1
        #         self.a2= i
        #         self.a3= i+1
        #         self.a4= i+2
        #         self.a5= maxPage
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True

    def number5(self):
        self.pageable.page = int(self.button5.text())
        i= self.pageable.page

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp / 10
        maxPage= math.ceil(self.numberOfPage)
        #hiện tất cả
        self.a1=maxPage-4           
        self.a2=maxPage-3
        self.a3=maxPage-2
        self.a4=maxPage-1
        self.a5=maxPage
        self.button4.setVisible(True)
        self.label.setVisible(False)
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True
    #hàm truyền dữ liệu vào để view list
    def LoadingData(self):
        self.tableList.setRowCount(10)
        # list = daoTest.request()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue
        self.insert_table(list=self.tmp[:-1])
        self.setPage(totalItem=self.tmp[-1])
        self.pagigation()
        self.update_index_page()
        self.tmp = True

class History_w(QMainWindow):
    def __init__(self, widget=None, gui=None, receiver=None):
        super(History_w, self).__init__()
        uic=loadUi(current_directory+'History.ui',self)
        self.menu1.clicked.connect(self.loadMenu1)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu4.clicked.connect(self.loadMenu4)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
        self.gui = gui
        self.receiver = receiver
        self.searchInfo.setStyleSheet("border-radius: 10px; padding: 8px;")
        # Ở màn hình History, định dạng kích thước cột trong table
        self.tableHistory.setColumnWidth(0,100)
        self.tableHistory.setColumnWidth(1,246)
        self.tableHistory.setColumnWidth(2,246)
        self.tableHistory.setColumnWidth(3,246)
        #làm mới
        self.refreshButton.clicked.connect(self.refresh)
        # phân trang
        self.pageable = PageRequest(page=1, maxPageItem=10)
        self.pageable.searcher.searchName = "name"
        self.length = 0
        self.previousButton.clicked.connect(self.previous)
        self.nextButton.clicked.connect(self.next)
        self.button1.clicked.connect(self.number1)
        self.button2.clicked.connect(self.number2)
        self.button3.clicked.connect(self.number3)
        self.button4.clicked.connect(self.number4)
        self.button5.clicked.connect(self.number5)

        #Tìm kiếm khi nhấn nút enter
        self.searchInfo.returnPressed.connect(self.search)

        self.tmp = True

    def setPage(self, totalItem):
        #khởi tạo giá trị của các button số trang
        self.numberOfPage = totalItem / 10
        maxPage = math.ceil(self.numberOfPage)
        if self.numberOfPage <= 5:
            self.a1 = 1
            self.a2 = 2
            self.a3 = 3
            self.a4 = 4
            self.a5 = 5
        else:
            self.a1 = 1
            self.a2 = 2
            self.a3 = 3
            self.a4 = 4
            self.a5 = maxPage

    #xử lý chuyển cửa sổ
    def loadMenu2(self):
        self.receiver.cm = -3
        self.receiver.start()
        self.gui.setHistory()
        self.widget.setCurrentIndex(1)
    def loadMenu3(self):
        self.receiver.cm = -4
        self.receiver.start()
        self.gui.setList()
        self.widget.setCurrentIndex(2)
    def loadMenu1(self):
        self.receiver.cm = -2
        self.receiver.start()
        self.gui.setTimer_Monitor()
        self.gui.setTimer()
        self.widget.setCurrentIndex(0)
    def loadMenu4(self):
        self.receiver.cm = -5
        self.receiver.start()
        self.gui.setTimer_Temperature()
        self.widget.setCurrentIndex(3)
    def loadMenu5(self):
        sys.exit()

    #làm mới
    def refresh(self):
        self.pageable.searcher.search = None
        # client send: currentPage, server return List
        # list = daoTest.request()
        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue
        # insert into table
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True

    #tìm kiếm
    def search(self):
        self.pageable.searcher.search= self.searchInfo.text()
        # client send: currentPage, server return List
        # list = daoTest.select_user(pageable=self.pageable)
        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue
        # insert into table
        self.insert_table(list=self.tmp[:-1])
        self.tmp = True


    #xử lý phân trang của view
    def insert_table(self, list):
        row = -1
        self.tableHistory.clearContents()
        for eachHistory in list:
            row += 1
            self.tableHistory.setItem(row, 0, QtWidgets.QTableWidgetItem(eachHistory[0]))
            self.tableHistory.setItem(row, 1, QtWidgets.QTableWidgetItem(eachHistory[1]))
            self.tableHistory.setItem(row, 2, QtWidgets.QTableWidgetItem(eachHistory[2]))
            self.tableHistory.setItem(row, 3, QtWidgets.QTableWidgetItem(eachHistory[3]))
        self.tableHistory.verticalHeader().setVisible(False)
        self.pagigation()

    # phân trang
    def pagigation(self):
        self.numberOfPage = self.tmp[-1] / 10
        print(self.numberOfPage)
        if self.numberOfPage <=1:
            self.button1.setVisible(True)
            self.button1.move(670, 510)
            self.button2.setVisible(False)
            self.button3.setVisible(False)
            self.button4.setVisible(False)
            self.button5.setVisible(False)
            self.previousButton.setVisible(False)
            self.nextButton.setVisible(False)
            self.label.setVisible(False)
        elif self.numberOfPage <=2:
            self.button1.setVisible(True)
            self.button1.move(620, 510)
            self.button2.setVisible(True)
            self.button2.move(720, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(520, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(820, 510)
            self.button3.setVisible(False)
            self.button4.setVisible(False)
            self.button5.setVisible(False)
            self.label.setVisible(False)
        elif self.numberOfPage <=3:
            print("ham3")
            self.button1.setVisible(True)
            self.button1.move(570, 510)
            self.button2.setVisible(True)
            self.button2.move(670, 510)
            self.button3.setVisible(True)
            self.button3.move(770, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(470, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(870, 510)
            self.button4.setVisible(False)
            self.button5.setVisible(False)
            self.label.setVisible(False)
        elif self.numberOfPage <=4:
            print("ham4")
            self.button1.setVisible(True)
            self.button1.move(520, 510)
            self.button2.setVisible(True)
            self.button2.move(620, 510)
            self.button3.setVisible(True)
            self.button3.move(720, 510)
            self.button4.setVisible(True)
            self.button4.move(820, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(420, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(920, 510)
            self.button5.setVisible(False)
            self.label.setVisible(False)
        elif self.numberOfPage <=5:
            self.button1.setVisible(True)
            self.button1.move(470, 510)
            self.button2.setVisible(True)
            self.button2.move(570, 510)
            self.button3.setVisible(True)
            self.button3.move(670, 510)
            self.button4.setVisible(True)
            self.button4.move(770, 510)
            self.button5.setVisible(True)
            self.button5.move(870, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(370, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(970, 510)
            self.label.setVisible(False)
        else: 
            self.button1.setVisible(True)
            self.button1.move(470, 510)
            self.button2.setVisible(True)
            self.button2.move(570, 510)
            self.button3.setVisible(True)
            self.button3.move(670, 510)
            self.button4.setVisible(False)
            self.label.setVisible(True)
            self.button5.setVisible(True)
            self.button5.move(870, 510)
            self.previousButton.setVisible(True)
            self.previousButton.move(370, 510)
            self.nextButton.setVisible(True)
            self.nextButton.move(970, 510)
    def update_index_page(self):
        # func
        self.button1.setText(str(self.a1))
        self.button2.setText(str(self.a2))
        self.button3.setText(str(self.a3))
        self.button4.setText(str(self.a4))
        self.button5.setText(str(self.a5))
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
        if self.pageable.page != 1:
            self.pageable.page-=1
            print(self.pageable.page)
            if int(self.button1.text())>=2:       
                self.decreaseValueButton()
                self.update_index_page()
            self.tableHistory.clearContents()
            # client send: currentPage, server return List
            # list = daoTest.select_user(pageable=self.pageable)
            self.receiver.start()
            self.receiver.pageable = self.pageable
            while self.tmp == True: continue
            # insert into table
            row = -1
            print(len(self.tmp[:-1]))
            if len(self.tmp[:-1]) ==0:
                return
            self.insert_table(list=self.tmp[:-1])
            self.tmp = True
        else:
            return 
        
    def next(self):
        self.pageable.page+=1
        print(self.pageable.page)
        if self.pageable.page>=5:          
            self.increaseValueButton()
            self.update_index_page()
        self.tableHistory.clearContents()
        # client send: currentPage, server return List
        # list = daoTest.select_user(pageable=self.pageable)
        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue
        # insert into table
        row = -1
        print(len(self.tmp[:-1]))
        if len(self.tmp[:-1]) == 0:
            return
        self.insert_table(list=self.tmp[:-1])
        self.tmp = True

    def number1(self):
        self.pageable.page = int(self.button1.text())
        i= self.pageable.page

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp[-1] / 10
        maxPage= math.ceil(self.numberOfPage)
        if self.numberOfPage<=5:
            self.a1=1           
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        # else:
        #     if i==1:
        #         self.a1=1           
        #         self.a2=2
        #         self.a3=3
        #         self.a4=4
        #         self.a5=maxPage
        #     if i==maxPage-4:
        #         #hiện tất cả
        #         self.a1=maxPage-4           
        #         self.a2=maxPage-3
        #         self.a3=maxPage-2
        #         self.a4=maxPage-1
        #         self.a5=maxPage
        #         self.button4.setVisible(True)
        #         self.label.setVisible(False)
        #     else: 
        #         self.a1= i-1
        #         self.a2= i
        #         self.a3= i+1
        #         self.a4= i+2
        #         self.a5= maxPage
        # client send: currentPage, server return List
        # list = daoTest.select_user(pageable=self.pageable)

        # insert into table
        self.insert_table(self.tmp[:-1])
        self.update_index_page()
        self.tmp = True

    def number2(self):
        self.pageable.page = int(self.button2.text())
        i= self.pageable.page

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp[-1] / 10
        maxPage= math.ceil(self.numberOfPage)
        if self.numberOfPage <=5:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        # else:
        #     if i == maxPage-3:
        #         #hiện tất cả
        #         self.a1=maxPage-4           
        #         self.a2=maxPage-3
        #         self.a3=maxPage-2
        #         self.a4=maxPage-1
        #         self.a5=maxPage
        #         self.button4.setVisible(True)
        #         self.label.setVisible(False)
        #     elif i==2:
        #         self.a1=1
        #         self.a2=2
        #         self.a3=3
        #         self.a4=4
        #         self.a5=maxPage
        #     else:
        #         self.a1= i-1
        #         self.a2= i
        #         self.a3= i+1
        #         self.a4= i+2
        #         self.a5= maxPage
        # list = daoTest.select_user(pageable=self.pageable)
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True
    def number3(self):
        self.pageable.page = int(self.button3.text())
        i= self.pageable.page

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp[-1] / 10
        maxPage= math.ceil(self.numberOfPage)
        if self.numberOfPage <=5:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        # else:
        #     if i == maxPage-2:
        #         #hiện tất cả
        #         self.a1=maxPage-4           
        #         self.a2=maxPage-3
        #         self.a3=maxPage-2
        #         self.a4=maxPage-1
        #         self.a5=maxPage
        #         self.button4.setVisible(True)
        #         self.label.setVisible(False)
        #     elif i>=3:
        #         self.a1= i-1
        #         self.a2= i
        #         self.a3= i+1
        #         self.a4= i+2
        #         self.a5= maxPage
        # list = daoTest.select_user(pageable=self.pageable)
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True
    def number4(self):
        self.pageable.page = int(self.button4.text())
        i= self.pageable.page

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp[-1] / 10
        maxPage= math.ceil(self.numberOfPage)
        if self.numberOfPage <=5:
            self.a1=1
            self.a2=2
            self.a3=3
            self.a4=4
            self.a5=5
        # else:
        #     if i==maxPage-1:
        #         #hiện tất cả
        #         self.a1=maxPage-4           
        #         self.a2=maxPage-3
        #         self.a3=maxPage-2
        #         self.a4=maxPage-1
        #         self.a5=maxPage
        #         self.button4.setVisible(True)
        #         self.label.setVisible(False)
        #     elif i>=3:
        #         self.a1= i-1
        #         self.a2= i
        #         self.a3= i+1
        #         self.a4= i+2
        #         self.a5= maxPage
        # list = daoTest.select_user(pageable=self.pageable)
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True
    def number5(self):
        self.pageable.page = int(self.button5.text())-1
        i= self.pageable.page +1

        self.receiver.start()
        self.receiver.pageable = self.pageable
        while self.tmp == True: continue

        self.numberOfPage = self.tmp[-1] / 10
        maxPage= math.ceil(self.numberOfPage)
        #hiện tất cả
        self.a1=maxPage-4           
        self.a2=maxPage-3
        self.a3=maxPage-2
        self.a4=maxPage-1
        self.a5=maxPage
        self.button4.setVisible(True)
        self.label.setVisible(False)
        # list = daoTest.select_user(pageable=self.pageable)
        self.insert_table(list=self.tmp[:-1])
        self.update_index_page()
        self.tmp = True

   #hàm truyền dữ liệu vào để view history
    def LoadingData(self):
        self.tableHistory.setRowCount(10)

        self.receiver.pageable = self.pageable
        while self.tmp == True: continue
        self.insert_table(list=self.tmp[:-1])
        self.setPage(totalItem=self.tmp[-1])

        self.pagigation()
        self.update_index_page()
        self.tmp = True
        

class Temperature_w(QMainWindow):
    def __init__(self, widget=None, gui=None, receiver=None):
        super(Temperature_w, self).__init__()
        uic=loadUi(current_directory+'temperature.ui',self)
        self.menu2.clicked.connect(self.loadMenu2)
        self.menu3.clicked.connect(self.loadMenu3)
        self.menu1.clicked.connect(self.loadMenu1)
        self.menu5.clicked.connect(self.loadMenu5)
        self.widget = widget
        self.gui = gui
        self.receiver = receiver
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
        self.temperature.axes.axis([Xmin, Xmax, Ymin, 40])
        self.humidity.axes.axis([Xmin, Xmax, Ymin, Ymax])
        # self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

    #xử lý chuyển cửa sổ
    def loadMenu2(self):
        # self.temperature.axes.clear()
        # self.temperature.axes.axis([self.X_temperature[0], self.X_temperature[-1], 0, 100])
        #
        # self.X_temperature = [self.X_temperature[-1]]
        # self.Y_temperature = [self.Y_temperature[-1]]

        self.receiver.cm = -3

        self.gui.temperature_timer.stop()
        self.gui.setHistory()
        self.widget.setCurrentIndex(1)
    def loadMenu3(self):
        # self.temperature.axes.clear()
        # self.temperature.axes.axis([self.X_temperature[0], self.X_temperature[-1], 0, 100])
        #
        # self.X = [self.X_temperature[-1]]
        # self.Y = [self.Y_temperature[-1]]

        self.receiver.cm = -4

        self.gui.temperature_timer.stop()
        self.gui.setList()
        self.widget.setCurrentIndex(2)
    def loadMenu1(self):

        # self.temperature.axes.clear()
        # self.temperature.axes.axis([self.X_temperature[0], self.X_temperature[-1], 0, 100])
        #
        # self.X_temperature = [self.X_temperature[-1]]
        # self.Y_temperature = [self.Y_temperature[-1]]

        self.receiver.cm = -2

        self.gui.setTimer_Monitor()
        self.gui.setTimer()
        self.gui.temperature_timer.stop()
        self.widget.setCurrentIndex(0)
    def loadMenu5(self):
        sys.exit()

    def plotTemperature(self):
        # print("print diagram Temperature")
        if (len(self.X_temperature) <= 20):
            self.X_temperature.append(self.X_temperature[-1] + 1)
            self.Y_temperature.append(self.gui.t)
        else:
            print("else Temperature")
            self.X_temperature.pop(0)
            self.X_temperature.append(self.X_temperature[-1] + 1)
            self.Y_temperature.pop(0)
            self.Y_temperature.append(self.gui.t)
            self.temperature.axes.clear()
            self.temperature.axes.axis([self.X_temperature[0], self.X_temperature[-1], 0, 40])
        self.temperature.axes.plot(self.X_temperature, self.Y_temperature, color='red')
        self.temperature.draw()
    def plotHumidity(self):
        # print("print diagram Humidity")
        if (len(self.X_humidity) <= 20):
            self.X_humidity.append(self.X_humidity[-1] + 1)
            self.Y_humidity.append(self.gui.o)
        else:
            print("else Humidity")
            self.X_humidity.pop(0)
            self.X_humidity.append(self.X_humidity[-1] + 1)
            self.Y_humidity.pop(0)
            self.Y_humidity.append(self.gui.o)
            self.humidity.axes.clear()
            self.humidity.axes.axis([self.X_humidity[0], self.X_humidity[-1], 0, 100])
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
    #HÀM KHỞI TẠO
    def __init__(self, receiver=None):
        self.receiver = receiver
        # new một cửa số và widget
        self.app = QApplication(sys.argv)
        self.widget =QtWidgets.QStackedWidget()

        #Lưu 4 hàm cửa sổ widget trên về biến
        self.Monitor_f = Monitor_w(widget=self.widget, gui=self, receiver=self.receiver)
        self.History_f = History_w(widget=self.widget, gui=self, receiver=self.receiver)
        self.List_f = List_w(widget=self.widget, gui=self, receiver=self.receiver)
        self.Temperature_f = Temperature_w(widget=self.widget, gui=self, receiver=self.receiver)
        #add widget vào
        self.widget.addWidget(self.Monitor_f)      #index0
        self.widget.addWidget(self.History_f)      #index1
        self.widget.addWidget(self.List_f)         #index2
        self.widget.addWidget(self.Temperature_f)  #index3

        #tạo một widget Timer để cập nhật dữ liệu
        self.monitor_timer = QTimer()
        self.timer = QTimer()
        # self.history_timer = QTimer()
        # self.list_timer = QTimer()
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
        self.t = tt
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
            q_image = QImage(self.frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(q_image)
            self.imagine.setPixmap(pixmap)
        except Exception as e:
            pass
            # print(e)
            # print("error")
    #
    def setHistory(self):
        self.History_f.LoadingData()
        self.widget.show()
    #
    def setList(self):
        self.List_f.LoadingData()
        self.widget.show()

    #
    def setTemperature(self):
        self.Temperature_f.setPlot()
        self.widget.show()

    #CÁC HÀM THIẾT LẬP THỜI GIAN ĐỂ CẬP NHẬT LẠI DỮ LIỆU
    #ở màn hình Monitor
    def setTimer_Monitor(self):
        self.monitor_timer.timeout.connect(self.setMonitor)
        self.monitor_timer.start(2000) #cập nhật giao diện
    def setTimer(self):
        self.timer.timeout.connect(self.updateCapture)
        self.timer.start(16)
    #ở màn hình history
    # def setTimer_History(self):
    #     self.history_timer.timeout.connect(self.setHistory)
    #     self.history_timer.start(100) #cập nhật giao diện
    # #ở màn hình list
    # def setTimer_List(self):
    #     self.list_timer.timeout.connect(self.setList)
    #     self.list_timer.start(2000) #cập nhật giao diện 5 giây
    #ở màn hình Temperture
    def setTimer_Temperature(self):
        self.temperature_timer.timeout.connect(self.setTemperature)
        self.temperature_timer.start(1000)

    #HÀM CHÍNH
    def draw(self):
        #chọn widget khi chương trình khởi chạy
        self.widget.setCurrentIndex(0)
        self.setSize()
        self.setTimer()
        self.setTimer_Monitor()
        self.exitWin()
    def exitWin(self):
        # thoát khi xong việc
        self.app.exec()


