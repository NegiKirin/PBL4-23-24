import os
import shutil
import sys
import threading
import time
import traceback
from PIL import Image

import cv2
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QSize, QDate, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QFileDialog
import numpy as np
from unidecode import unidecode

# from Server.Model.DAO.SessionDAO import SessionDAO


current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from server_gui import Ui_MainWindow
from Dialog import Ui_Dialog
from Model.DAO.UserDAO import UserDAO
from Model.DAO.SessionDAO import SessionDAO


class MainWindow(QMainWindow):
    def __init__(self, detector=None, sender=None):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.detector = detector
        self.send = sender
        self.max_normal_window = 0
        self.path_image = ''
        self.selected_student_id = None
        self.selected_session_id = None
        self.list_student = []
        self.list_session = []
        self.list_item_in_list_student = []
        self.list_item_in_list_session = []
        self.list_item_in_list_student_to_add = []
        self.path_data = "../database/"

        # hide window hint
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Created Dialog
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.window)
        self.window.setWindowFlag(Qt.FramelessWindowHint)
        self.window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # - event button for Dialog
        self.ui.btn_minus.clicked.connect(lambda: self.window.showMinimized())
        self.ui.btn_close.clicked.connect(lambda: self.window.close() and
                                          self.ChangePageStudentInSession(self.selected_session_id))
        # selected item in student list
        self.ui.listWidget.itemDoubleClicked.connect(self.select_student_in_student_list_to_add)


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
        # back page session list
        self.uic.btn_back_to_page_list_session.clicked.connect(self.changePageSessionList)

        # -- on page student list
        # search student by fullname
        self.uic.btn_search_student.clicked.connect(self.searchStudent)
        # change page add student
        self.uic.btn_add_student.clicked.connect(self.changePageAddStudent)
        # selected item in student list
        self.uic.student_list.itemDoubleClicked.connect(self.select_student_in_student_list)
        # selection change
        self.uic.student_list.itemSelectionChanged.connect(self.selection_changed_student_list)

        # -- on page add student
        # config add student
        # self.uic.btn_config_edit_student.clicked.connect(self.editStudent)
        # back page student list
        self.uic.btn_back_to_page_list_student.clicked.connect(self.changePageStudentList)
        # get path file images
        self.uic.btn_get_path_avatar.clicked.connect(self.getPathImage)
        # selection change
        self.uic.student_list_to_add.itemSelectionChanged.connect(self.selection_changed_student_list_to_add)

        # -- on page session list
        # search session by room_number
        self.uic.btn_search_session.clicked.connect(self.searchSession)
        # change page add session
        # todo: create page add session
        # selected item in student list
        self.uic.session_list.itemDoubleClicked.connect(self.select_session_in_session_list)
        # selection change
        self.uic.session_list.itemSelectionChanged.connect(self.selection_changed_session_list)

        # -- on page find student to add for session
        # search student to add for session
        self.uic.btn_search_student_to_add.clicked.connect(self.searchStudentToAddForSession)
        # add student for session
        self.uic.btn_add_student_for_session.clicked.connect(self.openDialogAddStudentToSession)

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

    def clearList(self):
        self.list_item_in_list_student.clear()
        self.list_item_in_list_session.clear()

    def changePageCamera(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_2)
        # todo: start module yolo

    def changePageStudentList(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_3)
        self.uic.student_list.clear()
        self.path_image = ''
        # todo: select students and add for student_list
        self.list_student = UserDAO().getAll()
        self.clearList()
        self.addItemForStudent(self.list_student)

    def addItemForStudent(self, users):
        for user in users:
            newItem = QListWidgetItem()
            newItem.setSizeHint(QSize(0, 45))

            self.centralwidget = QtWidgets.QWidget()
            self.centralwidget.setStyleSheet("opacity: 0;")
            self.centralwidget.setObjectName("centralwidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setSpacing(0)
            self.verticalLayout.setObjectName("verticalLayout")
            self.frame = QtWidgets.QFrame(self.centralwidget)
            font = QtGui.QFont()
            font.setPointSize(9)
            self.frame.setFont(font)
            self.frame.setStyleSheet("")
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame.setObjectName("frame")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.id = QtWidgets.QLabel(self.frame)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.id.setFont(font)
            self.id.setAlignment(QtCore.Qt.AlignCenter)
            self.id.setObjectName("id")
            self.id.setText(str(user.id))
            self.horizontalLayout.addWidget(self.id)
            self.line = QtWidgets.QFrame(self.frame)
            self.line.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line.setFrameShape(QtWidgets.QFrame.VLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setObjectName("line")
            self.horizontalLayout.addWidget(self.line)
            self.fullname = QtWidgets.QLabel(self.frame)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.fullname.setFont(font)
            self.fullname.setAlignment(QtCore.Qt.AlignCenter)
            self.fullname.setObjectName("fullname")
            self.fullname.setText(user.fullname)
            self.horizontalLayout.addWidget(self.fullname)
            self.line_2 = QtWidgets.QFrame(self.frame)
            self.line_2.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_2.setObjectName("line_2")
            self.horizontalLayout.addWidget(self.line_2)
            self.dataOfBirth = QtWidgets.QLabel(self.frame)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.dataOfBirth.setFont(font)
            self.dataOfBirth.setAlignment(QtCore.Qt.AlignCenter)
            self.dataOfBirth.setObjectName("dataOfBirth")
            d = str(user.dateOfBirth).split('-')
            d.reverse()
            d = '/'.join(d)
            self.dataOfBirth.setText(d)
            self.horizontalLayout.addWidget(self.dataOfBirth)
            self.line_3 = QtWidgets.QFrame(self.frame)
            self.line_3.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_3.setObjectName("line_3")
            self.horizontalLayout.addWidget(self.line_3)
            self.email = QtWidgets.QLabel(self.frame)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.email.setFont(font)
            self.email.setAlignment(QtCore.Qt.AlignCenter)
            self.email.setObjectName("email")
            self.email.setText(user.email)
            self.horizontalLayout.addWidget(self.email)
            self.line_4 = QtWidgets.QFrame(self.frame)
            self.line_4.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_4.setObjectName("line_4")
            self.horizontalLayout.addWidget(self.line_4)
            self.gender = QtWidgets.QLabel(self.frame)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.gender.setFont(font)
            self.gender.setAlignment(QtCore.Qt.AlignCenter)
            self.gender.setObjectName("gender")
            self.gender.setText(user.gender)
            self.horizontalLayout.addWidget(self.gender)
            self.line_5 = QtWidgets.QFrame(self.frame)
            self.line_5.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_5.setObjectName("line_5")
            self.horizontalLayout.addWidget(self.line_5)
            self.cccd = QtWidgets.QLabel(self.frame)
            font = QtGui.QFont()
            font.setPointSize(8)
            self.cccd.setFont(font)
            self.cccd.setAlignment(QtCore.Qt.AlignCenter)
            self.cccd.setObjectName("cccd")
            self.cccd.setText(user.cccd)
            self.horizontalLayout.addWidget(self.cccd)
            self.line_6 = QtWidgets.QFrame(self.frame)
            self.line_6.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_6.setObjectName("line_6")
            self.horizontalLayout.addWidget(self.line_6)
            self.widget = QtWidgets.QWidget(self.frame)
            self.widget.setObjectName("widget")
            self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
            self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_2.setObjectName("horizontalLayout_2")
            self.btn_delete_student = QtWidgets.QPushButton(self.widget)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.btn_delete_student.sizePolicy().hasHeightForWidth())
            self.btn_delete_student.setSizePolicy(sizePolicy)
            self.btn_delete_student.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.btn_delete_student.setStyleSheet("QPushButton{\n"
                                                  "border: none;\n"
                                                  "border-radius:5px;\n"
                                                  "}\n"
                                                  "QPushButton:hover{\n"
                                                  "background-color: rgb(255, 71, 71);\n"
                                                  "border-radius:5px;\n"
                                                  "}\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color:rgb(190, 32, 32);\n"
                                                  "}")
            self.btn_delete_student.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(current_directory + "images/icons/icons8-delete-30.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            self.btn_delete_student.setIcon(icon)
            self.btn_delete_student.setIconSize(QtCore.QSize(16, 16))
            self.btn_delete_student.setObjectName("btn_delete_student")
            self.horizontalLayout_2.addWidget(self.btn_delete_student)
            self.horizontalLayout.addWidget(self.widget)
            self.verticalLayout.addWidget(self.frame)

            self.btn_delete_student.hide()
            self.centralwidget.installEventFilter(self)
            self.btn_delete_student.clicked.connect(self.delete_student)

            self.id.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.fullname.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.dataOfBirth.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.email.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.cccd.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.gender.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.centralwidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.frame.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.btn_delete_student.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            self.list_item_in_list_student.append((self.centralwidget, self.btn_delete_student, newItem, user))

            self.uic.student_list.addItem(newItem)
            self.uic.student_list.setItemWidget(newItem, self.centralwidget)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Leave:
            for i in self.list_item_in_list_student:
                i[1].hide()
            for i in self.list_item_in_list_session:
                i[1].hide()

        elif event.type() == QEvent.Enter:
            pointer_to_widget = obj
            for list_item in self.list_item_in_list_student:
                if list_item[0] == pointer_to_widget:
                    list_item[1].show()
                    self.selected_student_id = list_item[-1].id
            for list_item in self.list_item_in_list_session:
                if list_item[0] == pointer_to_widget:
                    list_item[1].show()
            # for list_item in self.list_item_in_list_student_to_add:
            #     if list_item[0] == pointer_to_widget:
            #         self.selected_student_id = list_item[-1].id
            #         print(self.selected_student_id)
        return super(MainWindow, self).eventFilter(obj, event)

    def delete_student(self):
        item = None
        pointer_to_widget = self.sender()
        for list_item in self.list_item_in_list_student:
            if list_item[1] == pointer_to_widget:
                item = list_item[2]
                UserDAO().deleteById(list_item[-1].id)
                try:
                    shutil.rmtree(self.path_data + str(list_item[-1].id))
                except Exception as e:
                    print(e)

        row = self.uic.student_list.row(item)
        self.uic.student_list.takeItem(row)
        self.list_item_in_list_student.pop(row)

    def setPageEditUser(self, user):
        self.hide_label_error_in_adding_student()
        self.uic.btn_get_path_avatar.hide()
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_4)
        # print(user)
        # set info current
        self.uic.ip_fullname.setText(user.fullname)
        self.uic.ip_date_of_birth.setDate(user.dateOfBirth)
        self.uic.ip_email.setText(user.email)
        self.uic.ip_gender.setText(user.gender)
        self.uic.ip_cccd.setText(user.cccd)
        folder = self.path_data + str(user.id)
        file = os.listdir(self.path_data + str(user.id))[0]
        path = os.path.join(folder, file)
        img = cv2.imread(path)
        qt_img = self.convert_cv_qt(img, 150, 150)
        self.uic.avatar.setPixmap(qt_img)
        self.uic.btn_config_edit_student.clicked.connect(self.editStudent)

    def select_student_in_student_list(self, item):
        row = self.uic.student_list.row(item)
        self.setPageEditUser(self.list_student[row])

    def selection_changed_student_list(self):
        item = self.uic.student_list.currentItem()
        row = self.uic.student_list.row(item)
        self.selected_student_id = self.list_student[row].id
        # print(type(self.selected_student_id))

    def changePageSessionList(self):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_5)
        self.uic.session_list.clear()
        # todo: select sessions and add for session_list
        self.list_session = SessionDAO().getAll()
        self.clearList()
        self.addItemForSession(self.list_session)

    def addItemForSession(self, sessions):
        for session in sessions:
            newItem = QListWidgetItem()
            newItem.setSizeHint(QSize(0, 45))

            self.centralwidget = QtWidgets.QWidget()
            self.centralwidget.setObjectName("centralwidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setSpacing(0)
            self.verticalLayout.setObjectName("verticalLayout")
            self.frame = QtWidgets.QFrame(self.centralwidget)
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame.setObjectName("frame")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.room_number = QtWidgets.QLabel(self.frame)
            self.room_number.setAlignment(QtCore.Qt.AlignCenter)
            self.room_number.setObjectName("room_number")
            self.room_number.setText(session.room.roomNumber)
            self.horizontalLayout.addWidget(self.room_number)
            self.line = QtWidgets.QFrame(self.frame)
            self.line.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line.setFrameShape(QtWidgets.QFrame.VLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setObjectName("line")
            self.horizontalLayout.addWidget(self.line)
            self.day = QtWidgets.QLabel(self.frame)
            self.day.setAlignment(QtCore.Qt.AlignCenter)
            self.day.setObjectName("day")
            d = str(session.day).split('-')
            d.reverse()
            d = '/'.join(d)
            self.day.setText(d)
            self.horizontalLayout.addWidget(self.day)
            self.line_2 = QtWidgets.QFrame(self.frame)
            self.line_2.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_2.setObjectName("line_2")
            self.horizontalLayout.addWidget(self.line_2)
            self.start_time = QtWidgets.QLabel(self.frame)
            self.start_time.setAlignment(QtCore.Qt.AlignCenter)
            self.start_time.setObjectName("start_time")
            time = str(session.startTime).split(':')
            time = ':'.join(time[0:-1])
            self.start_time.setText(time)
            self.horizontalLayout.addWidget(self.start_time)
            self.line_3 = QtWidgets.QFrame(self.frame)
            self.line_3.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_3.setObjectName("line_3")
            self.horizontalLayout.addWidget(self.line_3)
            self.end_time = QtWidgets.QLabel(self.frame)
            self.end_time.setAlignment(QtCore.Qt.AlignCenter)
            self.end_time.setObjectName("end_time")
            time = str(session.endTime).split(':')
            time = ':'.join(time[0:-1])
            self.end_time.setText(time)
            self.horizontalLayout.addWidget(self.end_time)
            self.line_4 = QtWidgets.QFrame(self.frame)
            self.line_4.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_4.setObjectName("line_4")
            self.horizontalLayout.addWidget(self.line_4)
            self.widget = QtWidgets.QWidget(self.frame)
            self.widget.setObjectName("widget")
            self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
            self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout_2.setSpacing(0)
            self.horizontalLayout_2.setObjectName("horizontalLayout_2")
            self.btn_delete_session = QtWidgets.QPushButton(self.widget)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.btn_delete_session.sizePolicy().hasHeightForWidth())
            self.btn_delete_session.setSizePolicy(sizePolicy)
            self.btn_delete_session.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.btn_delete_session.setStyleSheet("QPushButton{\n"
                                                  "border: none;\n"
                                                  "border-radius:5px;\n"
                                                  "}\n"
                                                  "QPushButton:hover{\n"
                                                  "background-color: rgb(255, 71, 71);\n"
                                                  "border-radius:5px;\n"
                                                  "}\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color:rgb(190, 32, 32);\n"
                                                  "}")
            self.btn_delete_session.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(current_directory + "images/icons/icons8-delete-30.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            self.btn_delete_session.setIcon(icon)
            self.btn_delete_session.setIconSize(QtCore.QSize(16, 16))
            self.btn_delete_session.setObjectName("btn_delete_session")
            self.horizontalLayout_2.addWidget(self.btn_delete_session)
            self.horizontalLayout.addWidget(self.widget)
            self.verticalLayout.addWidget(self.frame)

            self.btn_delete_session.hide()
            self.centralwidget.installEventFilter(self)

            self.centralwidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.frame.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.room_number.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.day.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.end_time.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.start_time.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.btn_delete_session.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            self.list_item_in_list_session.append((self.centralwidget, self.btn_delete_session, newItem, session))

            self.uic.session_list.addItem(newItem)
            self.uic.session_list.setItemWidget(newItem, self.centralwidget)

    def searchStudent(self):
        # get student name to search bar
        name = self.uic.ip_search_student.text()
        if name == '':
            return
        # todo select student by name

    def changePageAddStudent(self):
        # change page add student
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_4)
        self.hide_label_error_in_adding_student()
        self.uic.btn_get_path_avatar.show()
        self.uic.avatar.clear()
        self.uic.ip_fullname.setText('')
        self.uic.ip_date_of_birth.setDate(QDate().currentDate())
        self.uic.ip_email.setText('')
        self.uic.ip_gender.setText('')
        self.uic.ip_cccd.setText('')
        self.path_image = ''
        self.uic.btn_config_edit_student.clicked.connect(self.addStudent)

    def hide_label_error_in_adding_student(self):
        self.uic.label_error_gender.setMaximumSize(QtCore.QSize(0, 16777215))
        self.uic.label_error_fullname.setMaximumSize(QtCore.QSize(0, 16777215))
        self.uic.label_error_email.setMaximumSize(QtCore.QSize(0, 16777215))
        self.uic.label_error_dateOfBirth.setMaximumSize(QtCore.QSize(0, 16777215))
        self.uic.label_error_cccd.setMaximumSize(QtCore.QSize(0, 16777215))

    def select_session_in_session_list(self, item):
        row = self.uic.session_list.row(item)
        # self.setPageEditUser(self.list_session[row])
        print(row)
        self.ChangePageStudentInSession(self.list_session[row].id)

    def selection_changed_session_list(self):
        item = self.uic.session_list.currentItem()
        row = self.uic.session_list.row(item)
        self.selected_session_id = self.list_session[row].id
        # print(type(self.selected_student_id))

    def ChangePageStudentInSession(self, sessionId):
        self.uic.stackedWidget.setCurrentWidget(self.uic.page_6)
        self.list_student = UserDAO().getListUser(sessionId)
        self.list_item_in_list_student.clear()
        self.uic.student_list_to_add.clear()
        self.addStudentForPageAddStudent(self.list_student)

    def addStudentForPageAddStudent(self, students):
        for user in students:
            newItem = QListWidgetItem()
            newItem.setSizeHint(QSize(0, 45))

            self.centralwidget = QtWidgets.QWidget()
            self.centralwidget.setObjectName("centralwidget")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setSpacing(0)
            self.verticalLayout.setObjectName("verticalLayout")
            self.frame = QtWidgets.QFrame(self.centralwidget)
            self.frame.setStyleSheet("QWidget:hover{\n"
                                     "    background-color: rgb(130, 195, 195);\n"
                                     "}\n"
                                     "\n"
                                     "QWidget{\n"
                                     "    border: none;\n"
                                     "}")
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame.setObjectName("frame")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
            self.horizontalLayout.setContentsMargins(7, 7, 7, 7)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.id = QtWidgets.QLabel(self.frame)
            self.id.setAlignment(QtCore.Qt.AlignCenter)
            self.id.setObjectName("id")
            self.id.setText(str(user.id))
            self.horizontalLayout.addWidget(self.id)
            self.line = QtWidgets.QFrame(self.frame)
            self.line.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line.setFrameShape(QtWidgets.QFrame.VLine)
            self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line.setObjectName("line")
            self.horizontalLayout.addWidget(self.line)
            self.fullname = QtWidgets.QLabel(self.frame)
            self.fullname.setAlignment(QtCore.Qt.AlignCenter)
            self.fullname.setObjectName("fullname")
            self.fullname.setText(user.fullname)
            self.horizontalLayout.addWidget(self.fullname)
            self.line_2 = QtWidgets.QFrame(self.frame)
            self.line_2.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_2.setObjectName("line_2")
            self.horizontalLayout.addWidget(self.line_2)
            self.dataOfBirth = QtWidgets.QLabel(self.frame)
            self.dataOfBirth.setAlignment(QtCore.Qt.AlignCenter)
            self.dataOfBirth.setObjectName("dataOfBirth")
            d = str(user.dateOfBirth).split('-')
            d.reverse()
            d = '/'.join(d)
            self.dataOfBirth.setText(d)
            self.horizontalLayout.addWidget(self.dataOfBirth)
            self.line_3 = QtWidgets.QFrame(self.frame)
            self.line_3.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_3.setObjectName("line_3")
            self.horizontalLayout.addWidget(self.line_3)
            self.email = QtWidgets.QLabel(self.frame)
            self.email.setAlignment(QtCore.Qt.AlignCenter)
            self.email.setObjectName("email")
            self.email.setText(user.email)
            self.horizontalLayout.addWidget(self.email)
            self.line_4 = QtWidgets.QFrame(self.frame)
            self.line_4.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_4.setObjectName("line_4")
            self.horizontalLayout.addWidget(self.line_4)
            self.gender = QtWidgets.QLabel(self.frame)
            self.gender.setAlignment(QtCore.Qt.AlignCenter)
            self.gender.setObjectName("gender")
            self.gender.setText(user.gender)
            self.horizontalLayout.addWidget(self.gender)
            self.line_5 = QtWidgets.QFrame(self.frame)
            self.line_5.setStyleSheet("background-color: rgb(74, 114, 118);")
            self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
            self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_5.setObjectName("line_5")
            self.horizontalLayout.addWidget(self.line_5)
            self.widget = QtWidgets.QWidget(self.frame)
            self.widget.setObjectName("widget")
            self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
            self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout_2.setObjectName("verticalLayout_2")
            self.btn_remove_student = QtWidgets.QPushButton(self.widget)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.btn_remove_student.sizePolicy().hasHeightForWidth())
            self.btn_remove_student.setSizePolicy(sizePolicy)
            self.btn_remove_student.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.btn_remove_student.setStyleSheet("QPushButton{\n"
                                                  "border: none;\n"
                                                  "border-radius:5px;\n"
                                                  "}\n"
                                                  "QPushButton:hover{\n"
                                                  "background-color: rgb(255, 71, 71);\n"
                                                  "border-radius:5px;\n"
                                                  "}\n"
                                                  "QPushButton:pressed {\n"
                                                  "    background-color:rgb(190, 32, 32);\n"
                                                  "}")
            self.btn_remove_student.setText("")
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(current_directory + "images/icons/icons8-delete-30.png"), QtGui.QIcon.Normal,
                           QtGui.QIcon.Off)
            self.btn_remove_student.setIcon(icon)
            self.btn_remove_student.setObjectName("btn_remove_student")
            self.verticalLayout_2.addWidget(self.btn_remove_student, 0, QtCore.Qt.AlignHCenter)
            self.horizontalLayout.addWidget(self.widget)
            self.verticalLayout.addWidget(self.frame)
            self.btn_remove_student.clicked.connect(self.removeStudent)

            self.btn_remove_student.hide()
            self.centralwidget.installEventFilter(self)

            self.centralwidget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.frame.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.id.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.fullname.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.dataOfBirth.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.email.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.gender.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.widget.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.btn_remove_student.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            self.list_item_in_list_student.append((self.centralwidget, self.btn_remove_student, newItem, user))

            self.uic.student_list_to_add.addItem(newItem)
            self.uic.student_list_to_add.setItemWidget(newItem, self.centralwidget)

    def selection_changed_student_list_to_add(self):
        item = self.uic.student_list_to_add.currentItem()
        row = self.uic.student_list_to_add.row(item)
        self.selected_student_id = self.list_student[row].id

    def removeStudent(self):
        print(self.selected_student_id)
        print(self.selected_session_id)
        UserDAO().deleteUserToSession(self.selected_student_id, self.selected_session_id)
        self.ChangePageStudentInSession(self.selected_session_id)

    def openDialogAddStudentToSession(self):
        self.window.show()
        self.ui.listWidget.clear()
        self.ui.btn_search_session.clicked.connect(self.searchStudentToAddSession)
        # self.ui.frame.installEventFilter(self)

    def addStudentForListSearchToAdd(self, students):
        for user in students:
            newItem = QListWidgetItem()
            newItem.setSizeHint(QSize(0, 100))

            self.centralwidget = QtWidgets.QWidget()
            self.centralwidget.setStyleSheet("QWidget:hover{\n"
                                             "    background-color: rgb(130, 195, 195);\n"
                                             "}\n"
                                             "\n"
                                             "QWidget{\n"
                                             "    border: none;\n"
                                             "}")
            self.centralwidget.setObjectName("centralwidget")
            self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.horizontalLayout.setSpacing(0)
            self.horizontalLayout.setObjectName("horizontalLayout")
            self.frame = QtWidgets.QFrame(self.centralwidget)
            self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame.setObjectName("frame")
            self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
            self.verticalLayout.setContentsMargins(0, 0, 0, 0)
            self.verticalLayout.setSpacing(0)
            self.verticalLayout.setObjectName("verticalLayout")
            self.frame_3 = QtWidgets.QFrame(self.frame)
            self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_3.setObjectName("frame_3")
            self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
            self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
            self.horizontalLayout_2.setObjectName("horizontalLayout_2")
            self.fullname = QtWidgets.QLabel(self.frame_3)
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.fullname.setFont(font)
            self.fullname.setStyleSheet("QLabel{\n"
                                        "    margin-left: 10px;\n"
                                        "}")
            self.fullname.setObjectName("fullname")
            self.fullname.setText(user.fullname)
            self.horizontalLayout_2.addWidget(self.fullname)
            self.verticalLayout.addWidget(self.frame_3)
            self.frame_2 = QtWidgets.QFrame(self.frame)
            self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_2.setObjectName("frame_2")
            self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_2)
            self.horizontalLayout_3.setObjectName("horizontalLayout_3")
            self.email = QtWidgets.QLabel(self.frame_2)
            self.email.setStyleSheet("QLabel{\n"
                                     "margin-left:10px;\n"
                                     "}")
            self.email.setObjectName("email")
            self.email.setText(user.email)
            self.horizontalLayout_3.addWidget(self.email)
            self.cccd = QtWidgets.QLabel(self.frame_2)
            self.cccd.setStyleSheet("QLabel{\n"
                                    "margin-left:20px;\n"
                                    "}")
            self.cccd.setObjectName("cccd")
            self.cccd.setText(user.cccd)
            self.horizontalLayout_3.addWidget(self.cccd)
            self.verticalLayout.addWidget(self.frame_2)
            self.horizontalLayout.addWidget(self.frame)

            self.frame.installEventFilter(self)

            self.frame.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.frame_2.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.frame_3.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.cccd.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.fullname.setAttribute(QtCore.Qt.WA_TranslucentBackground)
            self.email.setAttribute(QtCore.Qt.WA_TranslucentBackground)

            self.list_item_in_list_student_to_add.append((self.frame, newItem, user))

            self.ui.listWidget.addItem(newItem)
            self.ui.listWidget.setItemWidget(newItem, self.centralwidget)

    def searchStudentToAddSession(self):
        msg = self.ui.ip_search_student.text()
        msg = '%' + msg + '%'
        self.list_student = UserDAO().findByFullNameAndEmailNotInSession(msg, self.selected_session_id)
        print(self.list_student)
        self.ui.listWidget.clear()
        self.list_item_in_list_student_to_add.clear()
        self.addStudentForListSearchToAdd(self.list_student)

    def select_student_in_student_list_to_add(self, item):
        row = self.ui.listWidget.row(item)
        self.insertStudent(self.list_item_in_list_student_to_add[row][-1])

    def insertStudent(self, student):
        # print(student.id)
        # print(self.selected_session_id)
        UserDAO().insertStudentForSession(student.id, self.selected_session_id)
        self.window.close()
        self.ChangePageStudentInSession(self.selected_session_id)

    def addStudent(self):
        fullname, dateOfBirth, cccd, email, gender, allow = self.getParameterOnPageAddingStudent()
        print(fullname)
        print(dateOfBirth)
        print(email)
        print(gender)
        print(cccd)
        print(self.path_image)
        if self.path_image == '':
            return
        elif not allow:
            return
        # todo: add student
        lastUserId = UserDAO().insertStudent(fullname, dateOfBirth, cccd, email, gender)
        try:
            path = os.path.join(self.path_data, str(lastUserId))
            # path = self.path_data + str(lastUserId)
            os.makedirs(path, exist_ok=True)
            path_save_image = path + '\\' + os.path.basename(self.path_image)
            shutil.copy(self.path_image, path_save_image)
        except Exception as e:
            print(e)
        self.changePageStudentList()

    def editStudent(self):
        fullname, dateOfBirth, cccd, email, gender, allow = self.getParameterOnPageAddingStudent()
        print(fullname)
        print(dateOfBirth)
        print(email)
        print(gender)
        print(cccd)
        if not allow:
            return
        # todo: edit student
        UserDAO().updateById(self.selected_student_id, fullname, dateOfBirth, cccd, email, gender)

    def getParameterOnPageAddingStudent(self):
        # get parameter
        fullname = self.uic.ip_fullname.text()
        dateOfBirth = self.uic.ip_date_of_birth.date().toString('yyyy-MM-dd')
        email = self.uic.ip_email.text()
        gender = self.uic.ip_gender.text()
        cccd = self.uic.ip_cccd.text()
        allow = True
        # check gender to only accept Nam or Nu value
        if unidecode(gender).lower() != 'nam' and unidecode(gender).lower() != 'nu':
            # show label_error_gender
            self.uic.label_error_gender.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.uic.label_error_gender.setText("Nhập sai")
            allow = False
        else:
            # hide label_error_gender
            self.uic.label_error_gender.setMaximumSize(QtCore.QSize(0, 16777215))
            self.uic.label_error_gender.setText('')

        if fullname == '':
            # show label_error_fullname
            self.uic.label_error_fullname.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.uic.label_error_fullname.setText("Nhập họ và tên")
            allow = False
        else:
            self.uic.label_error_fullname.setMaximumSize(QtCore.QSize(0, 16777215))
            self.uic.label_error_fullname.setText('')

        if email == '':
            # show label_error_fullname
            self.uic.label_error_email.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.uic.label_error_email.setText("Nhập email")
            allow = False
        else:
            # hide label_error_fullname
            self.uic.label_error_email.setMaximumSize(QtCore.QSize(0, 16777215))
            self.uic.label_error_email.setText('')

        if cccd == '':
            # show label_error_fullname
            self.uic.label_error_cccd.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.uic.label_error_cccd.setText("Nhập CCCD")
            allow = False
        elif cccd.isdigit() == False:
            # show label_error_fullname
            self.uic.label_error_cccd.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.uic.label_error_cccd.setText("Nhập sai CCCD")
            allow = False
        else:
            # hide label_error_fullname
            self.uic.label_error_cccd.setMaximumSize(QtCore.QSize(0, 16777215))
            self.uic.label_error_cccd.setText('')
        return fullname, dateOfBirth, cccd, email, gender, allow

    def getPathImage(self):
        # filedialog
        default_path = ''
        self.path_image, _ = QFileDialog.getOpenFileName(None, "open file", default_path, "*.png")
        self.img = cv2.imread(self.path_image)
        qt_img = self.convert_cv_qt(self.img, 150, 150)
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
