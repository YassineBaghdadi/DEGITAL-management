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
import hashlib

from main import *
from db_m import *



logIn_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/logIn.ui"))

class LogIn(QWidget, logIn_ui):
    def __init__(self, parent = None):
        super(LogIn, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)

        self.admin_user = 'f986a7ef9eb3fa8b6ce6a46d5302adc3'#MOY
        self.admin_pass = '9d775cbd1a1a75b7b9ac184d0d12489e'#MOY1
        self.cnx.setEnabled(False)

        self.host_db ='localhost'
        self.port_db = 3306
        self.user_db = 'root'
        self.passwrd_db = 'root'

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QImage("img/pack.png")))
        self.setPalette(palette)
        self.label.setPixmap(QtGui.QPixmap('img/login.png'))
        self.label.setScaledContents(True)
        self.setWindowTitle('Bienvenue')

        self.username.setPlaceholderText('User Name')
        self.passwrd.setPlaceholderText('Password')

        self.cnx.clicked.connect(self.cnnx)
        self.username.textChanged.connect(self.typing)
        self.passwrd.textChanged.connect(self.typing1)
        self.createTables()
        self.refresh()
        self.db_ = DB_m()

    def cnnx(self):
        if str(hashlib.md5(self.username.text().encode()).hexdigest()) == self.admin_user and str(hashlib.md5(self.passwrd.text().encode()).hexdigest()) == self.admin_pass:  # todo our settings
            print(self.admin_user)
            print(str(hashlib.md5(self.username.text().encode()).hexdigest()))
            print('##########################')
            print(self.admin_pass)
            print(str(hashlib.md5(self.passwrd.text().encode()).hexdigest()))

            self.main = Main()
            self.main.show()
            self.close()
        else:
            print(self.admin_user)
            print(str(hashlib.md5(self.username.text().encode()).hexdigest()))
            print('##########################')
            print(self.admin_pass)
            print(str(hashlib.md5(self.passwrd.text().encode()).hexdigest()))
            self.passwrd.setText('')
            self.username.setText('')

    def typing(self):
        if len(self.username.text()) > 2:
            self.username.setStyleSheet('border : 2px solid white')
        else:
            self.username.setStyleSheet('border : 2px solid red')

        if len(self.username.text()) > 2 and len(self.passwrd.text()) > 2:
            self.cnx.setEnabled(True)
        else:
            self.cnx.setEnabled(False)



    def typing1(self):
        if len(self.passwrd.text()) > 2:
            self.passwrd.setStyleSheet('border : 2px solid white')
            self.cnx.setEnabled(True)
        else:
            self.passwrd.setStyleSheet('border : 2px solid red')
            self.cnx.setEnabled(False)

        if len(self.username.text()) > 2 and len(self.passwrd.text()) > 2:
            self.cnx.setEnabled(True)
        else:
            self.cnx.setEnabled(False)

    def createTables(self):
        pass
    def refresh(self):
        pass



def main():
    app = QtWidgets.QApplication(sys.argv)
    Sign_in_up_wn = LogIn()
    Sign_in_up_wn.show()
    sys.exit(app.exec_())
if __name__ == '__main__' :
    main()