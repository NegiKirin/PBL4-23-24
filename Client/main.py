import sys
import threading
import time
import cv2
import Interface.gui as gui

if __name__ == "__main__":

    #   HIỂN THỊ MÀN HÌNH
    gui = gui.GUI()
    gui.draw()
    gui.setSize()


    # HIỂN THỊ HISTORY
    history = [["Tín", "23-12-9 8:30", "23-12-9 9:30"],
               ["Hiếu", "23-12-9 8:30", "23-12-9 9:30"],
               ["Phúc", "23-12-9 8:30", "23-12-9 9:30"]
               ]
    gui.setH(history)
    gui.setHistory()
    # gui.setTimer_History()
    # HIỂN THỊ LIST
    list = [["Tín", "21TCLC_KHDL2", "CNTT"],
            ["Hiếu", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"],
            ["Phúc", "21TCLC_KHDL2", "CNTT"]
            ]
    gui.setL(list)
    gui.setList()

    gui.exitWin()

