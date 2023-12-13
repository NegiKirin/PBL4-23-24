import os
import sys
import threading
import time

import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QFileDialog
import numpy as np
from unidecode import unidecode


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from server_gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, detector=None, sender=None):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.detector = detector
        self.send = sender
        self.max_normal_window = 0

        # hide window hint
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # --- event  button
        # close window button
        self.uic.btn_close.clicked.connect(self.closeEvent)
        # restore window button
        self.uic.btn_window_restore.clicked.connect(self.Window_restore)
        # minus window
        self.uic.btn_minus.clicked.connect(lambda: self.showMinimized())
        # change page camera
        self.uic.btn_camera.clicked.connect(self.changePageCamera)
        # change page student list
        self.uic.btn_list_student.clicked.connect(self.changePageStudentList)
        # change page session list
        self.uic.btn_list_session.clicked.connect(self.changePageSessionList)
        # back page student list
        self.uic.btn_back_to_page_list_student.clicked.connect(self.changePageStudentList)
        # back page session list
        self.uic.btn_back_to_page_list_session.clicked.connect(self.changePageSessionList)

        # -- on page student list
        # search student by fullname
        self.uic.btn_search_student.clicked.connect(self.searchStudent)
        # change page add student
        self.uic.btn_add_student.clicked.connect(self.changePageAddStudent)

        # -- on page add student
        # config add student
        self.uic.btn_config_edit_student.clicked.connect(self.addStudent)
        # back page student list
        self.uic.btn_back_to_page_list_student.clicked.connect(self.changePageStudentList)
        # get path file images
        self.uic.btn_get_path_avatar.clicked.connect(self.getPathImage)

        # -- on page session list
        # search session by room_number
        self.uic.btn_search_session.clicked.connect(self.searchSession)
        # change page add session
        # todo: create page add session

        # -- on page find student to add for session
        # search student to add for session
        self.uic.btn_search_student_to_add.clicked.connect(self.searchStudentToAddForSession)

        # all thread
        self.thread = {}

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

    def changePageCamera(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_2)
        # todo: start module yolo

    def changePageStudentList(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_3)
        # todo: select students and add for student_list

    def changePageSessionList(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_5)
        # todo: select sessions and add for session_list

    def searchStudent(self):
        # get student name to search bar
        name = self.uic.ip_search_student.text()
        if name == '':
            return
        # todo select student by name

    def changePageAddStudent(self):
        # change page add student
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_4)
        self.uic.label_error_gender.setMaximumSize(QtCore.QSize(0, 16777215))
        self.uic.label_error_fullname.setMaximumSize(QtCore.QSize(0, 16777215))
        self.uic.label_error_email.setMaximumSize(QtCore.QSize(0, 16777215))
        self.uic.label_error_dateOfBirth.setMaximumSize(QtCore.QSize(0, 16777215))

    def addStudent(self):
        # get parameter
        fullname = self.uic.ip_fullname.text()
        dateOfBirth = self.uic.ip_date_of_birth.text()
        email = self.uic.ip_email.text()
        gender = self.uic.ip_gender.text()
        # check gender to only accept Nam or Nu value
        if unidecode(gender).lower() != 'nam' and unidecode(gender).lower() != 'nu':
            # show label_error_gender
            self.uic.label_error_gender.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.uic.label_error_gender.setText("Nhập sai")
        else:
            # hide label_error_gender
            self.uic.label_error_gender.setMaximumSize(QtCore.QSize(0, 16777215))
            self.uic.label_error_gender.setText('')

        if fullname == '':
            # show label_error_fullname
            self.uic.label_error_fullname.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.uic.label_error_fullname.setText("Nhập họ và tên")
        else:
            self.uic.label_error_fullname.setMaximumSize(QtCore.QSize(0, 16777215))
            self.uic.label_error_fullname.setText('')

        if email == '':
            # show label_error_fullname
            self.uic.label_error_email.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.uic.label_error_email.setText("Nhập email")
        else:
            # hide label_error_fullname
            self.uic.label_error_email.setMaximumSize(QtCore.QSize(0, 16777215))
            self.uic.label_error_email.setText('')


        # todo: add student

    def getPathImage(self):
        # filedialog
        default_path = ''
        self.path, _ = QFileDialog.getOpenFileName(None, "open file", default_path, "*.png")
        # todo: save images in folder database
        img = cv2.imread(self.path)
        qt_img = self.convert_cv_qt(img, 150, 150)
        self.uic.avatar.setPixmap(qt_img)


    def searchSession(self):
        # get student name of search bar
        name = self.uic.ip_search_session.text()
        if name == '':
            return
        # todo select session by room_number

    def searchStudentToAddForSession(self):
        # get student name of search bar
        name = self.uic.ip_search_student_to_add.text()
        if name == '':
            return
        # todo select student by name

class Capture_Video(QThread):
    signal = pyqtSignal(np.ndarray)

    def __init__(self, index, detector=None):
        self.index = index
        self.detector = detector
        print('start threading', self.index)
        super(Capture_Video, self).__init__()

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
