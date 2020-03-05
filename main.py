import datetime
import json
import random as rnd

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
# from graph import *
from about import *
from graph import *

import pyqtgraph as pg

from time import gmtime, strftime
from setting import *
from today_money_details import *
import noInternetAlert
from db_m import DB_m
from create_pdf import *
import logIn

main_ui, _ = loadUiType(path.join(path.dirname(__file__), "ui/main.ui"))

from bilan import *
# main_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/main.ui"))
from pirmis import *

class Main(QWidget, main_ui):
    def __init__(self, account_type, parent=None):
        super(Main, self).__init__(parent)
        QWidget.__init__(self)

        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setupUi(self)
        self.width_ = 871
        self.height_ = 431
        self.acc_type = account_type
        self.today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        print(self.today)
        # self.today = '2020-01-27 3456'
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
        self.home_icon_2.mousePressEvent = self.aboutUs
        self.mysqlCurs = self.mysqlConn.cursor()

        self.setWindowTitle('Home')
        # self.db_ = DB_m(self.host_db, self.user_db, self.passwrd_db, self.DBname, self.port_db)

        if self.acc_type != 'admin':

            self.permissions = [i for i in str(self.acc_type)]
            self.setting_btn.setEnabled(False)
            self.add_person_btn.setEnabled(False)
            self.RDV_btn.setEnabled(False)
            self.search_btn.setEnabled(False)
            self.Ditails_btn.setEnabled(False)
            self.sessions_btn.setEnabled(False)
            self.Statistiques_btn.setEnabled(False)
            self.pushButton_7.resize(0, 0)
            if '0' in self.permissions:

                self.add_person_btn.setEnabled(True)

            if '1' in self.permissions:
                self.RDV_btn.setEnabled(True)

            if '2' in self.permissions:
                self.search_btn.setEnabled(True)

            if '3' in self.permissions:
                self.Ditails_btn.setEnabled(True)

            if '4' in self.permissions:
                self.sessions_btn.setEnabled(True)

            if '5' in self.permissions:
                self.Statistiques_btn.setEnabled(True)

            # self.setting_btn.setEnabled(False)
            # self.sessions_btn.setEnabled(False)
            # self.Statistiques_btn.setEnabled(False)
            print(f'account type : {self.acc_type} \npermissions : {self.permissions}')
        self.home_frame.resize(self.width_, self.height_)
        self.home_icon.mousePressEvent = self.showHomeFrame
        # self.home_icon.setStyleSheet('background-image: url(img/btns/house.png);')
        # self.setting_btn.setStyleSheet('background-image: url(img/btns/settings.png);')
        self.home_icon.setPixmap(QtGui.QPixmap('img/btns/house.png'))
        self.setting_btn.setPixmap(QtGui.QPixmap('img/btns/settings.png'))
        self.home_icon.setScaledContents(True)
        self.home_icon_2.setPixmap(QtGui.QPixmap('img/about.png'))
        self.home_icon_2.setScaledContents(True)
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
        self.exit_2.clicked.connect(self.logout)
        self.pushButton_7.clicked.connect(self.go_to_bilan)

        self.pirmis_btn.setPixmap(QtGui.QPixmap('img/car.png'))
        self.pirmis_btn.setScaledContents(True)

        self.pirmis_btn.mousePressEvent = self.pirmis


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
        self.pushButton_6.clicked.connect(self.last_session_price)


        # RDV part:
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

        # search part :
        self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        # self.search_btn.setPixmap(QtGui.QPixmap('img/btns/off/search_btn.png'))
        # self.search_btn.setScaledContents(True)
        self.search_btn.mousePressEvent = self.showSearchForm
        self.save_searsh_changes.clicked.connect(self.saveEditePersonInfo)
        self.comboBox.currentTextChanged.connect(self.search_fill)
        self.lineEdit_19.setValidator(QIntValidator())

        # sessions part :
        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        # self.sessions_btn.setPixmap(QtGui.QPixmap('img/btns/off/seionse_btn.png'))
        # self.sessions_btn.setScaledContents(True)
        self.sessions_btn.mousePressEvent = self.showSessionsForm

        self.tabWidget.currentChanged.connect(self.session_tab_changed_event)
        self.session_codeP_lineEdit.textChanged.connect(self.session_codeP_editText_changed)
        self.ordononce_EditLine.textChanged.connect(self.enable_ordononce_add)
        self.session_price.setValidator(QIntValidator())
        self.ordononce_add_pushButton.clicked.connect(self.add_dwa_to_treeView)
        self.current_dwayat = []
        self.dwa_count = 0
        self.ordononce_treeWidget.itemSelectionChanged.connect(self.enable_ordononce_rmv)
        self.ordononce_rmv_pushButton.clicked.connect(self.rmv_dwa_from_treeView)

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
        self.session_save_btn.clicked.connect(self.save_session)

        self.completer_ = QCompleter()
        self.completer = QCompleter()
        self.ordononce_cls_pushButton.clicked.connect(self.clear_ordonance)
        # self.checkBox.stateChanged.connect(self.change_to_permit)

        # ditais part :
        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        # self.Ditails_btn.setPixmap(QtGui.QPixmap('img/btns/off/detais.png'))
        # self.Ditails_btn.setScaledContents(True)
        self.Ditails_btn.mousePressEvent = self.showDetailsForm
        self.lineEdit_51.textChanged.connect(self.searshDetaisTree)
        self.treeWidget.itemDoubleClicked.connect(self.go_to_history_specific_session)

        # statistiques part
        self.dateEdit_2.setDate(QtCore.QDate.currentDate())
        self.dateEdit_3.setDate(QtCore.QDate.currentDate())
        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        # self.Statistiques_btn.setPixmap(QtGui.QPixmap('img/btns/off/statistiques_btn.png'))
        # self.Statistiques_btn.setScaledContents(True)
        self.Statistiques_btn.mousePressEvent = self.showStatistiquesForm
        self.pushButton.clicked.connect(self.statictic)#todo here is the problem
        self.session_history_btn.clicked.connect(self.go_specific_detai)
        self.pushButton_2.clicked.connect(self.show_visites_graph)
        self.pushButton_3.clicked.connect(self.show_visites_ages_graph)
        self.pushButton_4.clicked.connect(self.show_visites_times_graph)
        self.pushButton_5.clicked.connect(self.show_money_graph)
        self.pushButton_8.clicked.connect(self.details_today_money)


        self.bck_done = 0

    def pirmis(self, event):
        self.p = Pirmis(self.acc_type)
        self.p.show()
        self.close()


    def details_today_money(self):
        self.mysqlCurs.execute(f'select * from person inner join sessions on person.codeP = sessions.client_code where S_date like "{self.today.split(" ")[0]}%"')
        data = []
        for i in self.mysqlCurs.fetchall():
            temp_data = list([i[0] ,i[1], i[2], i[17], i[19]])
            data.append(temp_data)

        self.tmd = Today_money_details(data)
        self.tmd.show()


    def aboutUs(self, event):
        self.abt = About()


    def go_to_bilan(self):
        self.bb = Bilan()
        self.bb.show()


    # def change_to_permit(self):
    #     if self.checkBox.isChecked():
    #         self.clear_ordonance()
    #         self.session_reason_textEdit.setText('Auto Ecole : \n\nCategorie Permis : \n\nRestriction(oui/non) : ')
    #     else:
    #         self.session_reason_textEdit.clear()
    #         self.clear_ordonance()

    def clear_ordonance(self):
        self.ordononce_treeWidget.clear()




    def last_session_price(self):
        try:
            self.mysqlCurs.execute('select max(id) from sessions')
            self.mysqlCurs.execute(f'''
                select F_name, L_name, price from sessions inner join person on person.codeP = sessions.client_code where sessions.id = {self.mysqlCurs.fetchone()[0]}
            ''')

            dt = self.mysqlCurs.fetchone()
            if dt:
                self.label_58.setText(f'{dt[0]} {dt[1]}')
                self.label_59.setText(f'{str(dt[2]).split("(")[0]} DH .')
        except Exception as e:
            print(e)



    def session_tab_changed_event(self):
        if len(self.session_codeP_lineEdit.text()) > 0:
            self.session_refresh()

    def go_specific_detai(self):
        self.showDetailsForm(None, c=self.session_codeP_lineEdit.text().split("--")[-1])

    def session_codeP_editText_changed(self):
        self.clear_session_data()
        self.session_refresh()

    def save_session(self):  # TODO send Price by socket to assistent account

        if self.session_price.text() == '':
            self.session_price.setText('0')

        if self.diable_checkBox.isChecked():
            self.session_json_data["Medicaux"]["Diabele"] = self.diable_lineEdit.text()

        if self.hta_checkBox.isChecked():
            self.session_json_data["Medicaux"]["hta"] = self.hta_lineEdit.text()

        if self.thyroide_checkBox.isChecked():
            self.session_json_data["Medicaux"]["Thyroide"] = self.thyroide_lineEdit.text()

        if self.chol_checkBox.isChecked():
            self.session_json_data["Medicaux"]["chol"] = self.chol_lineEdit.text()

        if self.anemie_checkBox.isChecked():
            self.session_json_data["Medicaux"]["Anemie"] = self.anemie_lineEdit.text()

        self.session_json_data["Medicaux"]["Autre"] = str(self.medicaux_autre.toPlainText())

        ###################################################################################

        if self.thyoide_checkBox.isChecked():
            self.session_json_data["chirurgicaux"]["Thyoide"] = self.thyoide_lineEdit.text()

        if self.vb_checkBox.isChecked():
            self.session_json_data["chirurgicaux"]["vb"] = self.vb_lineEdit.text()

        if self.amygdale_checkBox.isChecked():
            self.session_json_data["chirurgicaux"]["Amygdales"] = self.amygdale_lineEdit.text()

        if self.pelvienne_checkBox.isChecked():
            self.session_json_data["chirurgicaux"]["Pelvienne"] = self.pelvienne_lineEdit.text()

        self.session_json_data["chirurgicaux"]["Autre"] = str(self.chirurgicaux_autre.toPlainText())

        ###################################################################################
        try:
            self.mysqlCurs.execute(f'select sex from person where codeP = "{self.current_client_code}"')
            sex = self.mysqlCurs.fetchone()[0]
            if sex and sex == 'FEMME':
                self.session_json_data["Gyneco"]["first_regle_age"] = str(self.first_regle_age_lineEdit.text())

                if self.regului_radioButton.isChecked():
                    self.session_json_data["Gyneco"]["Cycle_menstruel"] = str(0) + self.textEdit.text()

                if self.inregului_radioButton.isChecked():
                    self.session_json_data["Gyneco"]["Cycle_menstruel"] = str(1) + self.textEdit.text()

                self.session_json_data["Gyneco"]["first_rapport_age"] = str(self.first_rapport_age_lineEdit.text())

                self.session_json_data["Gyneco"]["G"] = str(self.G_lineEdit.text())

                self.session_json_data["Gyneco"]["P"] = str(self.P_lineEdit.text())

                if self.fcs_checkBox.isChecked():
                    self.session_json_data["Gyneco"]["fcs"] = str(self.fcs_lineEdit.text())

                if self.mfiu_checkBox.isChecked():
                    self.session_json_data["Gyneco"]["mfiu"] = str(self.mfiu_lineEdit.text())

                if self.mort_ne_checkBox.isChecked():
                    self.session_json_data["Gyneco"]["mort_ne"] = str(self.mort_ne_lineEdit.text())

        except Exception as e:
            print(e)

        ###################################################################################

        if self.vb_checkBox_2.isChecked():
            self.session_json_data["Accauchement"]["vb"] = str(self.vb_lineEdit_2.text())

        if self.cesarienne_checkBox.isChecked():
            self.session_json_data["Accauchement"]["Cesarienne"] = str(self.cesarienne_lineEdit.text())

        if self.ddr_radioButton.isChecked():
            self.session_json_data["Accauchement"]["Grossesse_Actuale"] = str(0) + str(
                str(self.ddr_dateEdit.text()))

        if self.inpressise_radioButton.isChecked():
            self.session_json_data["Accauchement"]["Grossesse_Actuale"] = str(1)



        # self.session_json_data[]
        try:
            price = str(self.session_price.text())
            self.ordonance = ''
            for ix in range(self.ordononce_treeWidget.topLevelItemCount()):
                self.ordonance += str(self.ordononce_treeWidget.topLevelItem(ix).text(0) + '---')

            self.mysqlCurs.execute(f'select count(ordonance) from sessions where client_code like "{self.session_codeP_lineEdit.text().split("--")[-1]}" and S_date like "{str(self.today.split(" ")[0])}%"')
            # print(f'select count(ordonance) from sessions where client_code like "{self.session_codeP_lineEdit.text().split("--")[-1]}" and S_date like "{str(self.today.split(" ")[0])}%"')

            if self.mysqlCurs.fetchone()[0] == 0:
                self.mysqlCurs.execute(f"""insert into sessions (client_code, S_date, checking, price, ordonance, reason) 
                    values ("{self.session_codeP_lineEdit.text().split("--")[-1]}", "{self.today}", "{self.session_json_data}",
                            "{str(self.session_price.text()) + '(' + str(self.session_price_note_textEdit.toPlainText()) + ')'}",
                            "{self.ordonance}", "{self.session_reason_textEdit.toPlainText()}")""")

                self.mysqlConn.commit()

            try:
                dialog = QMessageBox()
                dialog.setIcon(QMessageBox.Question)
                dialog.setText('would you print it ?')
                check_box = QCheckBox("use Template ?", dialog)
                check_box.setCheckState(False)
                dialog.setCheckBox(check_box)
                dialog.addButton(QMessageBox.No)
                dialog.addButton(QMessageBox.Yes)
                result = dialog.exec()
                self.blink = True
                if result == QtWidgets.QMessageBox.Yes:
                    if dialog.checkBox().checkState() == Qt.Checked:
                        self.blink = False
                    self.mysqlCurs.execute(
                        f'select codeP, F_name, L_name, birth_date from person where codeP = "{self.session_codeP_lineEdit.text().split("--")[-1]}"')
                    client = self.mysqlCurs.fetchone()
                    self.file_path, _ = QFileDialog.getSaveFileName(caption='save as : ', directory=f'./{client[1]} {client[2]} ({client[0]}) [{str(time.strftime("%Y-%m-%d %Hh%M", time.gmtime()))}].pdf',
                                                               filter="Pdf files (*.pdf)")

                    if self.file_path:
                        if str(self.file_path).split('.')[-1] != 'pdf':
                            self.file_path += '.pdf'
                            #client = 'Nom Prenom', age = 'age', ordonance =None, DR_info = ['adress', 'city', '06.30.50.46.06'] , path = None, blink_page = False
                        p_info = self.sqliteCurs.execute('select adress, city, num from info ').fetchone()
                        self.mysqlCurs.execute(f'select assirance from sessions inner join person on person.codeP = sessions.client_code where codeP = "{self.session_codeP_lineEdit.text().split("--")[-1]}"')
                        self.mitual = False
                        assirnce = self.mysqlCurs.fetchone()[0]
                        if assirnce == 'CNOPS' or assirnce == 'CNSS' or assirnce == 'FAR' or assirnce == 'SAHAM' :
                            self.mitual = True
                        print_ordononce = Ppdf(client = client[1] + ' ' + client[2] + ' (' + client[0] + ') ',
                                                age = str(int(self.today.split('-')[0]) - int(str(client[3]).split('-')[0])),
                                                ordonance = self.ordonance,
                                                DR_info = [p_info[0], p_info[1], p_info[2]],
                                                path = self.file_path,
                                                blink_page = self.blink,
                                                mitual = self.mitual,
                                                price = price)

                            # err = QMessageBox.warning(dialog, 'Error', 'invalid extention', QMessageBox.Ok)
                        self.tabWidget.setCurrentIndex(0)
                        self.session_codeP_lineEdit.clear()
                else:
                    self.session_codeP_lineEdit.clear()
                    print('canceled')

                # file_path, _ = QFileDialog.getSaveFileName(caption='حفظ في :', directory='.', filter="text files (*.doc *.docx)")
                # if file_path:
                #     ppdf = Ppdf(self.ordonance, file_path)
            except Exception as e:
                print(e)

            # self.mysqlCurs.execute(f'select max(S_date) from sessions where client_code like "{self.session_codeP_lineEdit.text().split("--")[-1]}"')
            # self.mysqlCurs.execute(f'select ordonance from sessions where S_date like "{self.mysqlCurs.fetchone()[0]}" and client_code like "{self.session_codeP_lineEdit.text().split("--")[-1]}"')
            # data = self.mysqlCurs.fetchall()




        except Exception as e:
            print(e)



    def clear_session_data(self):
        self.diable_checkBox.setChecked(False)
        self.diable_lineEdit.clear()
        self.hta_checkBox.setChecked(False)
        self.hta_lineEdit.clear()
        self.thyroide_checkBox.setChecked(False)
        self.thyroide_lineEdit.clear()
        self.chol_checkBox.setChecked(False)
        self.chol_lineEdit.clear()
        self.anemie_checkBox.setChecked(False)
        self.anemie_lineEdit.clear()
        self.medicaux_autre.clear()
        self.thyoide_checkBox.setChecked(False)
        self.thyoide_lineEdit.clear()
        self.vb_checkBox.setChecked(False)
        self.vb_lineEdit.clear()
        self.amygdale_checkBox.setChecked(False)
        self.amygdale_lineEdit.clear()
        self.pelvienne_checkBox.setChecked(False)
        self.pelvienne_lineEdit.clear()
        self.chirurgicaux_autre.clear()
        self.first_regle_age_lineEdit.clear()
        self.textEdit.clear()
        self.regului_radioButton.setChecked(False)
        self.inregului_radioButton.setChecked(False)
        self.first_rapport_age_lineEdit.clear()
        self.G_lineEdit.clear()
        self.P_lineEdit.clear()
        self.fcs_checkBox.setChecked(False)
        self.fcs_lineEdit.clear()
        self.mfiu_checkBox.setChecked(False)
        self.mfiu_lineEdit.clear()
        self.mort_ne_checkBox.setChecked(False)
        self.mort_ne_lineEdit.clear()
        self.vb_checkBox_2.setChecked(False)
        self.vb_lineEdit_2.clear()
        self.cesarienne_checkBox.setChecked(False)
        self.cesarienne_lineEdit.clear()
        self.ddr_radioButton.setChecked(False)
        self.inpressise_radioButton.setChecked(False)
        self.session_reason_textEdit.clear()
        self.ordononce_treeWidget.clear()
        self.session_price.clear()
        self.session_price_note_textEdit.clear()

    def enable_ordononce_rmv(self):
        try:
            if self.ordononce_treeWidget.selectedItems()[0].text(0):
                self.ordononce_rmv_pushButton.setEnabled(True)
            else:
                self.ordononce_rmv_pushButton.setEnabled(False)
        except Exception as e:
            print(e)

    def rmv_dwa_from_treeView(self):
        # self.ordononce_treeWidget.takeTopLevelItem(self.ordononce_treeWidget.indexOfTopLevelItem(self.ordononce_treeWidget.selectedItems()[0].text(0)))
        # for ix in self.ordononce_treeWidget.selectedIndexes():
        #     text = ix.data(Qt.DisplayRole)  # or ix.data()
        #     print(text)
        for ix in self.ordononce_treeWidget.selectedIndexes():
            # text = ix.data(Qt.DisplayRole)  # or ix.data()
            print(ix)
        rows = [idx.row() for idx in self.ordononce_treeWidget.selectionModel().selectedRows()]
        print(rows[0])  # or return rows
        self.ordononce_treeWidget.takeTopLevelItem(rows[0])

        tt = [self.ordononce_treeWidget.topLevelItem(ix).text(0) for ix in
              range(self.ordononce_treeWidget.topLevelItemCount())]
        print(tt)
        if len(tt) == 0:
            self.ordononce_rmv_pushButton.setEnabled(False)

    def add_dwa_to_treeView(self):
        self.dwa_count += 1
        self.ordononce_treeWidget.addTopLevelItem(QTreeWidgetItem(['--> ' + self.ordononce_EditLine.text()]))
        self.current_dwayat.append(self.ordononce_EditLine.text())
        self.mysqlCurs.execute(f'select dwa_name from dwayat where dwa_name = "{self.ordononce_EditLine.text()}"')
        if not self.mysqlCurs.fetchone():
            self.mysqlCurs.execute(f'insert into dwayat (dwa_name) value ("{self.ordononce_EditLine.text()}") ')
            self.mysqlConn.commit()
        self.ordonoce_refresh(self.model1)
        self.ordononce_EditLine.clear()

    def enable_ordononce_add(self):

        self.mysqlCurs.execute(f'select count(id) from dwayat where dwa_name = "{self.ordononce_EditLine.text()}"')

        if len(self.ordononce_EditLine.text()) < 2 or self.mysqlCurs.fetchone()[
            0] > 1 or self.ordononce_EditLine.text() in self.current_dwayat:
            self.ordononce_add_pushButton.setEnabled(False)
        else:
            self.ordononce_add_pushButton.setEnabled(True)

    def handler(self):
        if self.numbersTree.selectedItems()[0].text(1):
            print(self.numbersTree.selectedItems()[0].text(1))
            self.mysqlCurs.execute('select F_name, L_name, cne, codeP from person where codeP = "{}"'.format(
                self.numbersTree.selectedItems()[0].text(1)))
            F_name, L_name, cne, codeP = self.mysqlCurs.fetchone()
            self.goSes(F_name + ' ' + L_name + '--' + cne + '--' + codeP)

    def goSes(self, codeP):
        self.showSessionsForm()
        self.session_codeP_lineEdit.setText(str(codeP))

    def getData(self, m):
        self.mysqlCurs.execute('select F_name, L_name, cne, codeP from person')
        dt = []
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
            self.mysqlCurs.execute(
                'select max(num) from nums where token_date like "{}"'.format(self.today.split(' ')[0]))
            last = self.mysqlCurs.fetchone()[0]
            if last:
                self.mysqlCurs.execute(
                    'insert into nums (num, client_code, token_date) values ({}, "{}", "{}")'.format(last + 1,
                                                                                                     self.nums_combo.currentText().split(
                                                                                                         ' ')[0],
                                                                                                     self.today.split(
                                                                                                         ' ')[0]))
            else:
                self.mysqlCurs.execute(
                    'insert into nums (num, client_code, token_date) values ({}, "{}", "{}")'.format(1,
                                                                                                     self.nums_combo.currentText().split(
                                                                                                         ' ')[0],
                                                                                                     self.today.split(
                                                                                                         ' ')[0]))

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




    def newRdvFill(self):
        self.mysqlCurs.execute('select codeP from person')
        current_client = [i[0] for i in self.mysqlCurs.fetchall()]
        if self.clientListcombo.currentText() == 'choisir un client' or str(self.clientListcombo.currentText().split(' ')[0]) not in current_client:
            self.newRDVF_name.setText('')
            self.newRDVL_name.setText('')
            self.newRDVtel.setText('')
            self.newRDVAddress.setText('')
            self.newRDVAssir.setText('')
            self.newRDVLast_visit.setText('')

        else:
            self.mysqlCurs.execute(f'''select F_name, L_name, tel, address, assirance from person where codeP = "{str(self.clientListcombo.currentText().split(' ')[0])}" ''')
            cl_info = self.mysqlCurs.fetchone()

            self.newRDVF_name.setText(str(cl_info[0]))
            self.newRDVL_name.setText(str(cl_info[1]))
            self.newRDVtel.setText(str(cl_info[2]))
            self.newRDVAddress.setText(str(cl_info[3]))
            self.newRDVAssir.setText(str(cl_info[4]))

            self.mysqlCurs.execute(f'select max(S_date) from sessions where id = "{str(self.clientListcombo.currentText().split(" ")[0])}"')
            self.newRDVLast_visit.setText(self.mysqlCurs.fetchone()[0])


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
        if len(self.lineEdit_16.text().split('-')[0]) > 4 or len(self.lineEdit_16.text().split('-')[1]) > 2 or len(
                self.lineEdit_16.text().split('-')[2]) > 2:
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
            self.lineEdit_22.setText('')
            self.textEdit_2.setText('')

        else:
            try:
                self.mysqlCurs.execute(f'''select cne, F_name, L_name, sex, 
                    birth_date, address, tel, assirance, family_status, childs, note
                    from person where codeP = "{str(self.comboBox.currentText().split(' ')[0])}" ''')

                client_info = self.mysqlCurs.fetchone()

                print(client_info)

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
                self.lineEdit_2.setText(str(client_info[10]))
                
                self.mysqlCurs.execute('select max(S_date) from sessions where client_code = "{}"'.format(str(self.comboBox.currentText().split(' ')[0])))
                lastV = self.mysqlCurs.fetchone()[0]
                if lastV:
                	self.lineEdit_22.setText(lastV)

            except Exception as e:
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))

    def addPersonCancel(self, event):
        self.codeP.setText('')
        self.F_name.setText('')
        self.L_name.setText('')
        self.cne.setText('')
        self.address.setText('')
        self.tel.setText('')

    def quit_(self):
        is_the_day = self.today.split('-')[2].split(' ')[0] == '01'or self.today.split('-')[2].split(' ')[0] == '10' or self.today.split('-')[2].split(' ')[0] == '20'
        print(self.today.split('-')[2].split(' ')[0])
        if self.bck_done == 0 and is_the_day:
            backup_remander = QMessageBox.information(self, 'buck up remander : ',
                                                      "c'est le meilleur moment pour faire la sauvegarde .",
                                                      QMessageBox.Yes, QMessageBox.No)
            if backup_remander == QMessageBox.Yes:
                self.stt = Setting()
                self.stt.show()
                self.bck_done +=1
            else:
                self.mysqlConn.close()
                self.close()
        else:
            self.mysqlConn.close()
            self.close()

    def logout(self):
        is_the_day = self.today.split('-')[2].split(' ')[0] == '01' or self.today.split('-')[2].split(' ')[0] == '10' or self.today.split('-')[2].split(' ')[0] == '20'
        print(self.today.split('-')[2].split(' ')[0])
        if self.bck_done == 0 and is_the_day:
            backup_remander = QMessageBox.information(self, 'buck up remander : ',
                                                      "c'est le meilleur moment pour faire la sauvegarde .",
                                                      QMessageBox.Yes, QMessageBox.No)
            if backup_remander == QMessageBox.Yes:
                self.stt = Setting()
                self.stt.show()
                self.bck_done += 1
            else:
                self.lg = logIn.LogIn()
                self.lg.show()
                self.close()
        else:
            self.lg = logIn.LogIn()
            self.lg.show()
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
            self.id_P += str(rnd.choice(chars))
            self.id_P += str(rnd.randint(0, 9))
            self.id_P += str(rnd.choice(chars))

        self.id_P += str(rnd.choice(chars))


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

        if data:
            self.numbersTree.setHeaderLabels(['Number', 'ID', 'Name', 'C.N.I', 'Date d\'inscription'])
            for date_ in self.dates:
                ittem = QTreeWidgetItem([date_])
                self.mysqlCurs.execute("""
                    select num, codeP, F_name, L_name, cne, inscri_date 
                                        from person inner join nums on person.codeP = nums.client_code where nums.token_date like '{}' order by num asc""".format(
                    date_))
                for row in self.mysqlCurs.fetchall():
                    child = QTreeWidgetItem(
                        [str(row[0]), str(row[1]), str(row[2]) + ' ' + str(row[3]), str(row[4]), str(row[5])])
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
        self.last_session_price()
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

            self.mysqlCurs.execute(
                "select count(id) from RDV where rdv_date = '{}' ".format(str(self.today.split(' ')[0])))
            self.today_RDV_counter.setText(str(self.mysqlCurs.fetchone()[0]))
            self.mysqlCurs.execute(
                """select count(id) from RDV where rdv_date < '{}' """.format(str(self.today.split(' ')[0])))
            self.time_out_counter.setText(str(self.mysqlCurs.fetchone()[0]))
            self.mysqlCurs.execute(
                """select count(id) from RDV where rdv_date >= '{}' """.format(str(self.today.split(' ')[0])))
            self.rdv_counter.setText(str(self.mysqlCurs.fetchone()[0]))

            self.mysqlCurs.execute('''select person.codeP, person.F_name, person.L_name, person.cne, RDV.rdv_date, RDV.note
            from person inner join RDV on person.codeP = RDV.client_code where RDV.rdv_date >= "{}" order by rdv_date asc'''.format(
                str(self.today.split(' ')[0])))
            for row_number, row_data in enumerate(self.mysqlCurs.fetchall()):
                self.todayRDVTable.insertRow(row_number)
                for col_num, data in enumerate(row_data):
                    if data == '':
                        self.todayRDVTable.setItem(row_number, col_num, QtWidgets.QTableWidgetItem('--------'))
                    else:
                        self.todayRDVTable.setItem(row_number, col_num, QtWidgets.QTableWidgetItem(str(data)))


        except Exception as e:
            print(250, str(e))
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
        try:

            while self.old_RDVTabble.rowCount() > 0:
                self.old_RDVTabble.removeRow(0)

            self.mysqlCurs.execute('''select person.codeP, person.F_name, person.L_name, person.cne, RDV.rdv_date, RDV.note
                        from person inner join RDV on person.codeP = RDV.client_code where rdv_date < "{}" order by rdv_date desc '''.format(
                str(self.today.split(' ')[0])))

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

            self.mysqlCurs.execute(f'select * from person where cne like "{self.cne.text()}"')
            self.is_cne_exists = self.mysqlCurs.fetchone()
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

        elif self.birth_date.date().toPyDate() >= datetime.date.today():
            don = QMessageBox.information(self, 'ERROR DATE', 'la date invalide', QMessageBox.Ok)

        elif self.pdt:
            err = QMessageBox.information(self, 'Alert',
                                          'cette personne existe déjà dans la base de données Sous cette code  '
                                          ': "{}" - ont été inscrits à : "{}"'.format(self.pdt[1], self.pdt[13]),
                                          QMessageBox.Ok)

        elif len(self.cne.text()) < 0 and self.is_cne_exists:
            err = QMessageBox.information(self, 'Alert', f'cette C.N.I existe déjà dans la base de données Sous : "{self.is_cne_exists[1]} {self.is_cne_exists[2]} ({self.is_cne_exists[5]})" - ont été inscrits à : "{self.is_cne_exists[13]}"',QMessageBox.Ok)

        else:
            addPq = """insert into person (codeP, F_name,L_name, birth_date, sex, cne, family_status,childs, address, tel, assirance, working, note, inscri_date, inscri_time )values (
                            '{}', '{}', '{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}' , '{}', '{}') ;"""
            try:
                self.mysqlCurs.execute(addPq.format(self.codeP.text(), self.F_name.text(), self.L_name.text(),
                                                    str(self.birth_date.date().toPyDate()), self.sexe, self.cne.text(),
                                                    str(self.familly_state.currentText()),
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
            except Exception as e:
                print(e)
                err_log = open('src/logs.txt', 'a')
                err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))
                self.err = noInternetAlert.NoInternetAlert()
                self.close()
                self.err.show()
            self.birth_date.setDate(QtCore.QDate.currentDate())

    def getAge(self):
        if self.birth_date.date().toPyDate() <= datetime.date.today():
            self.age_counter.setText(str((datetime.date.today().year - self.birth_date.date().toPyDate().year)))
            print('', datetime.date.today(), ' - ', ' ', self.birth_date.date().toPyDate(), ' = ',
                  datetime.date.today().year - self.birth_date.date().toPyDate().year)
        else:
            # self.birth_date.setDate(QtCore.QDate.currentDate())
            self.age_counter.setText('00')
            don = QMessageBox.information(self, 'ERROR DATE', 'la date invalide', QMessageBox.Ok)
            self.birth_date.setDate(QtCore.QDate.currentDate())

    def go_to_history_specific_session(self):
        # print(self.numbersTree.indexOfTopLevelItem(self.numbersTree.currentItem().parent()))
        # if self.numbersTree.currentItem().parent().text(0):
        #     print(self.numbersTree.currentItem().parent().text(0))
        # try:
        #     if self.treeWidget.currentItem().parent().text(0) and self.treeWidget.currentItem().parent().text(0)[:8] == "Sessions" and str(self.treeWidget.currentItem().text(0)):
        #         print(self.treeWidget.currentItem().parent().text(0))
        #
        #         self.mysqlCurs.execute(
        #             f'select checking from sessions where client_code = "{str(self.treeWidget.currentItem().parent().text(0))}" and S_date = "{str(self.treeWidget.currentItem().text(0))}"')
        #         self.session_save_btn.setEnabled(False)
        #         self.session_history_btn.setEnabled(False)
        #         self.fill_session_data_from_json(self.mysqlCurs.fetchone()[0])
        #
        # except Exception as e:
        #     print(e)
        if self.treeWidget.currentItem().parent() and self.treeWidget.currentItem().parent().text(0)[
                                                      :8] == "Sessions" and str(
                self.treeWidget.currentItem().text(0)):
            print(self.treeWidget.currentItem().parent().parent().text(0), ' --> ',
                  self.treeWidget.currentItem().parent().text(0), ' --> ', self.treeWidget.currentItem().text(0))

            self.mysqlCurs.execute(
                f'select checking, reason, ordonance, price from sessions where client_code = "{str(self.treeWidget.currentItem().parent().parent().text(0))}" and S_date = "{str(self.treeWidget.currentItem().text(0))}"')
            dt = self.mysqlCurs.fetchone()
            print(dt)
            self.session_codeP_lineEdit.clear()
            self.showSessionsForm()
            # self.session_save_btn.setEnabled(False)
            # self.session_history_btn.setEnabled(False)
            # print(self.mysqlCurs.fetchone()[0])
            self.tabWidget.resize(860, 330)
            self.fill_session_data_from_json(dt)
            # self.mysqlConn.commit()

    def session_refresh(self, data=None):

        # self.checkBox.setChecked(False)
        self.dwa_count = 0
        self.current_dwayat = []
        self.ordononce_treeWidget.clear()
        self.current_client_code = self.session_codeP_lineEdit.text().split("--")[-1]
        self.mysqlCurs.execute('''select codeP from person''')
        self.codesP.clear()
        for i in self.mysqlCurs.fetchall():
            self.codesP.append(i[0])

        if self.current_client_code not in self.codesP:
            self.tabWidget.resize(1, 1)
            self.session_save_btn.resize(1, 1)
            self.session_history_btn.resize(1, 1)
        else:
            self.tabWidget.resize(860, 330)
            self.session_save_btn.resize(87, 29)
            self.session_history_btn.resize(87, 29)
            self.mysqlCurs.execute(f'select max(S_date) from sessions where client_code = "{self.current_client_code}"')
            last_visit = self.mysqlCurs.fetchone()[0]
            if last_visit:
                self.mysqlCurs.execute(f'select checking, reason, ordonance, price from sessions where client_code = "{self.current_client_code}" and S_date = "{last_visit}"')
                # checking = json.loads(str(self.mysqlCurs.fetchone()[0]).replace("'", '"'), strict=False)
                self.fill_session_data_from_json(self.mysqlCurs.fetchone())

            #
            # self.mysqlCurs.execute(f'select reason, ordonance, price from sessions where client_code = "{self.current_client_code}" and S_date = "{last_visit}"')
            # dt = self.mysqlCurs.fetchone()
            # self.session_reason_textEdit.setText(dt[0])
            # self.ordononce_treeWidget.clear()
            # if dt:
            #     for i in str(dt[1]).split('---'):
            #         self.ordononce_treeWidget.addTopLevelItem(QTreeWidgetItem([str(i)]))
            #
            # self.session_price.setText(str(dt[2]).split('(')[0])
            # self.session_price_note_textEdit.setText(str(dt[2]).split('(')[1][:-2])

        # except Exception as e:
        #     print(e)
        try:
            self.mysqlCurs.execute(f'select sex from person where codeP = "{self.current_client_code}"')
            sex = self.mysqlCurs.fetchone()[0]
            if sex and sex == 'HOMME':
                self.groupBox_3.setEnabled(False)
                self.groupBox_4.setEnabled(False)
            else:
                self.groupBox_3.setEnabled(True)
                self.groupBox_4.setEnabled(True)

        except Exception as e:
            print(e)

        try:

            self.mysqlCurs.execute(
                f'select count(id) + 1 from sessions where client_code = "{self.current_client_code}"')
            if len(self.session_codeP_lineEdit.text()) > 0:
                self.sessions_counter_label.setText(str(self.mysqlCurs.fetchone()[0]))
        except Exception as e:
            print(e)
        self.ordonoce_refresh(self.model1)

    def fill_session_data_from_json(self, dt):
        if dt:
            print(dt)
            print(dt[0])
            checking = json.loads(str(dt[0]).replace("'", '"'), strict=False)

            if checking["Medicaux"]["Diabele"] != 'n':
                self.diable_checkBox.setChecked(True)
                self.diable_lineEdit.setText(checking["Medicaux"]["Diabele"])

            if checking["Medicaux"]["hta"] != 'n':
                self.hta_checkBox.setChecked(True)
                self.hta_lineEdit.setText(checking["Medicaux"]["hta"])

            if checking["Medicaux"]["Thyroide"] != 'n':
                self.thyroide_checkBox.setChecked(True)
                self.thyroide_lineEdit.setText(checking["Medicaux"]["Thyroide"])

            if checking["Medicaux"]["Chol"] != 'n':
                self.chol_checkBox.setChecked(True)
                self.chol_lineEdit.setText(checking["Medicaux"]["Chol"])

            if checking["Medicaux"]["Anemie"] != 'n':
                self.anemie_checkBox.setChecked(True)
                self.anemie_lineEdit.setText(checking["Medicaux"]["Anemie"])

            if checking["Medicaux"]["Autre"] != 'n':
                self.medicaux_autre.setText(checking["Medicaux"]["Autre"])

            if checking["chirurgicaux"]["Thyoide"] != 'n':
                self.thyoide_checkBox.setChecked(True)
                self.thyoide_lineEdit.setText(checking["chirurgicaux"]["Thyoide"])

            if checking["chirurgicaux"]["vb"] != 'n':
                self.vb_checkBox.setChecked(True)
                self.vb_lineEdit.setText(checking["chirurgicaux"]["vb"])

            if checking["chirurgicaux"]["Amygdales"] != 'n':
                self.amygdale_checkBox.setChecked(True)
                self.amygdale_lineEdit.setText(checking["chirurgicaux"]["Amygdales"])

            if checking["chirurgicaux"]["Pelvienne"] != 'n':
                self.pelvienne_checkBox.setChecked(True)
                self.pelvienne_lineEdit.setText(checking["chirurgicaux"]["Pelvienne"])

            if checking["chirurgicaux"]["Autre"] != 'n':
                self.chirurgicaux_autre.setText(checking["chirurgicaux"]["Autre"])

            if checking["Gyneco"]["first_regle_age"] != 'n':
                self.first_regle_age_lineEdit.setText(checking["Gyneco"]["first_regle_age"])

            if str(checking["Gyneco"]["Cycle_menstruel"][0]) != 'n':
                if str(checking["Gyneco"]["Cycle_menstruel"][0]) == '0':
                    self.regului_radioButton.setChecked(True)
                    self.textEdit.setText(checking["Gyneco"]["Cycle_menstruel"][1:])

                if str(checking["Gyneco"]["Cycle_menstruel"][0]) == '1':
                    self.inregului_radioButton.setChecked(True)
                    self.textEdit.setText(checking["Gyneco"]["Cycle_menstruel"][1:])

            if checking["Gyneco"]["first_rapport_age"] != 'n':
                self.first_rapport_age_lineEdit.setText(checking["Gyneco"]["first_rapport_age"])

            if checking["Gyneco"]["G"] != 'n':
                self.G_lineEdit.setText(checking["Gyneco"]["G"])

            if checking["Gyneco"]["P"] != 'n':
                self.P_lineEdit.setText(checking["Gyneco"]["P"])

            if str(checking["Gyneco"]["fcs"]) != 'n':
                self.fcs_checkBox.setChecked(True)
                self.fcs_lineEdit.setText(checking["Gyneco"]["fcs"])

            if str(checking["Gyneco"]["mfiu"]) != 'n':
                self.mfiu_checkBox.setChecked(True)
                self.mfiu_lineEdit.setText(checking["Gyneco"]["mfiu"])

            if str(checking["Gyneco"]["mort_ne"]) != 'n':
                self.mort_ne_checkBox.setChecked(True)
                self.mort_ne_lineEdit.setText(checking["Gyneco"]["mort_ne"])

            if str(checking["Accauchement"]["vb"]) != 'n':
                self.vb_checkBox_2.setChecked(True)
                self.vb_lineEdit_2.setText(checking["Accauchement"]["vb"])

            if str(checking["Accauchement"]["Cesarienne"]) != 'n':
                self.cesarienne_checkBox.setChecked(True)
                self.cesarienne_lineEdit.setText(checking["Accauchement"]["Cesarienne"])

            if str(checking["Accauchement"]["Grossesse_Actuale"][0]) == '0':
                self.ddr_radioButton.setChecked(True)
                # self.ddr_dateEdit.setDate(int(str(checking["Accauchement"]["Grossesse_Actuale"][1:]).split('-')[0]),
                #                           int(str(checking["Accauchement"]["Grossesse_Actuale"][1:]).split('-')[1]),
                #                           int(str(checking["Accauchement"]["Grossesse_Actuale"][1:]).split('-')[2]))
                self.ddr_dateEdit.setText(str(checking["Accauchement"]["Grossesse_Actuale"][1:]))

            if str(checking["Accauchement"]["Grossesse_Actuale"]) == '1':
                self.inpressise_radioButton.setChecked(True)

        if dt[1]:
            # if 'Auto Ecole' in dt[1]:
            #     # self.checkBox.setChecked(True)

            self.session_reason_textEdit.setText(dt[1])

        if dt[2]:
            for i in str(dt[2]).split('---'):
                self.ordononce_treeWidget.addTopLevelItem(QTreeWidgetItem([i]))

        if dt[3]:
            self.session_price.setText(str(dt[3]).split('(')[0])
            self.session_price_note_textEdit.setText(str(dt[3]).split('(')[1][:-1])

    def ordonoce_refresh(self, m):
        try:
            self.mysqlCurs.execute('select dwa_name from dwayat')
            self.dwayat = [str(i[0]) for i in self.mysqlCurs.fetchall()]
            m.setStringList(self.dwayat)

        except Exception as e:
            print(e)

    def showSessionsForm(self, event=None):
        self.model1 = QStringListModel()
        self.completer_.setModel(self.model1)
        self.ordonoce_refresh(self.model1)
        self.ordononce_EditLine.setCompleter(self.completer_)

        model = QStringListModel()
        self.completer.setModel(model)
        self.getData(model)
        self.session_codeP_lineEdit.setCompleter(self.completer)
        try:
            self.session_refresh()

        except Exception as e:
            print(e)

        self.tabWidget.setCurrentIndex(0)
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

        self.mysqlCurs.execute('select * from RDV where client_code = "{}" and rdv_date ="{}"'.format(
            str(self.clientListcombo.currentText().split(' ')[0]), str(self.newRDVDateEdit.date().toPyDate())))
        if self.clientListcombo.currentText() == 'choisir un client':
            errr = QMessageBox.information(self, 'ERROR', "vous devez d'abord choisir un client", QMessageBox.Ok)
        elif self.newRDVDateEdit.date().toPyDate() <= datetime.date.today():
            errr = QMessageBox.information(self, 'ERROR', "date invalide", QMessageBox.Ok)
        elif self.mysqlCurs.fetchone():
            errr = QMessageBox.information(self, 'ERROR', "this person already have this RDV", QMessageBox.Ok)
        else:
            self.mysqlCurs.execute('''
                insert into RDV (client_code, token_time, rdv_date, note) values(
                    "{}", "{}", "{}", "{}"
                )
                '''.format(str(self.clientListcombo.currentText().split(' ')[0]), self.today.split(' ')[0],
                           str(self.newRDVDateEdit.date().toPyDate()), self.newRDVNote.toPlainText()))
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

    def showDetailsForm(self, event, c=None):

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
        try:
            if c:
                self.lineEdit_51.setText(c)
        except Exception as e:
            print(e)
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


    def statictic(self):
        # self.visits = 0
        # self.cls_incription = 0
        # self.rdvs = 0
        # self.money = 0
        if str(self.dateEdit_2.date().toPyDate()) > str(self.dateEdit_3.date().toPyDate()):
            err = QMessageBox.warning(self, 'ERROR', 'invalid dates ', QMessageBox.Ok)
        else:
            self.statistic_refresh(str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate()))


    def statistic_refresh(self, start_date = None, end_date = None):
        self.ages = []
        self.from_0_to_10 = 0
        self.from_11_to_20 = 0
        self.from_21_to_30 = 0
        self.from_31_to_40 = 0
        self.bigger_than_40 = 0
        self.vistes_times = []
        self.from_7h_to_11h = 0
        self.from_12h_to_15h = 0
        self.from_16h_to_19h = 0
        # self.months = {'01' : 0, '02' : 0, '03' : 0, '04' : 0, '05' : 0, '06' : 0, '07' : 0, '08' : 0, '09' : 0, '10' : 0, '11' : 0, '12' : 0}
        # self.prices = {'jan' : 0, 'feb' : 0, 'mar' : 0, 'apr' : 0, 'may' : 0, 'jun' : 0, 'jul' : 0, 'aug' : 0, 'sep' : 0, 'oct' : 0, 'nov' : 0, 'dec' : 0}

        if start_date and end_date:
            self.mysqlCurs.execute(f"""select count(id) from sessions where S_date > '{str(self.dateEdit_2.date().toPyDate())}' and S_date < '{str(self.dateEdit_3.date().toPyDate())}'""")
            self.visits = self.mysqlCurs.fetchone()[0]
            self.mysqlCurs.execute("""
                    select count(codeP) from person where inscri_date > '{}' and inscri_date < '{}'
                """.format(str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
            self.cls_incription = self.mysqlCurs.fetchone()[0]
            self.mysqlCurs.execute("""
                    select count(id) from RDV where rdv_date > '{}' and rdv_date < '{}' 
                """.format(str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
            self.rdvs = self.mysqlCurs.fetchone()[0]
            self.mysqlCurs.execute("""
                    select sum(price) from sessions where S_date >= '{}' and S_date <= '{}'
                """.format(str(self.dateEdit_2.date().toPyDate()), str(self.dateEdit_3.date().toPyDate())))
            self.money = self.mysqlCurs.fetchone()[0]
            self.mysqlCurs.execute(
                f"""select codeP from sessions inner join person on person.codeP = sessions.client_code where sex like 'HOMME' 
                    and S_date >= '{str(self.dateEdit_2.date().toPyDate())}' and S_date <= '{str(self.dateEdit_3.date().toPyDate())}'""")
            self.males = self.mysqlCurs.fetchall()
            self.mysqlCurs.execute(
                f"""select codeP from sessions inner join person on person.codeP = sessions.client_code where sex like 'FEMME' 
                    and S_date >= '{str(self.dateEdit_2.date().toPyDate())}' and S_date <= '{str(self.dateEdit_3.date().toPyDate())}'""")
            self.females = self.mysqlCurs.fetchall()
            self.mysqlCurs.execute(
                f"""select  client_code, birth_date from sessions inner join person on person.codeP = sessions.client_code where
                        S_date >=  '{str(self.dateEdit_2.date().toPyDate())}' and S_date <= '{str(self.dateEdit_3.date().toPyDate())}'""")
            self.ages =  self.mysqlCurs.fetchall()

            self.mysqlCurs.execute(f'select S_date from sessions where S_date >=  "{str(self.dateEdit_2.date().toPyDate())}" and S_date <= "{str(self.dateEdit_3.date().toPyDate())}" ')
            self.vistes_times = self.mysqlCurs.fetchall()



        else:
            self.mysqlCurs.execute("""select count(id) from sessions""")
            self.visits = self.mysqlCurs.fetchone()[0]
            self.mysqlCurs.execute("""select count(codeP) from person""")
            self.cls_incription = self.mysqlCurs.fetchone()[0]
            self.mysqlCurs.execute("""select count(id) from RDV """)
            self.rdvs = self.mysqlCurs.fetchone()[0]

            # self.mysqlCurs.execute("""select sum(price) from sessions """)
            self.mysqlCurs.execute("""select price from sessions """)
            self.money = 0
            # print(self.mysqlCurs.fetchall())
            for i in self.mysqlCurs.fetchall():
                self.money += int(str(i[0]).split('(')[0])
                # print(int(str(i[0]).split('(')[0]))
            # print(f'money : {self.money}')
            self.mysqlCurs.execute(
                """select codeP from sessions inner join person on person.codeP = sessions.client_code where sex like 'HOMME'""")
            self.males = self.mysqlCurs.fetchall()
            self.mysqlCurs.execute(
                """select codeP from sessions inner join person on person.codeP = sessions.client_code where sex like 'FEMME'""")
            self.females = self.mysqlCurs.fetchall()
            self.mysqlCurs.execute(
                f"""select client_code, birth_date from sessions inner join person on person.codeP = sessions.client_code""")

            self.ages = self.mysqlCurs.fetchall()

            self.mysqlCurs.execute(f'select S_date from sessions')
            self.vistes_times = self.mysqlCurs.fetchall()

        self.mysqlCurs.execute(f'select price, S_date from sessions')
        self.price_and_date_list = self.mysqlCurs.fetchall()


        self.females_count = []
        for i in self.females:
            if i not in self.females_count:
                self.females_count.append(i)

        self.males_count = []
        for i in self.males:
            if i not in self.males_count:
                self.males_count.append(i)


        self.blackList = []
        for c, d in self.ages:
            if c not in self.blackList:
                self.blackList.append(c)
                if 1 <= int(self.today.split('-')[0]) - int(str(d).split('-')[0]) <= 10:
                    self.from_0_to_10 += 1
                if 11 <= int(self.today.split('-')[0]) - int(str(d).split('-')[0]) <= 20:
                    self.from_11_to_20 += 1
                if 21 <= int(self.today.split('-')[0]) - int(str(d).split('-')[0]) <= 30:
                    self.from_21_to_30 += 1
                if 31 <= int(self.today.split('-')[0]) - int(str(d).split('-')[0]) <= 40:
                    self.from_31_to_40 += 1
                if int(self.today.split('-')[0]) - int(str(d).split('-')[0]) > 40:
                    self.bigger_than_40 += 1

        for i in self.vistes_times:
            if 7 <= int(str(i[0]).split(' ')[1].split(':')[0]) <= 11:
                self.from_7h_to_11h += 1

            if 12 <= int(str(i[0]).split(' ')[1].split(':')[0]) <= 15:
                self.from_12h_to_15h += 1

            if 16 <= int(str(i[0]).split(' ')[1].split(':')[0]) <= 19:
                self.from_16h_to_19h += 1

        tt_money = 0
        today_money = 0
        try:
            for p, d in self.price_and_date_list:
                tt_money += int(str(p).split('(')[0])
                if str(d).split(' ')[0] == self.today.split(' ')[0]:
                    today_money += int(str(p).split('(')[0])
        except Exception as e:
            print(e)
        if self.visits:
            self.visites_total.setText(f'Total Visites : {self.visits}')
            self.mysqlCurs.execute('select count(id) from sessions where reason like "%auto ecole%" ')
            tt = self.mysqlCurs.fetchone()[0]

            self.visites_total_2.setText(f'Total Visites por permis : {tt} ( {round((tt / self.visits)*100, 2)} % )')
            if self.males_count:
                self.label_30.setText(f'Hommes : {len(self.males_count)} ( {round((len(self.males_count) / (len(self.males_count) + len(self.females_count))) * 100, 2)} % ).')
            else:
                self.label_30.setText(f'Hommes : 0')
            if self.females_count:
                self.label_44.setText(f'Femmes : {len(self.females_count)} ( {round((len(self.females_count) / (len(self.males_count) + len(self.females_count))) * 100, 2)} % ).')
            else:
                self.label_44.setText(f'Femmes : 0')

            # self.clients_total_2.setText(f'Total client : {self.cls_incription}')
            if self.from_0_to_10:
                self.label_46.setText(f'01 - 10 ans  : {self.from_0_to_10} ( {round ((self.from_0_to_10 / len(self.blackList)) * 100, 2)} % ).')
            else:
                self.label_46.setText(f'01 - 10 ans  : 0')

            if self.from_11_to_20:
                self.label_48.setText(f'11 - 20 ans  : {self.from_11_to_20} ( {round((self.from_11_to_20 / len(self.blackList)) * 100, 2)} % ).')
            else:
                self.label_48.setText(f'11 - 20 ans  : 0')

            if self.from_21_to_30:
                self.label_50.setText(f'21 - 30 ans  : {self.from_21_to_30} ( {round ((self.from_21_to_30 / len(self.blackList)) * 100, 2)} % ).')
            else:
                self.label_50.setText(f'21 - 30 ans  : 0')

            if self.from_31_to_40:
                self.label_53.setText(f'31 - 40 ans  : {self.from_31_to_40} ( {round((self.from_31_to_40 / len(self.blackList)) * 100, 2)} % ).')
            else:
                self.label_53.setText(f'31 - 40 ans  : 0')

            if self.bigger_than_40:
                self.label_54.setText(f' > 40 ans    : {self.bigger_than_40} ( {round((self.bigger_than_40 / len(self.blackList)) * 100, 2)} % ).')
            else:
                self.label_54.setText(f' > 40 ans    : 0')


            if self.from_7h_to_11h:
                self.label_47.setText(f'07h - 11h  : {self.from_7h_to_11h} ( {round ((self.from_7h_to_11h / self.visits) * 100, 2)} % ).')
            else:
                self.label_47.setText(f'07h - 11h  : 0')

            if self.from_12h_to_15h:
                self.label_52.setText(f'12h - 15h  : {self.from_12h_to_15h} ( {round((self.from_12h_to_15h / self.visits) * 100, 2)} % ).')
            else:
                self.label_52.setText(f'12h - 15h  : 0')

            if self.from_16h_to_19h:
                self.label_51.setText(f'16h - 19h    : {self.from_16h_to_19h} ( {round((self.from_16h_to_19h / self.visits) * 100, 2)} % ).')
            else:
                self.label_51.setText(f'16h - 19h    : 0')

            if today_money == 0:
                self.pushButton_8.resize(1, 1)
            else:
                self.pushButton_8.resize(110, 29)

            self.label_57.setText(f'Total : {str(tt_money)} DH .')
            self.label_61.setText(f'Aujourd\'hui : {str(today_money)} DH .')
        else:
            self.visites_total.setText(f'Total Visites : 0')

    def show_money_graph(self):
        bar_graph = Bar_graph(self.price_and_date_list, self.comboBox_years.currentText())

    def show_visites_graph(self):
        visites_graph = Graph('vitors order by gander', [len(self.males_count), len(self.females_count)], ['Homme', 'Femme'], (0.05, 0))

    def show_visites_times_graph(self):
        dt = [self.from_7h_to_11h, self.from_12h_to_15h, self.from_16h_to_19h]
        tm = list((0.01, 0.01, 0.01))
        tm[dt.index(max(dt))] += 0.04
        visites_times_graph = Graph('vitors order by time', dt, ['07h - 11h', '12h - 15h', '16h - 19h'], tuple(tm))

    def show_visites_ages_graph(self):
        dt = [self.from_0_to_10, self.from_11_to_20, self.from_21_to_30, self.from_31_to_40, self.bigger_than_40]
        tm = list((0.01, 0.01, 0.01, 0.01, 0.01))
        tm[dt.index(max(dt))] += 0.04
        visites_ages_graph = Graph('visitors order by age', dt,
                                   ['01 - 10 ans ', '11 - 20 ans ', '21 - 30 ans ', '31 - 40 ans ', ' > 40 ans '], tuple(tm))



    def showStatistiquesForm(self, event):
        self.statistic_refresh()
        # try:
        # except Exception as e:
        #     print(e)
        #     err_log = open('src/logs.txt', 'a')
        #     err_log.write('\n{} {} ( {} )'.format(self.today, str(e), self.acc_type))

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
                            ss = QTreeWidgetItem([session[0], str(session[1]).split('(')[0] + ' Dh'])
                            ch2.addChild(ss)
                            item.addChild(ch2)
                    try:
                        self.mysqlCurs.execute('select price from sessions where client_code like "{}"'.format(i[0]))
                        tt_money = 0
                        for ix in self.mysqlCurs.fetchall():
                            tt_money += int(str(ix[0]).split('(')[0])

                        if tt_money:
                            ch3 = QTreeWidgetItem(['Total money spended : ', '{} DH'.format(str(tt_money))])
                            item.addChild(ch3)
                    except Exception as e:
                        print(e)

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

    def searshDetaisTree(self):
        key = self.lineEdit_51.text()
        if key != '':
            self.treeWidget.clear()
            self.treeWidget.setColumnCount(9)
            self.treeWidget.setHeaderLabels(
                ["code", "prenom", "nom", "C.N.I", "naissance", "S Familier", "adresse", "TEL", "Inscri a"])
            self.mysqlCurs.execute(
                '''select codeP, F_name, L_name, cne, birth_date, family_status, address, tel, inscri_date from person
                 where codeP like "%{}%" or F_name like "%{}%" or L_name like "%{}%" or 
                 cne like "%{}%" or address like "%{}%" or tel like "%{}%" order by F_name asc '''.format(key, key, key,
                                                                                                          key, key,
                                                                                                          key))
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
                        ch2 = QTreeWidgetItem([f'Sessions History : {len(sessions)}'])
                        for session in sessions:
                            ss = QTreeWidgetItem([session[0], str(session[1]).split('(')[0] + ' Dh'])
                            ch2.addChild(ss)
                            item.addChild(ch2)
                    try:
                        self.mysqlCurs.execute('select price from sessions where client_code like "{}"'.format(i[0]))
                        tt_money = 0
                        for ix in self.mysqlCurs.fetchall():
                            tt_money += int(str(ix[0]).split('(')[0])

                        if tt_money:
                            ch3 = QTreeWidgetItem(['Total money spended : ', f'{str(tt_money)} DH'])
                            item.addChild(ch3)
                    except Exception as e:
                        print(e)

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

        else:
            self.detais_refresh()
