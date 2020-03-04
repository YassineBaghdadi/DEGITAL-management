import json
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

import noInternetAlert
import  main



_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/pirmis.ui"))

class Pirmis(QWidget, _ui):
    def __init__(self, accT, parent = None):
        super(Pirmis, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.account_type = accT
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle('Visite Pour Pirmis')

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
        quit = QAction("Quit", self)
        quit.triggered.connect(self.closeEvent)

        self.lineEdit_3.setValidator(QIntValidator())

        self.comboBox.currentTextChanged.connect(self.clients_combo_changed)
        self.mysqlCurs = self.mysqlConn.cursor()

        self.completers_conf()
        self.pushButton.clicked.connect(self.save__)


        self.clients__ = ['choisir un Patient ...']
        try:
            self.mysqlCurs.execute('select codeP, F_name, L_name, cne from person order by F_name asc')
            # print(self.mysqlCurs.fetchall())
            for a in self.mysqlCurs.fetchall():
                if str(a[3]) == '':
                    self.clients__.append(f'{str(a[1])} {str(a[2])} {str(a[0])}')
                else:
                    self.clients__.append(f'{str(a[1])} {str(a[2])} ({str(a[3])}) {str(a[0])}')

            self.comboBox.clear()
            self.comboBox.addItems(self.clients__)
        except Exception as e:
            print(e)
            self.close()

    def clients_combo_changed(self):
        if self.comboBox.currentText() in self.clients__ and self.comboBox.currentText() != 'choisir un Patient ...':
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)

    def completers_conf(self):

        ecoles_completer = QCompleter()
        ecoles_model = QStringListModel()
        ecoles_completer.setModel(ecoles_model)
        self.completer_get_data("a", ecoles_model)
        self.lineEdit.setCompleter(ecoles_completer)


        cat_completer = QCompleter()
        cat_model = QStringListModel()
        cat_completer.setModel(cat_model)
        self.completer_get_data("c", cat_model)
        self.lineEdit_2.setCompleter(cat_completer)

        r_completer = QCompleter()
        r_model = QStringListModel()
        r_completer.setModel(r_model)
        self.completer_get_data("r", r_model)
        self.lineEdit_4.setCompleter(r_completer)



        self.session_json_data = json.loads(""" {"Medicaux":{
                    "Diabele":"n",
                    "hta":"n",
                    "Thyroide":"n",
                    "Chol":"n",
                    "Anemie":"n",
                    "Autre":"n"
                },
            "chirurgicaux":{
                    "Thyoide":"n",
                    "vb":"n",
                    "Amygdales":"n",
                    "Pelvienne":"n",
                    "Autre":"n"
                },
            "Gyneco":{
                    "first_regle_age":"n",
                    "Cycle_menstruel":"n",
                    "first_rapport_age":"n",
                    "G":"n",
                    "P":"n",
                    "fcs":"n",
                    "mfiu":"n",
                    "mort_ne":"n"
                },
            "Accauchement":{
                    "vb":"n",
                    "Cesarienne":"n",
                    "Grossesse_Actuale":"n"
                }
        }""")

    def closeEvent(self, event):
        print('quiting ...')

        self.home = main.Main(self.account_type)
        self.home.show()



    def completer_get_data(self, t, m):
        try:
            self.mysqlCurs.execute(f'select data from pirmis_completer_data where type = "{t}"')
            self.dt = [str(i[0]) for i in self.mysqlCurs.fetchall()]
            m.setStringList(self.dt)

        except Exception as e:
            print(e)


    def save__(self):

        if self.comboBox.currentText() not in self.clients__ or self.comboBox.currentText() == 'choisir un Patient ...':
            err = QMessageBox.warning(self, 'Error', 'Vous Devez Choisir un Patient')
            return

        self.mysqlCurs.execute('select data from pirmis_completer_data')
        dtt = [i[0] for i in self.mysqlCurs.fetchall()]
        if self.lineEdit.text() not in dtt and self.lineEdit.text() != '':
            self.mysqlCurs.execute(f'insert into pirmis_completer_data (data, type) value("{self.lineEdit.text()}", "a")')

        if self.lineEdit_2.text() not in dtt and self.lineEdit_2.text() != '' :
            self.mysqlCurs.execute(f'insert into pirmis_completer_data (data, type) value("{self.lineEdit_2.text()}", "c")')

        if self.lineEdit_4.text() not in dtt and self.lineEdit_4.text() != '':
            self.mysqlCurs.execute(f'insert into pirmis_completer_data (data, type) value("{self.lineEdit_4.text()}", "r")')
        # Auto Ecole : \n\nCategorie Permis : \n\nRestriction(oui/non) :


        if self.lineEdit.text() != '' and self.lineEdit_2.text() != '' and  self.lineEdit_4.text() != '' and  self.lineEdit_3.text() != '':
            self.mysqlCurs.execute(f"""insert into sessions (client_code, S_date, checking, price, reason) 
                values ("{self.comboBox.currentText().split(" ")[-1]}",
                "{self.today}", 
                "{self.session_json_data}",
                "{str(self.lineEdit_3.text()) + '(' + str(self.textEdit.toPlainText()) + ')'}",
                "Auto Ecole : {self.lineEdit.text()}\n\nCategorie Permis : {self.lineEdit_2.text()}\n\nRestriction : {self.lineEdit_4.text()}")""")

            self.comboBox.setCurrentIndex(0)
            self.lineEdit.clear()
            self.lineEdit_2.clear()
            self.lineEdit_3.clear()
            self.lineEdit_4.clear()
            self.textEdit.clear()


        else:
            err = QMessageBox.warning(self, 'Error', 'Vous Devez Remplir Toutes les Entrées', QMessageBox.Ok)

        self.mysqlConn.commit()
        self.completers_conf()
