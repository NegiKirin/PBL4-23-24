# -*- coding: utf-8 -*-
import os

# Form implementation generated from reading ui file 'row_inListStudent.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QEvent

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'


class row_inListStudent(object):
    def setupUi(self):
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
        icon.addPixmap(QtGui.QPixmap(current_directory + "images/icons/icons8-delete-30.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete_student.setIcon(icon)
        self.btn_delete_student.setIconSize(QtCore.QSize(16, 16))
        self.btn_delete_student.setObjectName("btn_delete_student")
        self.horizontalLayout_2.addWidget(self.btn_delete_student)
        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addWidget(self.frame)
        self.centralwidget.installEventFilter(self)

    def eventForListStudent(self, obj, event):
        if event.type() == QEvent.Leave:
            print('leave')

        elif event.type() == QEvent.Enter:
            print('enter')



