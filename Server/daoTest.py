import cv2
import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__)) + '\\'
sys.path.append(current_directory+"..\\")

def select_userInfo(student):
    if student.id ==1:
        list= ["1","Tín", "21TCLC_KHDL", "CNTT"]
        return list
def select_userAvatar(student):
    if student.id ==1:
        image = cv2.imread(current_directory+'logo.jpg')
        # print(current_directory+'tui.png')
        # print(image)
        return image
def get_id():
    return 1
