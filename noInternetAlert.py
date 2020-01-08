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

    def rep(self):
        self.splash = Splash()
        self.close()
        self.splash.show()
    def quit(self):
        self.close()