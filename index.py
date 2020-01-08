import socket

from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import os
from os import path
import sys
import sqlite3

import noInternetAlert
from logIn import *
from db_m import *


splash_win_dir,_ = loadUiType(path.join(path.dirname(__file__), "ui/splash.ui"))


class Splash(QWidget, splash_win_dir):
    def __init__(self, parent = None):
        super(Splash, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowTitle('welcome back')
        self.timer = QBasicTimer()
        self.step = 0
        self.prog()
        self.localdb = sqlite3.connect('src/setting.db')
        self.curs = self.localdb.cursor()
        self.curs.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="admin_setting";')
        if self.curs.fetchone():
            print('the is exists ')
            # self.curs.execute('select host from admin_setting')
            # self.server = self.curs.fetchone()
        else:
            print('the table not found ')
            self.curs.execute('create table admin_setting (id INTEGER PRIMARY KEY AUTOINCREMENT , host text, db_user text, db_pass text, port int, db_name text)')
            self.localdb.commit()
            self.curs.execute('insert into admin_setting (host, db_user, db_pass, port, db_name) values ("localhost", "root", "root", 3306, "MOY")')
            self.localdb.commit()
            print('the table created successfully')

    def is_connected(self):
        try:
            self.curs.execute('select host, db_user, db_pass from admin_setting')
            data = self.curs.fetchone()
            self.mydb = DB_m(data[0], data[1], data[2],'')
            return True
        except:
            print(OSError)  # todo create errors on log file with time/date
            return False



    def prog(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def timerEvent(self, event):
        if self.step >= 100 :
            self.timer.stop()
            if self.is_connected():
                self.mydb.close_db()
                self.inde = LogIn()
                self.inde.show()
                self.close()


            else:
                self.noI = noInternetAlert.NoInternetAlert()
                self.close()
                self.noI.show()
            return
        self.step += 4
        self.progressBar.setValue(self.step)



def main():
    app = QtWidgets.QApplication(sys.argv)
    splash_wn = Splash()
    splash_wn.show()
    sys.exit(app.exec_())
if __name__ == '__main__' :
    main()