# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'row.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(972, 63)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.row = QtWidgets.QFrame(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(6)
        self.row.setFont(font)
        self.row.setStyleSheet("QWidget:hover{\n"
"    background-color: rgb(130, 195, 195);\n"
"}")
        self.row.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.row.setFrameShadow(QtWidgets.QFrame.Raised)
        self.row.setObjectName("row")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.row)
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 5)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.index = QtWidgets.QLabel(self.row)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.index.setFont(font)
        self.index.setAlignment(QtCore.Qt.AlignCenter)
        self.index.setObjectName("index")
        self.horizontalLayout_2.addWidget(self.index)
        self.line_2 = QtWidgets.QFrame(self.row)
        self.line_2.setStyleSheet("background-color: rgb(74, 114, 118);")
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.room_number = QtWidgets.QLabel(self.row)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.room_number.setFont(font)
        self.room_number.setAlignment(QtCore.Qt.AlignCenter)
        self.room_number.setObjectName("room_number")
        self.horizontalLayout_2.addWidget(self.room_number)
        self.line_3 = QtWidgets.QFrame(self.row)
        self.line_3.setStyleSheet("background-color: rgb(74, 114, 118);")
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_2.addWidget(self.line_3)
        self.day = QtWidgets.QLabel(self.row)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.day.setFont(font)
        self.day.setAlignment(QtCore.Qt.AlignCenter)
        self.day.setObjectName("day")
        self.horizontalLayout_2.addWidget(self.day)
        self.line_4 = QtWidgets.QFrame(self.row)
        self.line_4.setStyleSheet("background-color: rgb(74, 114, 118);")
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.horizontalLayout_2.addWidget(self.line_4)
        self.start_time = QtWidgets.QLabel(self.row)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.start_time.setFont(font)
        self.start_time.setAlignment(QtCore.Qt.AlignCenter)
        self.start_time.setObjectName("start_time")
        self.horizontalLayout_2.addWidget(self.start_time)
        self.line_5 = QtWidgets.QFrame(self.row)
        self.line_5.setStyleSheet("background-color: rgb(74, 114, 118);")
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.horizontalLayout_2.addWidget(self.line_5)
        self.end_time = QtWidgets.QLabel(self.row)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.end_time.setFont(font)
        self.end_time.setAlignment(QtCore.Qt.AlignCenter)
        self.end_time.setObjectName("end_time")
        self.horizontalLayout_2.addWidget(self.end_time)
        self.verticalLayout.addWidget(self.row)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.index.setText(_translate("MainWindow", "1"))
        self.room_number.setText(_translate("MainWindow", "C102"))
        self.day.setText(_translate("MainWindow", "20/12/2023"))
        self.start_time.setText(_translate("MainWindow", "10:30"))
        self.end_time.setText(_translate("MainWindow", "11:30"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
