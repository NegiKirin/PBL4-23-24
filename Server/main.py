import sys

from PyQt5.QtWidgets import QApplication

import Server
from New_Interface import main_gui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = main_gui.MainWindow()
    main_win.show()
    sys.exit(app.exec())
    # Server.server()