import datetime
import random

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



import pyqtgraph as pg



from time import gmtime, strftime
from setting import *

import noInternetAlert
from db_m import DB_m

main_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/main.ui"))
# main_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/main.ui"))

class Main(QWidget, main_ui):
    def __init__(self, account_type, parent = None):
        super(Main, self).__init__(parent)
        QWidget.__init__(self)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setupUi(self)
        self.width_ = 871
        self.height_ = 431
        self.acc_type = account_type
        self.today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        # self.today = '2020-01-27 3456'
        self.sqliteConn = sqlite3.connect('src/setting.db')
        self.sqliteCurs = self.sqliteConn.cursor()
        self.host_db, self.user_db, self.passwrd_db, self.DBname, self.port_db = self.sqliteCurs.execute('select host, db_user, db_pass, db_name, port from admin_setting').fetchone()
        self.mysqlConn = pymysql.connect(
                host=self.host_db,
                user=self.user_db,
                passwd=self.passwrd_db,
                db=self.DBname,
                port=int(self.port_db)

            )
        self.mysqlCurs = self.mysqlConn.cursor()

        self.setWindowTitle('Home')
        # self.db_ = DB_m(self.host_db, self.user_db, self.passwrd_db, self.DBname, self.port_db)

        if self.acc_type == 'admin':
            pass
        else:
            self.setting_btn.setEnabled(False)
            self.sessions_btn.setEnabled(False)
            self.Statistiques_btn.setEnabled(False)

        self.home_frame.resize(self.width_, self.height_)
        self.home_icon.mousePressEvent = self.showHomeFrame
        # self.home_icon.setStyleSheet('background-image: url(img/btns/house.png);')
        # self.setting_btn.setStyleSheet('background-image: url(img/btns/settings.png);')
        self.home_icon.setPixmap(QtGui.QPixmap('img/btns/house.png'))
        self.setting_btn.setPixmap(QtGui.QPixmap('img/btns/settings.png'))
        self.home_icon.setScaledContents(True)
        self.setting_btn.setScaledContents(True)
        self.setting_btn.mousePressEvent = self.goSetting
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QImage("img/pack.png")))
        self.setPalette(palette)

        self.exit.clicked.connect(self.quit_)
        self.numbersTree.itemDoubleClicked.connect(self.handler)

        self.nums_combo.currentTextChanged.connect(self.enableSaveBtn)
        self.addNum.clicked.connect(self.saveNewNum)
        self.home_refresh()
        self.num_close.clicked.connect(self.deleteNums)
        self.num_addNew.clicked.connect(self.addPersonFrame)

        ##########################  add person part :  ##########################################################
        self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        # self.add_person_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_person_btn.png'))
        # self.add_person_btn.setScaledContents(True)
        self.add_person_btn.mousePressEvent = self.addPersonFrame
        self.add_person_save_btn.setStyleSheet('background-image: url(img/btns/off/save_btn.png);')
        # self.add_person_save_btn.setPixmap(QtGui.QPixmap('img/btns/off/save_btn.png'))
        # self.add_person_save_btn.setScaledContents(True)
        self.add_person_annuler_btn.setStyleSheet('background-image: url(img/btns/off/anuler.png);')

        # self.add_person_annuler_btn.setPixmap(QtGui.QPixmap('img/btns/off/anuler.png'))
        # self.add_person_annuler_btn.setScaledContents(True)
        self.add_person_annuler_btn.mousePressEvent = self.addPersonCancel
        self.birth_date.setDate(QtCore.QDate.currentDate())
        self.birth_date.dateChanged.connect(self.getAge)
        self.add_person_save_btn.mousePressEvent = self.addPerson
        # self.children_num.textChanged(self.virifNum(self.children_num))
        self.children_num.setValidator(QIntValidator())

        self.person_refresh()


        #RDV part:
        self.newRDVDateEdit.setDate(QtCore.QDate.currentDate())
        self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')

        # self.RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/RDV_btn.png'))
        # self.RDV_btn.setScaledContents(True)
        self.RDV_btn.mousePressEvent = self.showRDVFrame

        self.today_RDV_btn.setStyleSheet('background-image: url(img/btns/on/today_rdv_btn.png);')
        # self.today_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/on/today_rdv_btn.png'))
        # self.today_RDV_btn.setScaledContents(True)
        self.today_RDV_btn.mousePressEvent = self.showTodayRDVFrame

        self.time_out_RDV_btn.setStyleSheet('background-image: url(img/btns/off/out_rdv_btn.png);')
        # self.time_out_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/out_rdv_btn.png'))
        # self.time_out_RDV_btn.setScaledContents(True)
        self.time_out_RDV_btn.mousePressEvent = self.showTimeOutRDVFrame

        self.new_RDV_btn.setStyleSheet('background-image: url(img/btns/off/add_rdv_btn.png);')
        # self.new_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_rdv_btn.png'))
        # self.new_RDV_btn.setScaledContents(True)
        self.save_new_rdv.setStyleSheet('background-image: url(img/btns/off/save_btn.png);')
        # self.save_new_rdv.setPixmap(QtGui.QPixmap('img/btns/off/save_btn.png'))
        # self.save_new_rdv.setScaledContents(True)
        self.annuler_rdv.setStyleSheet('background-image: url(img/btns/off/anuler.png);')
        # self.annuler_rdv.setPixmap(QtGui.QPixmap('img/btns/off/anuler.png'))
        # self.annuler_rdv.setScaledContents(True)
        self.new_RDV_btn.mousePressEvent = self.showNewRDVFrame
        self.save_new_rdv.mousePressEvent = self.saveNewRDV
        self.clientListcombo.currentTextChanged.connect(self.newRdvFill)
        self.rdv_refresh()

        #search part :
        self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        # self.search_btn.setPixmap(QtGui.QPixmap('img/btns/off/search_btn.png'))
        # self.search_btn.setScaledContents(True)
        self.search_btn.mousePressEvent = self.showSearchForm
        self.save_searsh_changes.clicked.connect(self.saveEditePersonInfo)
        self.comboBox.currentTextChanged.connect(self.search_fill)
        self.lineEdit_19.setValidator(QIntValidator())

        #sessions part :
        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        # self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/off/seionse_btn.png'))
        # self.sessions_btn.setScaledContents(True)
        self.sessions_btn.mousePressEvent = self.showSessionsForm
        completer = QCompleter()

        self.session_codeP_lineEdit.setCompleter(completer)
        model = QStringListModel()
        completer.setModel(model)
        self.getData(model)

        #ditais part :
        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        # self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/off/detais.png'))
        # self.Ditails_btn.setScaledContents(True)
        self.Ditails_btn.mousePressEvent = self.showDetailsForm
        self.lineEdit_51.textChanged.connect(self.searshDetaisTree)

        #statistiques part
        self.dateEdit_2.setDate(QtCore.QDate.currentDate())
        self.dateEdit_3.setDate(QtCore.QDate.currentDate())
        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        # self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/off/statistiques_btn.png'))
        # self.Statistiques_btn.setScaledContents(True)
        self.Statistiques_btn.mousePressEvent = self.showStatistiquesForm
        self.pushButton.clicked.connect(self.statictic)

    def handler(self):
        if self.numbersTree.selectedItems()[0].text(1):
            print(self.numbersTree.selectedItems()[0].text(1))
            self.mysqlCurs.execute('select F_name, L_name, cne, codeP from person where codeP = "{}"'.format(self.numbersTree.selectedItems()[0].text(1)))
            F_name, L_name, cne, codeP = self.mysqlCurs.fetchone()
            self.goSes(F_name + ' ' + L_name + '--' + cne + '--' + codeP)

    def goSes(self, codeP):
        self.showSessionsForm(None)
        self.session_codeP_lineEdit.setText(str(codeP))

    def getData(self, m):
        self.mysqlCurs.execute('select F_name, L_name, cne, codeP from person')
        dt =[]
        for i in self.mysqlCurs.fetchall():
            dt.append(str(i[0]) + ' ' + str(i[1]) + '--' + str(i[2]) + '--' + str(i[3]))
        m.setStringList(dt)

    def deleteNums(self):

        # self.mysqlCurs.execute('SET SQL_SAFE_UPDATES = 0;')
        try:
            self.mysqlCurs.execute('select st from tools where id = 1')
            st = self.mysqlCurs.fetchone()[0]
            if st == 'c':
                self.mysqlCurs.execute('update tools set st = "o" where id = 1')

            else:
                self.mysqlCurs.execute('update tools set st = "c" where id = 1')

            self.mysqlConn.commit()
        except Exception as e:
            print(e)

        self.home_refresh()



    def saveNewNum(self):
        self.mysqlCurs.execute("""
                select count(id) from nums where client_code = "{}" and token_date like '{}'
        """.format(self.nums_combo.currentText().split(' ')[0], self.today.split(' ')[0]))
        if self.mysqlCurs.fetchone()[0]:
            err = QMessageBox.warning(self, 'ERROR', 'this client already took an number', QMessageBox.Ok)
        else:
            self.mysqlCurs.execute('select max(num) from nums where token_date like "{}"'.format(self.today.split(' ')[0]))
            last = self.mysqlCurs.fetchone()[0]
            if last:
                self.mysqlCurs.execute('insert into nums (num, client_code, token_date) values ({}, "{}", "{}")'.format(last + 1, self.nums_combo.currentText().split(' ')[0], self.today.split(' ')[0]))
            else:
                self.mysqlCurs.execute('insert into nums (num, client_code, token_date) values ({}, "{}", "{}")'.format(1, self.nums_combo.currentText().split(' ')[0], self.today.split(' ')[0]))

            self.mysqlConn.commit()
            self.home_refresh()

    def enableSaveBtn(self):
        if self.nums_combo.currentText() == 'choisir un client':
            self.addNum.setEnabled(False)
        else:
            self.addNum.setEnabled(True)



    def goSetting(self, event):
        self.sett = Setting()
        self.sett.show()


    def statictic(self):
        # self.visits = 0
        # self.cls_incription = 0
        # self.rdvs = 0
        # self.money = 0
        if str(self.dateEdit_2.date().toPyDate()) >= str(self.dateEdit_3.date().toPyDate()):
            err = QMessageBox.warning(self, 'ERROR', 'invalid dates ', QMessageBox.Ok)
        else:
            if self.comboBox_2.currentText() == 'For All ...':
                self.mysqlCurs.execute("""
                    select count(client_code) from sessions where S_date >= '{}' and S_date <= '{}'
                """.format(str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
                self.visits = self.mysqlCurs.fetchone()[0]
                self.mysqlCurs.execute("""
                    select count(codeP) from person where inscri_date >= '{}' and inscri_date <= '{}'
                """.format(str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
                self.cls_incription = self.mysqlCurs.fetchone()[0]
                self.mysqlCurs.execute("""
                    select count(id) from RDV where rdv_date >= '{}' and rdv_date <= '{}' 
                """.format(str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
                self.rdvs = self.mysqlCurs.fetchone()[0]
                self.mysqlCurs.execute("""
                    select sum(price) from sessions where S_date >= '{}' and S_date <= '{}'
                """.format(str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
                self.money = self.mysqlCurs.fetchone()[0]
            else:
                self.mysqlCurs.execute("""
                        select count(client_code) from sessions where client_code = '{}' and S_date >= '{}' and S_date <= '{}'
                """.format(self.comboBox_2.currentText().split(' ')[0], str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
                self.visits = self.mysqlCurs.fetchone()[0]
                self.cls_incription = 1
                self.mysqlCurs.execute('select count(id) from RDV where client_code = "{}" and rdv_date >= "{}" and rdv_date <= "{}"'.format(
                    self.comboBox_2.currentText().split(' ')[0], str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
                self.rdvs = self.mysqlCurs.fetchone()[0]
                self.mysqlCurs.execute('select sum(price) from sessions where client_code ="{}"and S_date >= "{}" and S_date <= "{}"'.format(
                    self.comboBox_2.currentText().split(' ')[0], str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
                self.money = self.mysqlCurs.fetchone()[0]

            self.label_71.setText(str(self.visits))
            self.label_72.setText(str(self.cls_incription))
            self.label_73.setText(str(self.rdvs))
            self.label_74.setText(str(self.money))


    def newRdvFill(self):
        client_info = []
        if self.clientListcombo.currentText() == 'choisir un client':
            self.newRDVF_name.setText('')
            self.newRDVL_name.setText('')
            self.newRDVtel.setText('')
            self.newRDVAddress.setText('')
            self.newRDVAssir.setText('')
            self.newRDVLast_visit.setText('')

        else:
            try:
                try:
                    self.mysqlCurs.execute('''select person.F_name, person.L_name, person.tel, person.address, person.assirance, max(S_date) 
                    from person inner join sessions on person.codeP = sessions.client_code where codeP = "{}" '''.format(str(self.clientListcombo.currentText().split(' ')[0])))

                    client_info = self.mysqlCurs.fetchone()

                    self.newRDVF_name.setText(str(client_info[0]))
                    self.newRDVL_name.setText(str(client_info[1]))
                    self.newRDVtel.setText(str(client_info[2]))
                    self.newRDVAddress.setText(str(client_info[3]))
                    self.newRDVAssir.setText(str(client_info[4]))
                    if len(str(client_info[5])) > 4:
                        self.newRDVLast_visit.setText(str(client_info[5]))
                    else:
                        self.newRDVLast_visit.setText('------')
                except Exception as e:
                    print(e)
                    err_log = open('src/logs.txt', 'a')
                    err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type ))
                    self.mysqlCurs.execute('''select person.F_name, person.L_name, person.tel, person.address, person.assirance
                                    from person where codeP = "{}" '''.format(
                        str(self.clientListcombo.currentText().split(' ')[0])))

                    client_info = self.mysqlCurs.fetchone()

                    self.newRDVF_name.setText(str(client_info[0]))
                    self.newRDVL_name.setText(str(client_info[1]))
                    self.newRDVtel.setText(str(client_info[2]))
                    self.newRDVAddress.setText(str(client_info[3]))
                    self.newRDVAssir.setText(str(client_info[4]))

            except Exception as e :
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type ))



                # self.clientListcombo.setEnabled(False)


            # try:
            #     self.mysqlCurs.execute('''select F_name, L_name, tel, address, assirance from person where codeP = "{}" '''.format(str(self.clientListcombo.currentText().split(' ')[0])))
            #
            #     client_info = self.mysqlCurs.fetchone()
            #
            #     self.newRDVF_name.setText(str(client_info[0]))
            #     self.newRDVL_name.setText(str(client_info[1]))
            #     self.newRDVtel.setText(str(client_info[2]))
            #     self.newRDVAddress.setText(str(client_info[3]))
            #     self.newRDVAssir.setText(str(client_info[4]))
            # except Exception as e :
            #     print(e)
            #     self.clientListcombo.setEnabled(False)
            #
            # try:
            #     self.mysqlCurs.execute('''select max(S_date) from sessions where client_code = "{}" '''.format(
            #         str(self.clientListcombo.currentText().split(' ')[0])))
            #     y = str(self.mysqlCurs.fetchone()[0])
            #
            #     if len(y) > 4:
            #         self.newRDVLast_visit.setText(y)
            #     else:
            #         self.newRDVLast_visit.setText('------')
            #
            # except Exception as e:
            #     print(e)

    def saveEditePersonInfo(self):
        if len(self.lineEdit_16.text().split('-')[0]) > 4 or len(self.lineEdit_16.text().split('-')[1]) > 2 or len(self.lineEdit_16.text().split('-')[2]) > 2:
            print('invalid date ')
            err = QMessageBox.warning(self, 'Error', 'invalid date ', QMessageBox.Ok)
        else:

            self.mysqlCurs.execute("""
            update person set cne = '{}',F_name = '{}', L_name = '{}', birth_date ='{}', address = '{}', tel = '{}', childs ='{}', note ='{}' where codeP = '{}'
            """.format(self.lineEdit_11.text(), self.lineEdit_14.text(), self.lineEdit_15.text(),
                       self.lineEdit_16.text(),
                       self.lineEdit_13.text(), self.lineEdit_12.text(), self.lineEdit_19.text(),
                       self.textEdit_2.toPlainText(), str(self.comboBox.currentText().split(' ')[0])))
            self.mysqlConn.commit()
            err = QMessageBox.information(self, 'DONE', 'the updated successfully', QMessageBox.Ok)

            self.searsh_refresh()


    def search_fill(self):
        if self.comboBox.currentText() == 'choisir un client':
            self.lineEdit_11.setText('')
            self.lineEdit_14.setText('')
            self.lineEdit_15.setText('')
            self.lineEdit_17.setText('')
            self.lineEdit_16.setText('')
            self.lineEdit_13.setText('')
            self.lineEdit_12.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_18.setText('')
            self.lineEdit_19.setText('')
            self.lineEdit_20.setText('')
            self.lineEdit_21.setText('')
            self.lineEdit_22.setText('')
            self.textEdit_2.setText('')

        else:
            try:
                    self.mysqlCurs.execute('''select person.cne, person.F_name, person.L_name, person.sex, 
                    person.birth_date, person.address, person.tel, person.assirance, person.family_status, person.childs, person.Genetic_disease, person.Chronic_disease, max(S_date), person.note
                    from person inner join sessions on person.codeP = sessions.client_code where codeP = "{}" '''.format(str(self.comboBox.currentText().split(' ')[0])))

                    client_info = self.mysqlCurs.fetchone()

                    self.lineEdit_11.setText(str(client_info[0]))
                    self.lineEdit_14.setText(str(client_info[1]))
                    self.lineEdit_15.setText(str(client_info[2]))
                    self.lineEdit_17.setText(str(client_info[3]))
                    self.lineEdit_16.setText(str(client_info[4]))
                    self.lineEdit_13.setText(str(client_info[5]))
                    self.lineEdit_12.setText(str(client_info[6]))
                    self.lineEdit_23.setText(str(client_info[7]))
                    self.lineEdit_18.setText(str(client_info[8]))
                    self.lineEdit_19.setText(str(client_info[9]))
                    self.lineEdit_20.setText(str(client_info[10]))
                    self.lineEdit_21.setText(str(client_info[11]))
                    self.lineEdit_22.setText(str(client_info[12]))
                    self.textEdit_2.setText(str(client_info[13]))
            except Exception as e:
                    print(e)
                    err_log = open('src/logs.txt', 'a')
                    err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type ))

    def addPersonCancel(self, event):
        self.codeP.setText('')
        self.F_name.setText('')
        self.L_name.setText('')
        self.cne.setText('')
        self.address.setText('')
        self.tel.setText('')

    def quit_(self):
        self.mysqlConn.close()
        self.close()


    def generatecode(self):
        self.id_P = ''

        chars = ['A', 'a', 0, 'B', 'b', 1, 'C', 'c', 2, 'D',
                 'd', 3, 'E', 'e', 4, 'F', 'f', 5, 'G', 'g',
                 6, 'H', 'h', 'I', 'i', 'J', 'j', 7, 'L', 'l',
                 'M', 'm', 'N', 8, 'n', 'o', 'P', 'p', 'Q', 'q',
                 'R', 'r', 'S', 's', 'T', 't', 'U', 'u', 'V', 'v',
                 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z', 9]

        for i in range(2):
            self.id_P += str(random.choice(chars))
            self.id_P += str(random.randint(0, 9))
            self.id_P += str(random.choice(chars))
            if i == 1:
                self.id_P += str(random.choice(chars))
                break

        return self.id_P


    def home_refresh(self):
        self.searsh_refresh()
        try:
            self.mysqlCurs.execute("""select token_date from nums order by token_date desc""")
            dt = self.mysqlCurs.fetchall()
            self.dates = []
            for i in dt:
                if i[0] not in self.dates:
                    self.dates.append(i[0])
        except Exception as e:
            print(e)
            self.dates = []

        if self.acc_type == 'admin':
            self.num_close.resize(87, 29)
            self.num_close.setEnabled(True)
            self.mysqlCurs.execute('select st from tools where id = 1')
            st = self.mysqlCurs.fetchone()[0]
            if st == 'c':
                self.num_close.setText('Open')
            else:
                self.num_close.setText('Close')
        else:
            self.mysqlCurs.execute('select st from tools where id = 1')
            st = self.mysqlCurs.fetchone()[0]
            if st == 'c':
                self.nums_combo.setEnabled(False)
            else:
                self.nums_combo.setEnabled(True)



        self.numbersTree.clear()
        self.mysqlCurs.execute('''select num, codeP, F_name, L_name, cne, inscri_date 
        from person inner join nums on person.codeP = nums.client_code order by token_date asc''')
        data = self.mysqlCurs.fetchall()
        self.numbersTree.clear()
        # if data:
        #     self.numbersTree.setHeaderLabels(['Number', 'ID', 'Name', 'C.N.I', 'Date d\'inscription'])
        #     for row in data:
        #         item = QTreeWidgetItem([str(row[0]), str(row[1]), str(row[2]) + ' ' + str(row[3]), str(row[4]), str(row[5])])
        #         self.numbersTree.addTopLevelItem(item)

        if data :
            self.numbersTree.setHeaderLabels(['Number', 'ID', 'Name', 'C.N.I', 'Date d\'inscription'])
            for date_ in self.dates:
                ittem = QTreeWidgetItem([date_])
                self.mysqlCurs.execute("""
                    select num, codeP, F_name, L_name, cne, inscri_date 
                                        from person inner join nums on person.codeP = nums.client_code where nums.token_date like '{}' order by num asc""".format(date_))
                for row in self.mysqlCurs.fetchall():
                    child = QTreeWidgetItem([str(row[0]), str(row[1]), str(row[2]) + ' ' + str(row[3]), str(row[4]), str(row[5])])
                    ittem.addChild(child)

                    self.numbersTree.addTopLevelItem(ittem)





        clients__ = ['choisir un client']
        try:
            self.mysqlCurs.execute('select codeP, F_name, L_name, cne from person order by F_name asc')
            # print(self.mysqlCurs.fetchall())
            for a in self.mysqlCurs.fetchall():
                if str(a[3]) == '':
                    clients__.append(str(a[0]) + ' | ' + str(a[1]) + ' ' + str(a[2] + ' ' + '------'))
                else:
                    clients__.append(str(a[0]) + ' | ' + str(a[1]) + ' ' + str(a[2] + ' ' + str(a[3])))

            self.nums_combo.clear()
            self.nums_combo.addItems(clients__)

        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
            self.nums_combo.clear()
            self.nums_combo.addItems(clients__)


    def person_refresh(self):
        self.codesP = []
        try:
            self.mysqlCurs.execute('''select codeP from person''')
            for i in self.mysqlCurs.fetchall():
                self.codesP.append(i[0])

            while True:
                self.new_code = self.generatecode()
                if self.new_code in self.codesP:
                    pass
                else:
                    self.codeP.setText(self.generatecode())
                    break

        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
            # self.codeP.setText(self.generatecode())


    def rdv_refresh(self):

        try:
            while self.todayRDVTable.rowCount() > 0:
                self.todayRDVTable.removeRow(0)

            self.today_RDV_counter.setText('')
            self.time_out_counter.setText('')
            self.rdv_counter.setText('')

            self.mysqlCurs.execute("select count(id) from RDV where rdv_date = '{}' ".format(str(self.today.split(' ')[0])))
            self.today_RDV_counter.setText(str(self.mysqlCurs.fetchone()[0]))
            self.mysqlCurs.execute("""select count(id) from RDV where rdv_date < '{}' """.format(str(self.today.split(' ')[0])))
            self.time_out_counter.setText(str(self.mysqlCurs.fetchone()[0]))
            self.mysqlCurs.execute("""select count(id) from RDV where rdv_date >= '{}' """.format(str(self.today.split(' ')[0])))
            self.rdv_counter.setText(str(self.mysqlCurs.fetchone()[0]))


            self.mysqlCurs.execute('''select person.codeP, person.F_name, person.L_name, person.cne, RDV.rdv_date, RDV.note
            from person inner join RDV on person.codeP = RDV.client_code where RDV.rdv_date >= "{}" order by rdv_date asc'''.format(str(self.today.split(' ')[0])))
            for row_number, row_data in enumerate(self.mysqlCurs.fetchall()):
                self.todayRDVTable.insertRow(row_number)
                for col_num, data in enumerate(row_data):
                    if data == '':
                        self.todayRDVTable.setItem(row_number, col_num, QtWidgets.QTableWidgetItem('--------'))
                    else:
                        self.todayRDVTable.setItem(row_number, col_num, QtWidgets.QTableWidgetItem(str(data)))


        except Exception as e :
                print(250, str(e))
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
        try:

            while self.old_RDVTabble.rowCount() > 0:
                self.old_RDVTabble.removeRow(0)

            self.mysqlCurs.execute('''select person.codeP, person.F_name, person.L_name, person.cne, RDV.rdv_date, RDV.note
                        from person inner join RDV on person.codeP = RDV.client_code where rdv_date < "{}" order by rdv_date desc '''.format(str(self.today.split(' ')[0])))

            for row_number, row_data in enumerate(self.mysqlCurs.fetchall()):
                self.old_RDVTabble.insertRow(row_number)
                for col_num, data in enumerate(row_data):
                    if data == '':
                        self.old_RDVTabble.setItem(row_number, col_num, QtWidgets.QTableWidgetItem('--------'))
                    else:
                        self.old_RDVTabble.setItem(row_number, col_num, QtWidgets.QTableWidgetItem(str(data)))



            # self.mysqlCurs.execute('''select person.codeP, person.F_name, person.L_name, person.cne, RDV.note
            #             from person inner join RDV on person.codeP = RDV.client_codewhere rdv_date < "{}"'''.format(
            #     self.today.split(' ')[0]))
            #
            # for row_number, row_data in enumerate(self.mysqlCurs.fetchall()):
            #     self.tbl.insertRow(row_number)
            #     for col_num, data in enumerate(row_data):
            #         if data == '':
            #             self.old_RDVTabble.setItem(row_number, col_num, QtWidgets.QTableWidgetItem('--------'))
            #         else:
            #             self.old_RDVTabble.setItem(row_number, col_num, QtWidgets.QTableWidgetItem(str(data)))

        except Exception as e:
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))

        clients = ['choisir un client']
        try:
            self.mysqlCurs.execute('select codeP, F_name, L_name, cne from person order by F_name asc')
            # print(self.mysqlCurs.fetchall())
            for a in self.mysqlCurs.fetchall():
                if str(a[3]) == '':
                    clients.append(str(a[0]) + ' | ' + str(a[1]) + ' ' + str(a[2] + ' ' + '------'))
                else:
                    clients.append(str(a[0]) + ' | ' + str(a[1]) + ' ' + str(a[2] + ' ' + str(a[3])))

            self.clientListcombo.clear()
            self.clientListcombo.addItems(clients)

        except Exception as e:
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
                self.clientListcombo.clear()
                self.clientListcombo.addItems(clients)



    def searsh_refresh(self):

        # self.mysqlConn.commit()
        clients_ = ['choisir un client']
        try:
            self.mysqlCurs.execute('select codeP, F_name, L_name, cne from person order by F_name asc')
            # print(self.mysqlCurs.fetchall())
            for a in self.mysqlCurs.fetchall():
                if str(a[3]) == '':
                    clients_.append(str(a[0]) + ' | ' + str(a[1]) + ' ' + str(a[2] + ' ' + '------'))
                else:
                    clients_.append(str(a[0]) + ' | ' + str(a[1]) + ' ' + str(a[2] + ' ' + str(a[3])))

            self.comboBox.clear()
            self.comboBox.addItems(clients_)

        except Exception as e:
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
                self.comboBox.clear()
                self.comboBox.addItems(clients_)


        self.mysqlConn.commit()




    def addPerson(self, event):
        try:
            self.person_refresh()
        except Exception as e:
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
        self.sexe = ''
        self.pdt = []
        try:
            self.mysqlCurs.execute('select * from person where F_name = "{}" and  L_name = "{}" and birth_date = "{}"'
                                       .format(self.F_name.text(), self.L_name.text(),
                                               str(self.birth_date.date().toPyDate())))
            self.pdt = self.mysqlCurs.fetchone()
        except Exception as e:
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))

        if self.homme.isChecked():
            self.sexe += 'HOMME'

        elif self.femme.isChecked():
            self.sexe += 'FEMME'

        if len(self.F_name.text()) < 2 or len(self.F_name.text()) > 30:
            self.F_name.setFocus()
            err = QMessageBox.information(self, '', 'Prénom invalide', QMessageBox.Ok)


        elif len(self.L_name.text()) < 2 or len(self.L_name.text()) > 30:
            self.F_name.setFocus()
            err = QMessageBox.information(self, '', ' le nom de famille invalide', QMessageBox.Ok)

        elif self.birth_date.date().toPyDate() >= datetime.date.today() :
            don = QMessageBox.information(self, 'ERROR DATE', 'la date invalide', QMessageBox.Ok)

        elif self.pdt:
            err = QMessageBox.information(self, 'Alert', 'cette personne existe déjà dans la base de données Sous cette code  '
                                                         ': "{}" - ont été inscrits à : "{}"'.format(self.pdt[1], self.pdt[13]), QMessageBox.Ok)

        else:
            addPq = """insert into person (codeP, F_name,L_name, birth_date, sex, cne, family_status,childs, address, tel, assirance, work, note, inscri_date, inscri_time )values (
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}' , '{}', '{}') ;"""
            try:
                self.mysqlCurs.execute(addPq.format(self.codeP.text(), self.F_name.text(), self.L_name.text(), str(self.birth_date.date().toPyDate()), self.sexe, self.cne.text(), str(self.familly_state.currentText()),
                        self.children_num.text(),
                        self.address.text(),
                        self.tel.text(),
                        str(self.assurance_type.currentText()),
                         str(self.prof_combo.currentText()),
                        self.note.toPlainText(),
                        self.today.split(' ')[0],
                        self.today.split(' ')[1]
                        ))
                err = QMessageBox.information(self, '', 'the adding operation successfully', QMessageBox.Ok)
                # try:
                #     self.mysqlCurs.execute(addPq.format(self.codeP.text(), self.F_name.text(), self.L_name.text(), str(self.birth_date.date().toPyDate()), self.sexe, self.cne.text(), str(self.familly_state.currentText()),
                #         self.children_num.text(),
                #         self.address.text(),
                #         self.tel.text(),
                #         str(
                #             self.assurance_type.currentText()),
                #         self.note.toPlainText(),
                #         self.today
                #         ))
                #     err = QMessageBox.information(self, '', 'the adding operation successfully', QMessageBox.Ok)
                #
                # except Exception as e:
                #     print(e)
                #     self.mysqlCurs.execute('''create table if not exists person (codeP varchar(10) PRIMARY KEY, F_name varchar(20),
                #                              L_name varchar(30), birth_date varchar(30) , sex varchar(10), cne varchar(12), family_status varchar (15),
                #                              childs int , address varchar(255), tel varchar(20), assirance varchar(255), note text, inscri_date varchar(20))
                #                              ENGINE=INNODB default charset = utf8;;''')
                #     self.mysqlConn.commit()
                #     self.mysqlCurs.execute(addPq.format(
                #         self.codeP.text(),
                #         self.F_name.text(),
                #         self.L_name.text(),
                #         str(
                #             self.birth_date.date().toPyDate()),
                #         self.sexe,
                #         self.cne.text(),
                #         str(
                #             self.familly_state.currentText()),
                #         self.children_num.text(),
                #         self.address.text(),
                #         self.tel.text(),
                #         str(
                #             self.assurance_type.currentText()),
                #         self.note.toPlainText(),
                #         str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
                #         ))
                #
                #     err = QMessageBox.information(self, '', 'the adding operation successfully', QMessageBox.Ok)

                self.mysqlConn.commit()

                self.codeP.setText('')
                self.F_name.setText('')
                self.L_name.setText('')
                self.cne.setText('')
                self.address.setText('')
                self.tel.setText('')
            except Exception as e :
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
                self.err = noInternetAlert.NoInternetAlert()
                self.close()
                self.err.show()
            self.birth_date.setDate(QtCore.QDate.currentDate())

    def getAge(self):
        if self.birth_date.date().toPyDate() <= datetime.date.today() :
            self.age_counter.setText(str((datetime.date.today().year - self.birth_date.date().toPyDate().year)))
            print('', datetime.date.today() , ' - ' , ' ' , self.birth_date.date().toPyDate() , ' = ' ,  datetime.date.today().year - self.birth_date.date().toPyDate().year )
        else:
            # self.birth_date.setDate(QtCore.QDate.currentDate())
            self.age_counter.setText('00')
            don = QMessageBox.information(self, 'ERROR DATE', 'la date invalide', QMessageBox.Ok)
            self.birth_date.setDate(QtCore.QDate.currentDate())

    def showSessionsForm(self, event):

        # self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.add_person_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_person_btn.png'))
        self.add_person_btn.setScaledContents(True)

        # self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/RDV_btn.png'))
        self.RDV_btn.setScaledContents(True)

        # self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.search_btn.setPixmap(QtGui.QPixmap('img/btns/off/search_btn.png'))
        self.search_btn.setScaledContents(True)

        # self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/on/seionse_btn.png'))
        self.sessions_btn.setScaledContents(True)

        # self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/off/detais.png'))
        self.Ditails_btn.setScaledContents(True)

        # self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/off/statistiques_btn.png'))
        self.Statistiques_btn.setScaledContents(True)

        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        self.Statistiques_frame.resize(1, 1)
        self.sessions_frame.resize(self.width_, self.height_)

    def showHomeFrame(self, event):

        # self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.add_person_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_person_btn.png'))
        self.add_person_btn.setScaledContents(True)

        # self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/RDV_btn.png'))
        self.RDV_btn.setScaledContents(True)

        # self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.search_btn.setPixmap(QtGui.QPixmap('img/btns/off/search_btn.png'))
        self.search_btn.setScaledContents(True)

        # self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/off/seionse_btn.png'))
        self.sessions_btn.setScaledContents(True)

        # self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/off/detais.png'))
        self.Ditails_btn.setScaledContents(True)

        # self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/off/statistiques_btn.png'))
        self.Statistiques_btn.setScaledContents(True)

        self.home_frame.resize(self.width_, self.height_)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)
        self.sessions_frame.resize(1, 1)
        self.home_refresh()

    def addPersonFrame(self, event):
        try:
            self.person_refresh()
        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
        # self.add_person_btn.setStyleSheet('background-image: url(img/btns/on/add_person_btn.png);')
        self.add_person_btn.setPixmap(QtGui.QPixmap('img/btns/on/add_person_btn.png'))
        self.add_person_btn.setScaledContents(True)

        # self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/RDV_btn.png'))
        self.RDV_btn.setScaledContents(True)

        # self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.search_btn.setPixmap(QtGui.QPixmap('img/btns/off/search_btn.png'))
        self.search_btn.setScaledContents(True)

        # self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/off/seionse_btn.png'))
        self.sessions_btn.setScaledContents(True)

        # self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/off/detais.png'))
        self.Ditails_btn.setScaledContents(True)

        # self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/off/statistiques_btn.png'))
        self.Statistiques_btn.setScaledContents(True)


        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(self.width_, self.height_)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)
        self.sessions_frame.resize(1, 1)

    def showRDVFrame(self, event):
        try:
            self.rdv_refresh()
        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
        # self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.add_person_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_person_btn.png'))
        self.add_person_btn.setScaledContents(True)

        # self.RDV_btn.setStyleSheet('background-image: url(img/btns/on/RDV_btn.png);')
        self.RDV_btn.setPixmap(QtGui.QPixmap('img/btns/on/RDV_btn.png'))
        self.RDV_btn.setScaledContents(True)

        # self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.search_btn.setPixmap(QtGui.QPixmap('img/btns/off/search_btn.png'))
        self.search_btn.setScaledContents(True)

        # self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/off/seionse_btn.png'))
        self.sessions_btn.setScaledContents(True)

        # self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/off/detais.png'))
        self.Ditails_btn.setScaledContents(True)

        # self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/off/statistiques_btn.png'))
        self.Statistiques_btn.setScaledContents(True)


        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(self.width_, self.height_)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)
        self.sessions_frame.resize(1, 1)

    def showTodayRDVFrame(self, event):
        # self.today_RDV_btn.setStyleSheet('background-image: url(img/btns/on/today_rdv_btn.png);')
        self.today_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/on/today_rdv_btn.png'))
        self.today_RDV_btn.setScaledContents(True)

        # self.time_out_RDV_btn.setStyleSheet('background-image: url(img/btns/off/out_rdv_btn.png);')
        self.time_out_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/out_rdv_btn.png'))
        self.time_out_RDV_btn.setScaledContents(True)

        # self.new_RDV_btn.setStyleSheet('background-image: url(img/btns/off/add_rdv_btn.png);')
        self.new_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_rdv_btn.png'))
        self.new_RDV_btn.setScaledContents(True)

        self.today_RDV_frame.resize(821, 311)
        self.time_out_RDV_frame.resize(1, 1)
        self.new_RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def showTimeOutRDVFrame(self, event):
        # self.today_RDV_btn.setStyleSheet('background-image: url(img/btns/off/today_rdv_btn.png);')
        self.today_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/today_rdv_btn.png'))
        self.today_RDV_btn.setScaledContents(True)

        # self.time_out_RDV_btn.setStyleSheet('background-image: url(img/btns/on/out_rdv_btn.png);')
        self.time_out_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/on/out_rdv_btn.png'))
        self.time_out_RDV_btn.setScaledContents(True)

        # self.new_RDV_btn.setStyleSheet('background-image: url(img/btns/off/add_rdv_btn.png);')
        self.new_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_rdv_btn.png'))
        self.new_RDV_btn.setScaledContents(True)

        self.today_RDV_frame.resize(1, 1)
        self.time_out_RDV_frame.resize(821, 311)
        self.new_RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def showNewRDVFrame(self, event):
        # self.today_RDV_btn.setStyleSheet('background-image: url(img/btns/off/today_rdv_btn.png);')
        self.today_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/today_rdv_btn.png'))
        self.today_RDV_btn.setScaledContents(True)

        # self.time_out_RDV_btn.setStyleSheet('background-image: url(img/btns/off/out_rdv_btn.png);')
        self.time_out_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/out_rdv_btn.png'))
        self.time_out_RDV_btn.setScaledContents(True)

        # self.new_RDV_btn.setStyleSheet('background-image: url(img/btns/on/add_rdv_btn.png);')
        self.new_RDV_btn.setPixmap(QtGui.QPixmap('img/btns/on/add_rdv_btn.png'))
        self.new_RDV_btn.setScaledContents(True)

        self.today_RDV_frame.resize(1, 1)
        self.time_out_RDV_frame.resize(1, 1)
        self.new_RDV_frame.resize(821, 311)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def saveNewRDV(self, event):

        self.mysqlCurs.execute('select * from RDV where client_code = "{}" and rdv_date ="{}"'.format(str(self.clientListcombo.currentText().split(' ')[0]), str(self.newRDVDateEdit.date().toPyDate())))
        if self.clientListcombo.currentText() == 'choisir un client':
            errr = QMessageBox.information(self, 'ERROR', "vous devez d'abord choisir un client", QMessageBox.Ok)
        elif self.newRDVDateEdit.date().toPyDate() <= datetime.date.today() :
            errr = QMessageBox.information(self, 'ERROR', "date invalide", QMessageBox.Ok)
        elif self.mysqlCurs.fetchone():
            errr = QMessageBox.information(self, 'ERROR', "this person already have this RDV", QMessageBox.Ok)
        else:
                self.mysqlCurs.execute('''
                insert into RDV (client_code, token_time, rdv_date, note) values(
                    "{}", "{}", "{}", "{}"
                )
                '''.format(str(self.clientListcombo.currentText().split(' ')[0]), self.today.split(' ')[0], str(self.newRDVDateEdit.date().toPyDate()), self.newRDVNote.toPlainText()))
                self.mysqlConn.commit()
                self.rdv_refresh()
                self.newRDVDateEdit.setDate(QtCore.QDate.currentDate())
            # try:
            #     self.mysqlCurs.execute('''
            #     insert into RDV (client_code, from_time, rdv_date, note) values(
            #         "{}", "{}", "{}", "{}"
            #     )
            #     '''.format(str(self.clientListcombo.currentText().split(' ')[0]), self.today, str(self.newRDVDateEdit.date().toPyDate()), self.newRDVNote.toPlainText()))
            # except Exception as e:
            #     print(e)
            #
            #     self.mysqlCurs.execute('''
            #         create table RDV (id INT AUTO_INCREMENT PRIMARY KEY, client_code varchar(12), from_time varchar(12), rdv_date varchar(20), note text)
            #     ''')
            #     self.mysqlConn.commit()
            #     self.mysqlCurs.execute('''
            #     insert into RDV (client_code, from_time, rdv_date, note) values(
            #         "{}", "{}", "{}", "{}"
            #     )
            #     '''.format(str(self.clientListcombo.currentText().split(' ')[0]), self.today, str(self.newRDVDateEdit.date().toPyDate()), self.newRDVNote.toPlainText()))


    # def annulerNewRDV(self, event):#todo
    #     # self.annuler_rdv.setStyleSheet('background-image: url(img/btns/on/anuler.png);')
    #     # time.sleep(0.05)
    #     # self.annuler_rdv.setStyleSheet('background-image: url(img/btns/off/anuler.png);')
    #     print('clicked')

    def showSearchForm(self, event):
        try:
            self.searsh_refresh()
        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
        # self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.add_person_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_person_btn.png'))
        self.add_person_btn.setScaledContents(True)

        # self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/RDV_btn.png'))
        self.RDV_btn.setScaledContents(True)

        # self.search_btn.setStyleSheet('background-image: url(img/btns/on/search_btn.png);')
        self.search_btn.setPixmap(QtGui.QPixmap('img/btns/on/search_btn.png'))
        self.search_btn.setScaledContents(True)

        # self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/off/seionse_btn.png'))
        self.sessions_btn.setScaledContents(True)

        # self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/off/detais.png'))
        self.Ditails_btn.setScaledContents(True)

        # self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/off/statistiques_btn.png'))
        self.Statistiques_btn.setScaledContents(True)

        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(self.width_, self.height_)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)
        self.sessions_frame.resize(1, 1)


    def showDetailsForm(self, event):
        try:
            # self.refresh()
            # self.searshDetaisTree()
            self.detais_refresh()
        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))

        # self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.add_person_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_person_btn.png'))
        self.add_person_btn.setScaledContents(True)

        # self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/RDV_btn.png'))
        self.RDV_btn.setScaledContents(True)

        # self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.search_btn.setPixmap(QtGui.QPixmap('img/btns/off/search_btn.png'))
        self.search_btn.setScaledContents(True)

        # self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/off/seionse_btn.png'))
        self.sessions_btn.setScaledContents(True)

        # self.Ditails_btn.setStyleSheet('background-image: url(img/btns/on/detais.png);')
        self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/on/detais.png'))
        self.Ditails_btn.setScaledContents(True)

        # self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/off/statistiques_btn.png'))
        self.Statistiques_btn.setScaledContents(True)

        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(self.width_, self.height_)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)
        self.sessions_frame.resize(1, 1)

        #
        # try:
        #     self.mysqlCurs.execute('select codeP, F_name, L_name, cne, birth_date, family_status, address, tel, inscri_date from person order by F_name asc')
        #     for i in self.mysqlCurs.fetchall():
        #         self.mysqlCurs.execute('select rdv_date, note from RDV where client_code like "{}" order by rdv_date desc'.format(i[0]))
        #         ch1 = QTreeWidgetItem([' Tout les RDVs : '])
        #         for rdv in self.mysqlCurs.fetchall():
        #             rr = QTreeWidgetItem(rdv)
        #             ch1.addChild(rr)
        #
        #         ch2 = QTreeWidgetItem(['Sessions History'])
        #         self.mysqlCurs.execute('select S_date, price from RDV where client_code like "{}" order by rdv_date desc'.format(i[0]))
        #         for session in self.mysqlCurs.fetchall():
        #             ss = QTreeWidgetItem(session)
        #             ch2.addChild(ss)
        #
        #         self.mysqlCurs.execute('select sum(price) from sessions where client_code like "{}"'.format(i[0]))
        #         tt_money = self.mysqlCurs.fetchone()
        #         ch3 = QTreeWidgetItem(['Total money spended : ', tt_money])
        #
        #         ch4 = QTreeWidgetItem(['Familly : '])
        #         self.mysqlCurs.execute('select codeP, F_name, L_name, cne, Address from person where L_name like "{}"'.format(i[2]))
        #         item = QTreeWidgetItem(i)
        #         item.addChild(ch1)
        #         item.addChild(ch2)
        #         item.addChild(ch3)
        #         item.addChild(ch4)
        #         self.treeWidget.addTopLevelItem(item)
        #
        # except Exception as e:
        #     print(e)

    def showStatistiquesForm(self, event):
        try:
            self.searshDetaisTree()
        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))

        # self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.add_person_btn.setPixmap(QtGui.QPixmap('img/btns/off/add_person_btn.png'))
        self.add_person_btn.setScaledContents(True)

        # self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.RDV_btn.setPixmap(QtGui.QPixmap('img/btns/off/RDV_btn.png'))
        self.RDV_btn.setScaledContents(True)

        # self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.search_btn.setPixmap(QtGui.QPixmap('img/btns/off/search_btn.png'))
        self.search_btn.setScaledContents(True)

        # self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/off/seionse_btn.png'))
        self.sessions_btn.setScaledContents(True)

        # self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/off/detais.png'))
        self.Ditails_btn.setScaledContents(True)

        # self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/on/statistiques_btn.png);')
        self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/on/statistiques_btn.png'))
        self.Statistiques_btn.setScaledContents(True)

        try:
            clients = ['For All ...']
            self.mysqlCurs.execute('select codeP, F_name, L_name, cne from person order by F_name asc')
            # print(self.mysqlCurs.fetchall())
            for a in self.mysqlCurs.fetchall():
                if str(a[3]) == '':
                    clients.append(str(a[0]) + ' | ' + str(a[1]) + ' ' + str(a[2] + ' ' + '------'))
                else:
                    clients.append(str(a[0]) + ' | ' + str(a[1]) + ' ' + str(a[2] + ' ' + str(a[3])))

            self.comboBox_2.clear()
            self.comboBox_2.addItems(clients)
        except Exception as e:
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))

        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        self.sessions_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(self.width_, self.height_)

    def detais_refresh(self):
        try:
            self.treeWidget.clear()

            self.treeWidget.setColumnCount(9)
            self.treeWidget.setHeaderLabels(
                ["code", "prenom", "nom", "C.N.I", "naissance", "S Familier", "adresse", "TEL", "Inscri a"])
            self.mysqlCurs.execute(
                'select codeP, F_name, L_name, cne, birth_date, family_status, address, tel, inscri_date from person order by F_name asc')
            data = self.mysqlCurs.fetchall()
            if data:
                # self.treeWidget.resize(841, 321)
                self.treeWidget.setGeometry(15, 101, 841, 321)
                self.label_2.setGeometry(1, 1, 1, 1)
                for i in data:
                    item = QTreeWidgetItem([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]])

                    self.mysqlCurs.execute(
                        'select rdv_date, note from RDV where client_code like "{}" order by rdv_date desc'.format(
                            i[0]))

                    rdvs = self.mysqlCurs.fetchall()
                    if rdvs:
                        ch1 = QTreeWidgetItem([' Tout les RDVs : {}'.format(len(rdvs))])
                        for rdv in rdvs:
                            rr = QTreeWidgetItem([rdv[0], rdv[1]])
                            ch1.addChild(rr)
                        item.addChild(ch1)

                    self.mysqlCurs.execute(
                        'select S_date, price from sessions where client_code like "{}" order by S_date desc'.format(
                            i[0]))
                    sessions = self.mysqlCurs.fetchall()
                    if sessions:
                        ch2 = QTreeWidgetItem(['Sessions History : {}'.format(len(sessions))])
                        for session in sessions:
                            ss = QTreeWidgetItem([session[0], session[1]])
                            ch2.addChild(ss)
                            item.addChild(ch2)

                    self.mysqlCurs.execute('select sum(price) from sessions where client_code like "{}"'.format(i[0]))
                    tt_money = self.mysqlCurs.fetchone()
                    if tt_money[0]:
                        ch3 = QTreeWidgetItem(['Total money spended : ', '{} DH'.format(tt_money[0])])
                        item.addChild(ch3)

                    self.mysqlCurs.execute(
                        'select codeP, F_name, L_name, cne, Address from person where L_name like "{}" and codeP != "{}"'.format(
                            i[2], i[0]))
                    familly = self.mysqlCurs.fetchall()
                    if familly:
                        ch4 = QTreeWidgetItem(['Familly : {}'.format(len(familly))])
                        for family in familly:
                            ff = QTreeWidgetItem([family[0], family[1], family[2], family[3]])
                            ch4.addChild(ff)
                        item.addChild(ch4)

                    self.treeWidget.addTopLevelItem(item)
            else:
                self.treeWidget.setGeometry(1, 1, 1, 1)
                self.label_2.setGeometry(230, 140, 420, 183)
                # self.label_2.setStyleSheet('background-image: url(img/nodatafound.png);')
                self.label_2.setPixmap(QtGui.QPixmap('img/nodatafound.png'))
                self.label_2.setScaledContents(True)
        except Exception as e:
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))


    def searshDetaisTree(self ):
        key = self.lineEdit_51.text()
        if key != '':
            self.treeWidget.clear()
            self.treeWidget.setColumnCount(9)
            self.treeWidget.setHeaderLabels(
                ["code", "prenom", "nom", "C.N.I", "naissance", "S Familier", "adresse", "TEL", "Inscri a"])
            self.mysqlCurs.execute(
                '''select codeP, F_name, L_name, cne, birth_date, family_status, address, tel, inscri_date from person
                 where codeP like "%{}%" or F_name like "%{}%" or L_name like "%{}%" or 
                 cne like "%{}%" or address like "%{}%" or tel like "%{}%" order by F_name asc '''.format(key, key, key, key, key, key))
            data = self.mysqlCurs.fetchall()
            if data :
                # self.treeWidget.resize(841, 321)
                self.treeWidget.setGeometry(15, 101, 841, 321)
                self.label_2.setGeometry(1, 1, 1, 1)
                for i in data:
                    item = QTreeWidgetItem([i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]])
                    self.mysqlCurs.execute(
                        'select rdv_date, note from RDV where client_code like "{}" order by rdv_date desc'.format(i[0]))

                    rdvs = self.mysqlCurs.fetchall()
                    if rdvs:
                        ch1 = QTreeWidgetItem([' Tout les RDVs : {}'.format(len(rdvs))])
                        for rdv in rdvs:
                            rr = QTreeWidgetItem([rdv[0], rdv[1]])
                            ch1.addChild(rr)
                        item.addChild(ch1)


                    self.mysqlCurs.execute(
                        'select S_date, price from sessions where client_code like "{}" order by S_date desc'.format(i[0]))
                    sessions = self.mysqlCurs.fetchall()
                    if sessions:
                        ch2 = QTreeWidgetItem(['Sessions History : {}'.format(len(sessions))])
                        for session in sessions:
                            ss = QTreeWidgetItem([session[0], session[1]])
                            ch2.addChild(ss)
                            item.addChild(ch2)



                    self.mysqlCurs.execute('select sum(price) from sessions where client_code like "{}"'.format(i[0]))
                    tt_money = self.mysqlCurs.fetchone()
                    if tt_money[0]:
                        ch3 = QTreeWidgetItem(['Total money spended : ', f'{str(tt_money[0])} DH'])
                        item.addChild(ch3)



                    self.mysqlCurs.execute(
                        'select codeP, F_name, L_name, cne, Address from person where L_name like "{}" and codeP != "{}"'.format(i[2], i[0]))
                    familly = self.mysqlCurs.fetchall()
                    if familly:
                        ch4 = QTreeWidgetItem(['Familly : {}'.format(len(familly))])
                        for family in familly:
                            ff = QTreeWidgetItem([family[0], family[1], family[2], family[3]])
                            ch4.addChild(ff)
                        item.addChild(ch4)

                    self.treeWidget.addTopLevelItem(item)
            else:
                self.treeWidget.setGeometry(1, 1, 1, 1)
                self.label_2.setGeometry(230, 140, 420, 183)
                # self.label_2.setStyleSheet('background-image: url(img/nodatafound.png);')
                self.label_2.setPixmap(QtGui.QPixmap('img/nodatafound.png'))
                self.label_2.setScaledContents(True)

        else:
            self.detais_refresh()



