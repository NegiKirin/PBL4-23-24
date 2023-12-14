import os
import sys
import threading
import time

import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem
import numpy as np


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from update_gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, detector=None, sender=None):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.detector = detector
        self.send = sender
        self.max_normal_window = 0
        self.sessions = []

        # hide window hint
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # infor bar hide
        self.hide_infor()

        # --- event  button
        # close window button
        self.uic.btn_close.clicked.connect(self.closeEvent)
        # restore window button
        self.uic.btn_window_restore.clicked.connect(self.Window_restore)
        # minus window
        self.uic.btn_minus.clicked.connect(lambda: self.showMinimized())
        # config room number
        self.uic.btn_config_room_number.clicked.connect(self.config_room_number)
        # select item in list widget
        self.uic.listWidget.itemDoubleClicked.connect(self.select_items)

        self.thread = {}

    def start_capture_video(self):
        self.thread[1] = capture_video(index=1, detector=self.detector)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_webcam)

    def show_webcam(self, cv_img):
        # Update the image_label with a new opencv image
        qt_img = self.convert_cv_qt(cv_img, 800, 600)
        self.uic.label_webcam.setPixmap(qt_img)

    def hide_infor(self):
        self.uic.frame_infor.setMaximumSize(QtCore.QSize(0, 16777215))
        self.uic.frame_infor.setMinimumSize(QtCore.QSize(0, 0))

    def show_infor(self, user, image):
        self.uic.frame_infor.setMaximumSize(QtCore.QSize(300, 16777215))
        self.uic.frame_infor.setMinimumSize(QtCore.QSize(250, 0))
        self.uic.label_name.setText(user.fullname)
        qt_img = self.convert_cv_qt(image, 140, 140)
        self.uic.label_avatar.setPixmap(qt_img)
        # set action for btns
        self.user = user
        self.uic.btn_confirm.clicked.connect(self.confirm_infor)
        self.uic.btn_cancel.clicked.connect(self.cancel_infor)

    def confirm_infor(self):
        cccd = self.uic.input_cccd.text()
        if cccd == self.user.cccd:
            print('OK')
            # todo: update for student
            self.send.sendSessionIdAndUserId(self.sessions.id, self.user.id)

            t = threading.Thread(target=self.detector.face_detection, args=[self])
            t.setDaemon = True
            t.start()
            self.uic.input_cccd.setText('')
            self.hide_infor()
        else:
            t = threading.Thread(target=self.detector.face_detection, args=[self])
            t.setDaemon = True
            t.start()
            self.uic.input_cccd.setText('')
            self.hide_infor()
        t = threading.Thread(target=self.detector.face_detection, args=[self])
        t.setDaemon = True
        t.start()
        self.uic.input_cccd.setText('')
        self.hide_infor()

    def cancel_infor(self):
        t = threading.Thread(target=self.detector.face_detection, args=[self])
        t.setDaemon = True
        t.start()
        self.hide_infor()

    def convert_cv_qt(self, cv_img, width, height):
        # Convert from an opencv image to QPixmap
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format.Format_RGB888)
        p = convert_to_Qt_format.scaled(width, height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def stop_capture_video(self):
        self.thread[1].stop()

    # function close window
    def closeEvent(self, event):
        self.close()

    #function restore window
    def Window_restore(self):
        if self.max_normal_window == 0:
            self.showMaximized()
            self.max_normal_window = 1
        elif self.max_normal_window == 1:
            self.showNormal()
            self.max_normal_window = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()

    def mouseMoveEvent(self, event):
        width = self.uic.frame.width()
        height = self.uic.frame.height()
        if self.startPos.x() <= width and self.startPos.y() <= height \
            and self.isFullScreen() == False:
            self.move(self.pos() + (event.pos() - self.startPos))

    def config_room_number(self):
        room_number = self.uic.room_number.text()
        print(room_number)
        # === ID SESSION ===
        self.sessions = self.send.sendRoomNumber(room_number)
        if self.sessions == []:
            return
        if self.sessions != []:
            # set row in list widget
            self.addItemForSession(self.results)

            self.uic.stackedWidget.setCurrentWidget(self.uic.page_2)

    def addItemForSession(self, sessions):
        i = 0
        print(sessions)
        # add row
        for session in sessions:
            newItem = QListWidgetItem()
            newItem.setSizeHint(QSize(0, 35))

            centralwidget = QtWidgets.QWidget()
            centralwidget.setStyleSheet("")
            centralwidget.setObjectName("centralwidget")
            verticalLayout = QtWidgets.QVBoxLayout(centralwidget)
            verticalLayout.setContentsMargins(0, 0, 0, 0)
            verticalLayout.setSpacing(0)
            verticalLayout.setObjectName("verticalLayout")
            row = QtWidgets.QFrame(centralwidget)
            font = QtGui.QFont()
            font.setPointSize(6)
            row.setFont(font)
            row.setStyleSheet("QWidget:hover{\n"
                                   "    background-color: rgb(130, 195, 195);\n"
                                   "}")
            row.setFrameShape(QtWidgets.QFrame.StyledPanel)
            row.setFrameShadow(QtWidgets.QFrame.Raised)
            row.setObjectName("row")
            horizontalLayout_2 = QtWidgets.QHBoxLayout(row)
            horizontalLayout_2.setContentsMargins(0, 5, 0, 5)
            horizontalLayout_2.setSpacing(0)
            horizontalLayout_2.setObjectName("horizontalLayout_2")
            index = QtWidgets.QLabel(row)
            font = QtGui.QFont()
            font.setPointSize(10)
            index.setFont(font)
            index.setAlignment(QtCore.Qt.AlignCenter)
            index.setObjectName("index")
            horizontalLayout_2.addWidget(index)
            i+=1
            index.setText(str(i))
            line_2 = QtWidgets.QFrame(row)
            line_2.setStyleSheet("background-color: rgb(74, 114, 118);")
            line_2.setFrameShape(QtWidgets.QFrame.VLine)
            line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_2.setObjectName("line_2")
            horizontalLayout_2.addWidget(line_2)
            room_number = QtWidgets.QLabel(row)
            font = QtGui.QFont()
            font.setPointSize(10)
            room_number.setFont(font)
            room_number.setAlignment(QtCore.Qt.AlignCenter)
            room_number.setObjectName("room_number")
            horizontalLayout_2.addWidget(room_number)
            room_number.setText(session.room.roomNumber)
            line_3 = QtWidgets.QFrame(row)
            line_3.setStyleSheet("background-color: rgb(74, 114, 118);")
            line_3.setFrameShape(QtWidgets.QFrame.VLine)
            line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_3.setObjectName("line_3")
            horizontalLayout_2.addWidget(line_3)
            day = QtWidgets.QLabel(row)
            font = QtGui.QFont()
            font.setPointSize(10)
            day.setFont(font)
            day.setAlignment(QtCore.Qt.AlignCenter)
            day.setObjectName("day")
            horizontalLayout_2.addWidget(day)
            d = str(session.day).split('-')
            d.reverse()
            d = '-'.join(d)
            day.setText(d)
            line_4 = QtWidgets.QFrame(row)
            line_4.setStyleSheet("background-color: rgb(74, 114, 118);")
            line_4.setFrameShape(QtWidgets.QFrame.VLine)
            line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_4.setObjectName("line_4")
            horizontalLayout_2.addWidget(line_4)
            start_time = QtWidgets.QLabel(row)
            font = QtGui.QFont()
            font.setPointSize(10)
            start_time.setFont(font)
            start_time.setAlignment(QtCore.Qt.AlignCenter)
            start_time.setObjectName("start_time")
            horizontalLayout_2.addWidget(start_time)
            start_time.setText(str(session.startTime))
            line_5 = QtWidgets.QFrame(row)
            line_5.setStyleSheet("background-color: rgb(74, 114, 118);")
            line_5.setFrameShape(QtWidgets.QFrame.VLine)
            line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
            line_5.setObjectName("line_5")
            horizontalLayout_2.addWidget(line_5)
            end_time = QtWidgets.QLabel(row)
            font = QtGui.QFont()
            font.setPointSize(10)
            end_time.setFont(font)
            end_time.setAlignment(QtCore.Qt.AlignCenter)
            end_time.setObjectName("end_time")
            horizontalLayout_2.addWidget(end_time)
            end_time.setText(str(session.endTime))
            verticalLayout.addWidget(row)

            self.uic.listWidget.addItem(newItem)
            self.uic.listWidget.setItemWidget(newItem, centralwidget)

    def select_items(self, item):
        row = self.uic.listWidget.row(item)
        # send session id return image data
        t = threading.Thread(target=self.send.sendIdSession, args=[self.sessions[row].id, self])
        t.setDaemon = True
        t.start()

        self.uic.stackedWidget.setCurrentWidget(self.uic.page_4)
        # self.send.sendIdSession(self.results[row].id)

    def progress(self, percen):
        self.uic.progressBar.setValue(percen)
        if percen == 100:
            self.uic.stackedWidget.setCurrentWidget(self.uic.page)
            # self.detector.

    def startDetector(self, images, users):
        self.detector.load_images(images, users, self)

class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)

    def __init__(self, index, detector=None):
        self.index = index
        self.detector = detector
        print('start threading', self.index)
        super(capture_video, self).__init__()

    # def run(self):
    #     cap = cv2.VideoCapture(0)
    #     while True:
    #         ret, frame = cap.read()
    #         if ret:
    #             self.signal.emit(frame)

    def run(self):
        try:
            if self.detector.img == None:
                time.sleep(1)
                self.run()
            while True:
                self.signal.emit(self.detector.img)
        except Exception as e:
            print(str(e))

    def stop(self):
        print('stop threading', self.index)
        self.terminate()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    # main_win.start_capture_video()
    sys.exit(app.exec())
