import pymysql
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

import noInternetAlert



_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/Settings.ui"))

class Setting(QWidget, _ui):
    def __init__(self, parent = None):
        super(Setting, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.tabIndex = 0
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.w = 441
        self.h = 321
        self.label_9.setText('1/3')
        self.setWindowTitle('Setting')
        self.today = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))


        self.right.setPixmap(QtGui.QPixmap('img/right.png'))
        self.right.setScaledContents(True)

        self.addUser.resize(self.w, self.h)
        self.addMG.resize(1, 1)
        self.addMCh.resize(1, 1)

        self.right.mousePressEvent = self.forward
        self.save.clicked.connect(self.save_user)
        self.sqliteConn = sqlite3.connect('src/setting.db')
        self.sqliteCurs = self.sqliteConn.cursor()
        self.host_db, self.user_db, self.passwrd_db, self.DBname, self.port_db = self.sqliteCurs.execute(
            'select host, db_user, db_pass, db_name, port from admin_setting').fetchone()
        self.mysqlConn = pymysql.connect(
            host=self.host_db,
            user=self.user_db,
            passwd=self.passwrd_db,
            db=self.DBname,
            port=int(self.port_db)

        )
        self.mysqlCurs = self.mysqlConn.cursor()
        self.refresh()
        self.users.itemSelectionChanged.connect(self.selectUser)
        self.treeWidget.itemSelectionChanged.connect(self.selectChM)
        self.treeWidget_2.itemSelectionChanged.connect(self.selectGM)
        self.delete_2.clicked.connect(self.deleteUser)
        self.pushButton_8.clicked.connect(self.deleteChM)
        self.pushButton_6.clicked.connect(self.deleteGM)
        self.pushButton_7.clicked.connect(self.addChM)
        self.pushButton_5.clicked.connect(self.addGM)

    def addChM(self):
        try:
            self.mysqlCurs.execute('select * from malades where name = "{}"'.format(self.lineEdit_9.text()))
            if self.mysqlCurs.fetchone():
                err = QMessageBox.warning(self, 'ERROR', 'this "malade" is already exists on the database', QMessageBox.Ok)
            elif self.lineEdit_9.text() != '':
                self.mysqlCurs.execute('insert into malades (name , type) values("{}", "chronic")'.format(self.lineEdit_9.text()))
                self.mysqlConn.commit()
                self.lineEdit_9.setText('')
                self.refresh()
        except Exception as e:
            print(e)
            if self.lineEdit_9.text() != '':
                self.mysqlCurs.execute(
                    'insert into malades (name , type) values("{}", "chronic")'.format(self.lineEdit_9.text()))
                self.mysqlConn.commit()
                self.lineEdit_9.setText('')
                self.refresh()

    def addGM(self):
        try:
            self.mysqlCurs.execute('select * from malades where name = "{}"'.format(self.lineEdit_8.text()))
            if self.mysqlCurs.fetchone():
                err = QMessageBox.warning(self, 'ERROR', 'this "malade" is already exists on the database', QMessageBox.Ok)
            elif self.lineEdit_8.text() != '':
                self.mysqlCurs.execute('insert into malades (name , type) values("{}", "ginic")'.format(self.lineEdit_8.text()))
                self.mysqlConn.commit()
                self.lineEdit_8.setText('')
                self.refresh()

        except Exception as e:
            print(e)
            if self.lineEdit_8.text() != '':
                self.mysqlCurs.execute(
                    'insert into malades (name , type) values("{}", "ginic")'.format(self.lineEdit_8.text()))
                self.mysqlConn.commit()
                self.lineEdit_8.setText('')
                self.refresh()

    def deleteUser(self):
        try:
            self.mysqlCurs.execute(''' delete from users where id = {}'''.format(self.users.selectedItems()[0].text(0)))
            self.mysqlConn.commit()
            self.refresh()
            print('deleted done')
        except Exception as e:
            print(e)
            open('src/login_logs.txt', 'a').write(
                '\n{},  err : {}'.format(self.today, e))

    def deleteChM(self):

        try:
            self.mysqlCurs.execute(''' delete from malades where id = {}'''.format(self.treeWidget.selectedItems()[0].text(0)))
            self.mysqlConn.commit()
            self.refresh()
            print('deleted done')
        except Exception as e:
            print(e)
            open('src/login_logs.txt', 'a').write(
                '\n{},  err  : {}'.format(self.today, e))

    def deleteGM(self):

        try:
            self.mysqlCurs.execute(''' delete from malades where id = {}'''.format(self.treeWidget_2.selectedItems()[0].text(0)))
            self.mysqlConn.commit()
            self.refresh()
            print('deleted done')
        except Exception as e:
            print(e)
            open('src/login_logs.txt', 'a').write(
                '\n{},  err  : {}'.format(self.today, e))

    def selectUser(self):
        try:
            self.userSelected = self.users.selectedItems()[0].text(0)
            if self.userSelected:
                self.delete_2.setEnabled(True)
                self.username.setText(self.users.selectedItems()[0].text(1))
                self.passwrd.setText(self.users.selectedItems()[0].text(2))
                self.passwrd_2.setText(self.users.selectedItems()[0].text(2))
                print(self.users.selectedItems()[0].text(0))

        except Exception as e:
            print(e)
        # if getSelected:
        #     # value = getSelected.text(0)
            # print (value)

    def selectChM(self):
        try:
            if self.treeWidget.selectedItems()[0].text(0):
                self.pushButton_8.setEnabled(True)
                self.lineEdit_9.setText(self.treeWidget.selectedItems()[0].text(1))

                print(self.treeWidget.selectedItems()[0].text(0))

        except Exception as e:
            print(e)
        # if getSelected:
        #     # value = getSelected.text(0)
            # print (value)



    def selectGM(self):
        try:
            if self.treeWidget_2.selectedItems()[0].text(0):
                self.pushButton_6.setEnabled(True)
                self.lineEdit_8.setText(self.treeWidget_2.selectedItems()[0].text(1))

                print(self.treeWidget_2.selectedItems()[0].text(0))
        #
        except Exception as e:
            print(e)
        # if getSelected:
        #     # value = getSelected.text(0)
            # print (value)


    def refresh(self):

        self.username.setText('')
        self.passwrd.setText('')
        self.passwrd_2.setText('')

        self.users.clear()
        self.mysqlCurs.execute('select * from users ')
        data = self.mysqlCurs.fetchall()
        if data:
            self.users.setHeaderLabels(['ID', 'UserName', 'Password', 'Type'])
            for i in data:
                item = QTreeWidgetItem([str(i[0]), str(i[1]), str(i[2]), str(i[3])])
                self.users.addTopLevelItem(item)


        self.lineEdit_9.setText('')
        self.treeWidget.clear()
        self.mysqlCurs.execute('select id, name from malades where type = "chronic"')
        data = self.mysqlCurs.fetchall()
        if data:
            self.treeWidget.setHeaderLabels(['ID', 'Name'])
            for i in data:
                item = QTreeWidgetItem([str(i[0]), str(i[1])])
                self.treeWidget.addTopLevelItem(item)



        self.lineEdit_8.setText('')
        self.treeWidget_2.clear()
        self.mysqlCurs.execute('select id, name from malades where type = "ginic" ')
        data = self.mysqlCurs.fetchall()
        if data:
            self.treeWidget_2.setHeaderLabels(['ID', 'Name'])
            for i in data:
                item = QTreeWidgetItem([str(i[0]), str(i[1])])
                self.treeWidget_2.addTopLevelItem(item)






    def save_user(self):

        self.mysqlCurs.execute('select * from users where username like "{}"'.format(self.username.text()))

        if self.passwrd.text() == '' or  self.passwrd_2.text() == '' or self.username.text() == '':
            err = QMessageBox.warning(self, 'ERROR', 'you have to fill all inputs ', QMessageBox.Ok)

        elif self.passwrd.text() != self.passwrd_2.text():
            err = QMessageBox.warning(self, 'ERROR', 'you have to use the same password ', QMessageBox.Ok)

        elif self.mysqlCurs.fetchone():
            err = QMessageBox.warning(self, 'ERROR', 'this user is already exists in the database', QMessageBox.Ok)

        else:
            self.acc_type = ''
            if self.admin.isChecked() :
                self.acc_type = 'admin'
            elif self.ass.isChecked():
                self.acc_type = 'ass'

            self.mysqlCurs.execute('insert into users (username, passwrd, role) values("{}", "{}", "{}")'.format(self.username.text(), self.passwrd.text(), self.acc_type))
            self.mysqlConn.commit()

            self.username.setText('')
            self.passwrd.setText('')
            self.passwrd_2.setText('')
            self.refresh()

    def forward(self, event):
        self.refresh()
        if self.tabIndex == 0:
            self.addUser.resize(1, 1)
            self.addMG.resize(self.w, self.h)
            self.addMCh.resize(1, 1)
            self.tabIndex = 1
            self.label_9.setText('2/3')

        elif self.tabIndex == 1:
            self.addUser.resize(1, 1)
            self.addMG.resize(1, 1)
            self.addMCh.resize(self.w, self.h)
            self.tabIndex = 2
            self.label_9.setText('3/3')

        elif self.tabIndex == 2:
            self.addUser.resize(self.w, self.h)
            self.addMG.resize(1, 1)
            self.addMCh.resize(1, 1)
            self.tabIndex = 0
            self.label_9.setText('1/3')


def main():
    app = QtWidgets.QApplication(sys.argv)
    splash_wn = Setting()
    splash_wn.show()
    sys.exit(app.exec_())
if __name__ == '__main__' :
    main()