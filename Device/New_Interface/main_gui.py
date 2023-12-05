import os
import sys
import threading
import time

import cv2
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
import numpy as np
current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory)
from new_gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, detector=None):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)
        self.detector = detector

        self.max_normal_window = 0

        # hide window hint
        self.setWindowFlag(Qt.FramelessWindowHint)

        # infor bar hide
        self.hide_infor()

        # --- event button
        # close window button
        self.uic.btn_close.clicked.connect(self.closeEvent)
        # restore window button
        self.uic.btn_window_restore.clicked.connect(self.Window_restore)
        # minus window
        self.uic.btn_minus.clicked.connect(lambda: self.showMinimized())

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

    def show_infor(self, infor, image):
        self.uic.frame_infor.setMaximumSize(QtCore.QSize(300, 16777215))
        self.uic.frame_infor.setMinimumSize(QtCore.QSize(250, 0))
        self.uic.label_name.setText(str(infor[5]))
        qt_img = self.convert_cv_qt(image, 140, 140)
        self.uic.label_avatar.setPixmap(qt_img)
        # set action for btns
        self.infor = infor
        self.uic.btn_confirm.clicked.connect(self.confirm_infor)
        self.uic.btn_cancel.clicked.connect(self.cancel_infor)

    def confirm_infor(self):
        cccd = self.uic.input_cccd.text()
        if cccd == self.infor[1]:
            print('OK')
            self.detector.dao.HistoryDAO().insert(int(self.infor[0]), 1)
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
