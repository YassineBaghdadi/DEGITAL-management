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
import  noInternetAlert
from noInternetAlert import *
from logIn import *
from db_m import *
from admin_settings import *

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
        self.today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))




    def is_connected(self):
        try:#todo
            con = sqlite3.connect('src/setting.db')
            cur = con.cursor()
            self.dt = cur.execute('select host, db_user, db_pass, db_name, port from admin_setting').fetchone()

            if DB_m(self.dt[0], self.dt[1], self.dt[2], self.dt[3], int(self.dt[4])):
                print('connected')
                self.logi = LogIn()
                self.logi.show()
                self.close()
            else:
                print('cant conn')
                self.err = noInternetAlert.NoInternetAlert()
                self.err.show()
                self.close()

            # TODO delay
            # if cur.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="delay";').fetchone() and cur.execute('SELECT * FROM delay;').fetchall():
            #     try:
            #
            #         last_open = cur.execute('select logins_date where id = max(id)').fetchone()
            #         if int(last_open) + cur.execute('select days from delay where id = 1').fetchone() >= datetime.toda
            #
            #     except:
            #         pass


            con.close()
        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n' + self.today + ' ' + str(e))

            self.err = noInternetAlert.NoInternetAlert()
            self.err.show()
            self.close()



    def prog(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(100, self)

    def timerEvent(self, event):
        if self.step >= 100 :
            self.timer.stop()
            self.is_connected()
            # except:
            #     err = noInternetAlert.NoInternetAlert()
            #     err.show()
            #     self.close()
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