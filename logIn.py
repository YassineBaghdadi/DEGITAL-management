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
import noInternetAlert



logIn_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/logIn.ui"))

class LogIn(QWidget, logIn_ui):
    def __init__(self, parent = None):
        super(LogIn, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.admin_user = 'f986a7ef9eb3fa8b6ce6a46d5302adc3'#MOY
        self.admin_pass = '9d775cbd1a1a75b7b9ac184d0d12489e'#MOY1
        self.cnx.setEnabled(False)
        try:
            self.dblocal = sqlite3.connect('src/setting.db')
            self.curs = self.dblocal.cursor()
            self.host_db = self.curs.execute('select host from admin_setting where id = 1').fetchone()[0]
            self.user_db = self.curs.execute('select db_user from admin_setting where id = 1').fetchone()[0]
            self.passwrd_db = self.curs.execute('select db_pass from admin_setting where id = 1').fetchone()[0]
            self.port_db = self.curs.execute('select port from admin_setting where id = 1').fetchone()[0]
            self.DBname = self.curs.execute('select db_name from admin_setting where id = 1').fetchone()[0]
        except:
            err = noInternetAlert.NoInternetAlert()
            err.show()

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QImage("img/pack.png")))
        self.setPalette(palette)
        self.label.setPixmap(QtGui.QPixmap('img/login.png'))
        self.label.setScaledContents(True)
        self.setWindowTitle('Bienvenue')

        self.username_in.setPlaceholderText('User Name')
        self.passwrd_in.setPlaceholderText('Password')

        self.cnx.clicked.connect(self.cnnx)
        self.username_in.textChanged.connect(self.typing)
        self.passwrd_in.textChanged.connect(self.typing1)
        self.passwrd_in.returnPressed.connect(self.cnnx)
        self.createTables()
        self.refresh()
        self.db_ = DB_m(self.host_db, self.user_db, self.passwrd_db, self.DBname) #todo get FROM setting from admin_+setting
        # try:
        #     self.db_ = DB_m(self.host_db, self.user_db, self.passwrd_db, self.DBname) #todo get FROM setting from admin_+setting
        # except:
        #     err = noInternetAlert.NoInternetAlert()
        #     err.show()

    def cnnx(self):
        if str(hashlib.md5(self.username_in.text().encode()).hexdigest()) == self.admin_user and str(hashlib.md5(self.passwrd_in.text().encode()).hexdigest()) == self.admin_pass:  # todo our settings
            # print(self.admin_user)
            # print(str(hashlib.md5(self.username_in.text().encode()).hexdigest()))
            # print('##########################')
            # print(self.admin_pass)
            # print(str(hashlib.md5(self.passwrd_in.text().encode()).hexdigest()))
            #todo go to suder admin settings
            # self.main = Main()
            # self.main.show()
            # self.close()
            pass
        else:
            if self.db_.logIn( self.username_in.text(), self.passwrd_in.text()) == 'admin':
                #the admin
                print('profile : ', self.db_.logIn(self.username_in.text(), self.passwrd_in.text()))
                main_ = Main('admin')
                main_.show()
                self.close()

            elif self.db_.logIn( self.username_in.text(), self.passwrd_in.text()) == 'ass':
                #the assistent
                print('profile : ', self.db_.logIn(self.username_in.text(), self.passwrd_in.text()))
                main_ = Main('ass')
                main_.show()
                self.close()

            elif self.db_.logIn( self.username_in.text(), self.passwrd_in.text()) == 'wrong':
                #some input wrong
                self.passwrd_in.setText('')
                self.username_in.setText('')
                print('something was wrong', self.db_.logIn( self.username_in.text(), self.passwrd_in.text()))

            elif self.db_.logIn(self.username_in.text(), self.passwrd_in.text()) == 'error':
                #system error
                self.passwrd_in.setText('')
                self.username_in.setText('')
                print('sys error', self.db_.logIn( self.username_in.text(), self.passwrd_in.text()))




    def typing(self):
        if len(self.username_in.text()) > 2:
            self.username_in.setStyleSheet('border : 2px solid white')
        else:
            self.username_in.setStyleSheet('border : 2px solid red')

        if len(self.username_in.text()) > 2 and len(self.passwrd_in.text()) > 2:
            self.cnx.setEnabled(True)
        else:
            self.cnx.setEnabled(False)



    def typing1(self):
        if len(self.passwrd_in.text()) > 2:
            self.passwrd_in.setStyleSheet('border : 2px solid white')
            self.cnx.setEnabled(True)
        else:
            self.passwrd_in.setStyleSheet('border : 2px solid red')
            self.cnx.setEnabled(False)

        if len(self.username_in.text()) > 2 and len(self.passwrd_in.text()) > 2:
            self.cnx.setEnabled(True)
        else:
            self.cnx.setEnabled(False)

    def createTables(self):
        pass
    def refresh(self):
        pass


