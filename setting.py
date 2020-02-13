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
        self.setWindowTitle('Setting')
        self.today = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        self.pushButton.clicked.connect(self.save_info)

        self.save.clicked.connect(self.save_user)
        self.sqliteConn = sqlite3.connect('src/setting.db')
        self.sqliteCurs = self.sqliteConn.cursor()
        p_info = self.sqliteCurs.execute('select adress, city, num from info ').fetchone()

        self.lineEdit_4.setText(str(p_info[0]))
        self.lineEdit_2.setText(str(p_info[1]))
        self.lineEdit_3.setText(str(p_info[2]))
        self.lineEdit_4.textChanged.connect(self.adress_typing)
        self.label_7.setText(f'{str(len(self.lineEdit_4.text()))}/75')


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
        self.delete_2.clicked.connect(self.deleteUser)

        self.tabWidget.currentChanged.connect(self.tab_changed_refresh)

        self.comboBox.currentTextChanged.connect(self.perm_ref)
        self.pushButton_2.clicked.connect(self.seve_permissions)

    def seve_permissions(self):
        self.refresh()
        permissions = ''
        if self.checkBox.isChecked():
            permissions += '0'

        if self.checkBox_2.isChecked():
            permissions += '1'

        if self.checkBox_6.isChecked():
            permissions += '2'

        if self.checkBox_3.isChecked():
            permissions += '3'

        if self.checkBox_4.isChecked():
            permissions += '4'

        if self.checkBox_5.isChecked():
            permissions += '5'

        self.mysqlCurs.execute(f'update users set role = "{permissions}" where username like "{self.comboBox.currentText()}"')
        self.mysqlConn.commit()


    def save_info(self):
        #Édifice Tariq - n ° 5 (au-dessus de la pharmacie Tariq)- rue Bani Marin
        #05.35.20.15.70
        self.sqliteCurs.execute('delete from info')
        self.sqliteConn.commit()
        self.sqliteCurs.execute(f'insert into info values ("{str(self.lineEdit_4.text())}", "{str(self.lineEdit_2.text())}", "{str(self.lineEdit_3.text())}")')
        self.sqliteConn.commit()

    def adress_typing(self):
        self.label_7.setText(f'{str(len(self.lineEdit_4.text()))}/75')
        if len(self.lineEdit_4.text()) > 75:
            self.pushButton.setEnabled(False)
            self.label_7.setText('error')
        else:
            self.pushButton.setEnabled(True)




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

    def tab_changed_refresh(self):
        self.refresh()
        if self.tabWidget.currentIndex() == 2:
            # self.perm_ref()
            self.mysqlCurs.execute('select username from users where role not like "admin"')
            dt = list(self.mysqlCurs.fetchall())

            users_ass = ['']
            if dt:
                for i in dt:
                    users_ass.append(i[0])

                self.comboBox.clear()
                self.comboBox.addItems(users_ass)

    def perm_ref(self):
        if self.comboBox.currentText():
            self.pushButton_2.setEnabled(True)
            self.mysqlCurs.execute(f'select role from users where role not like "admin" and username like "{self.comboBox.currentText()}"')
            # print(self.mysqlCurs.fetchone())
            dt1 = str(self.mysqlCurs.fetchone()[0])
            print(dt1.split())

            self.checkBox.setChecked(False)
            if '0' in dt1:
                self.checkBox.setChecked(True)

            self.checkBox_2.setChecked(False)
            if '1' in dt1:
                self.checkBox_2.setChecked(True)


            self.checkBox_6.setChecked(False)
            if '2' in dt1:
                self.checkBox_6.setChecked(True)

            self.checkBox_3.setChecked(False)
            if '3' in dt1:
                self.checkBox_3.setChecked(True)

            self.checkBox_4.setChecked(False)
            if '4' in dt1:
                self.checkBox_4.setChecked(True)


            self.checkBox_5.setChecked(False)
            if '5' in dt1:
                self.checkBox_5.setChecked(True)
        else:
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.pushButton_2.setEnabled(False)




    def refresh(self):
        # self.perm_ref()
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
#
def main():
    app = QtWidgets.QApplication(sys.argv)
    splash_wn = Setting()
    splash_wn.show()
    sys.exit(app.exec_())
if __name__ == '__main__' :
    main()