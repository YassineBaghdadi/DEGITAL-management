from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import os
from os import path
import sys
import time
import sqlite3


Sign_in_up_ui,_ = loadUiType(path.join(path.dirname(__file__), "index.ui"))

class Sign_in_up(QWidget, Sign_in_up_ui):
    def __init__(self, parent = None):
        super(Sign_in_up, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.width_ = 871
        self.height_ = 431

        self.home_frame.resize(self.width_, self.height_)
        self.add_person_btn.clicked.connect(self.addP)
        self.home_icon.mousePressEvent = self.showH

    def showH(self, event):
        self.home_frame.resize(self.width_, self.height_)
        self.add_person_frame.resize(1, 1)

    def addP(self):

        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(self.width_, self.height_)






def main():
    app = QtWidgets.QApplication(sys.argv)
    Sign_in_up_wn = Sign_in_up()
    Sign_in_up_wn.show()
    sys.exit(app.exec_())


if __name__ == '__main__' :
    main()