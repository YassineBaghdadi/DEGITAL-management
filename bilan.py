import pipes

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

from create_pdf import  *
import noInternetAlert



_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/bilan.ui"))

class Bilan(QWidget, _ui):
    def __init__(self, parent = None):
        super(Bilan, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.move(20,10)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Setting')
        self.today = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))

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
        self.current_tahalil = []

        self.lineEdit.textChanged.connect(self.enable_add_btn)
        self.pushButton.clicked.connect(self.add)
        self.refresh()
        self.pushButton_2.clicked.connect(self.save_)
        self.clients = ['choisir un patient']
        self.mysqlCurs.execute(f'select F_name, L_name, codeP from person')
        for i in self.mysqlCurs.fetchall():
            self.clients.append(f'{i[0]} {i[1]} ("{i[2]}")')

        self.comboBox.addItems(self.clients)

    def save_(self):
        client = self.comboBox.currentText()
        if client == 'choisir un patient':
            err = QMessageBox.warning(self, 'ERROR', 'you have to choose patient')
        else:
            self.data = ''
            info = list(self.sqliteCurs.execute('select adress, city, num from info ').fetchone())
            for i in range(self.treeWidget.topLevelItemCount()):
                self.data += self.treeWidget.topLevelItem(i).text(0) + '@'

            self.file_path, _ = QFileDialog.getSaveFileName(caption='save as : ',
                                                            directory=f"""./{client.replace('"', '')} Bilan Biologique [{str(time.strftime("%Y-%m-%d %Hh%M", time.gmtime()))}].pdf""",
                                                            filter="Pdf files (*.pdf)")
            print(f'the path : {self.file_path}')
            print(str(self.comboBox.currentText()).split("(")[1].split(")")[0])
            self.mysqlCurs.execute(f'select birth_date from person where codeP = {str(self.comboBox.currentText()).split("(")[1].split(")")[0]} ')#todo errrrrrrrrr
            age = int(self.today.split('-')[0]) - int(str(self.mysqlCurs.fetchone()[0]).split('-')[0])
            outPdf = Tahalil_pdf(client, age, self.data, info, self.file_path)

    def refresh(self):
        self.mysqlCurs.execute(f'select tahalil_name from tahalil')
        self.all_tahalil = [i[0] for i in self.mysqlCurs.fetchall()]

        self.mysqlCurs.execute(f'select tahalil_name from tahalil')

        wordList =[i[0] for i in self.mysqlCurs.fetchall()]
        print(wordList)


        completer = QCompleter(wordList, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(completer)


    def add(self):

        self.treeWidget.addTopLevelItem(QTreeWidgetItem([str(self.lineEdit.text())]))
        self.current_tahalil.append(str(self.lineEdit.text()))
        if self.lineEdit.text() not in self.all_tahalil:
            self.mysqlCurs.execute(f'insert into tahalil(tahalil_name) value("{self.lineEdit.text()}")')
            self.mysqlConn.commit()

        self.lineEdit.clear()
        self.refresh()

    def enable_add_btn(self):
        if self.lineEdit.text() != '' and self.lineEdit.text() not in self.current_tahalil:
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)




def main():
    app = QtWidgets.QApplication(sys.argv)
    splash_wn = Bilan()
    splash_wn.show()
    sys.exit(app.exec_())
if __name__ == '__main__' :
    main()
