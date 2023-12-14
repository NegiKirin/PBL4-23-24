import sys

from PyQt5.QtWidgets import QApplication

from View.main_gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    # main_win.start_capture_video()
    sys.exit(app.exec())
