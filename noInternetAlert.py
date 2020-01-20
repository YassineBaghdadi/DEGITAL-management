import socket

from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import os
from os import path
import sys
from index import *
from logIn import *

alert_fail,_ = loadUiType(path.join(path.dirname(__file__), "ui/noInternetAlert.ui"))


class NoInternetAlert(QWidget, alert_fail):
    def __init__(self, parent = None):
        super(NoInternetAlert, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.label.setPixmap(QtGui.QPixmap('img/err.png'))
        self.label.setScaledContents(True)

        self.report.clicked.connect(self.rep)
        self.exit_btn.clicked.connect(self.quit)
        self.label_2.mousePressEvent = self.showSecrit
        self.enter.clicked.connect(self.ss)
        self.u, self.p =str(open('ss.txt', 'r').readline()).split('.')

        self.i = 0

    def ss(self):
        if str(hashlib.md5(self.lineEdit.text().encode()).hexdigest()) == self.u and str(hashlib.md5(self.lineEdit_2.text().encode()).hexdigest()) == self.p:
            self.AS = AdminSetting()
            self.AS.show()
            self.close()
        else:
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')


    def showSecrit(self, event):
        if self.i == 0:
            self.frame.resize(300, 190)
            self.i = 1
        else:
            self.frame.resize(1, 1)
            self.i = 0


    def rep(self):
        self.splash = Splash()
        self.close()
        self.splash.show()
    def quit(self):
        self.close()
