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


main_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/index.ui"))

class Main(QWidget, main_ui):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.width_ = 871
        self.height_ = 431


        self.home_frame.resize(self.width_, self.height_)

        self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.add_person_btn.mousePressEvent = self.addPersonFrame
        self.add_person_save_btn.setStyleSheet('background-image: url(img/btns/off/save_btn.png);')
        self.add_person_annuler_btn.setStyleSheet('background-image: url(img/btns/off/anuler.png);')


        self.home_icon.mousePressEvent = self.showHomeFrame
        self.home_icon.setStyleSheet('background-image: url(img/btns/house.png);')
        self.setting_btn.setStyleSheet('background-image: url(img/btns/settings.png);')


        self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.RDV_btn.mousePressEvent = self.showRDVFrame

        self.today_RDV_btn.setStyleSheet('background-image: url(img/btns/on/today_rdv_btn.png);')
        self.today_RDV_btn.mousePressEvent = self.showTodayRDVFrame

        self.time_out_RDV_btn.setStyleSheet('background-image: url(img/btns/off/out_rdv_btn.png);')
        self.time_out_RDV_btn.mousePressEvent = self.showTimeOutRDVFrame

        self.new_RDV_btn.setStyleSheet('background-image: url(img/btns/off/add_rdv_btn.png);')
        self.save_new_rdv.setStyleSheet('background-image: url(img/btns/off/save_btn.png);')
        self.annuler_rdv.setStyleSheet('background-image: url(img/btns/off/anuler.png);')
        self.new_RDV_btn.mousePressEvent = self.showNewRDVFrame
        self.save_new_rdv.mousePressEvent = self.saveNewRDV
        # self.annuler_rdv.mousePressEvent = self.annulerNewRDV

        self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.search_btn.mousePressEvent = self.showSearchForm
        self.save_searsh_changes.setStyleSheet('background-image: url(img/btns/off/save_btn.png);')

        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.sessions_btn.mousePressEvent = self.showSessionsForm

        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Ditails_btn.mousePressEvent = self.showDetailsForm

        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.Statistiques_btn.mousePressEvent = self.showStatistiquesForm

        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QImage("img/pack.png")))

        self.setPalette(palette)

        ##### Séance


    def showSessionsForm(self, event):
        pass

    def showHomeFrame(self, event):
        self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.home_frame.resize(self.width_, self.height_)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def addPersonFrame(self, event):
        self.add_person_btn.setStyleSheet('background-image: url(img/btns/on/add_person_btn.png);')
        self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')

        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(self.width_, self.height_)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def showRDVFrame(self, event):
        self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.RDV_btn.setStyleSheet('background-image: url(img/btns/on/RDV_btn.png);')
        self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')

        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(self.width_, self.height_)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def showTodayRDVFrame(self, event):
        self.today_RDV_btn.setStyleSheet('background-image: url(img/btns/on/today_rdv_btn.png);')
        self.time_out_RDV_btn.setStyleSheet('background-image: url(img/btns/off/out_rdv_btn.png);')
        self.new_RDV_btn.setStyleSheet('background-image: url(img/btns/off/add_rdv_btn.png);')
        self.today_RDV_frame.resize(821, 311)
        self.time_out_RDV_frame.resize(1, 1)
        self.new_RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def showTimeOutRDVFrame(self, event):
        self.today_RDV_btn.setStyleSheet('background-image: url(img/btns/off/today_rdv_btn.png);')
        self.time_out_RDV_btn.setStyleSheet('background-image: url(img/btns/on/out_rdv_btn.png);')
        self.new_RDV_btn.setStyleSheet('background-image: url(img/btns/off/add_rdv_btn.png);')
        self.today_RDV_frame.resize(1, 1)
        self.time_out_RDV_frame.resize(821, 311)
        self.new_RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def showNewRDVFrame(self, event):
        self.today_RDV_btn.setStyleSheet('background-image: url(img/btns/off/today_rdv_btn.png);')
        self.time_out_RDV_btn.setStyleSheet('background-image: url(img/btns/off/out_rdv_btn.png);')
        self.new_RDV_btn.setStyleSheet('background-image: url(img/btns/on/add_rdv_btn.png);')
        self.today_RDV_frame.resize(1, 1)
        self.time_out_RDV_frame.resize(1, 1)
        self.new_RDV_frame.resize(821, 311)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def saveNewRDV(self, event):#todo
        # self.save_new_rdv.setStyleSheet('background-image: url(img/btns/on/save_btn.png);')
        # time.sleep(0.05)
        # self.save_new_rdv.setStyleSheet('background-image: url(img/btns/off/save_btn.png);')
        pass

    # def annulerNewRDV(self, event):#todo
    #     # self.annuler_rdv.setStyleSheet('background-image: url(img/btns/on/anuler.png);')
    #     # time.sleep(0.05)
    #     # self.annuler_rdv.setStyleSheet('background-image: url(img/btns/off/anuler.png);')
    #     print('clicked')

    def showSearchForm(self, event):
        self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.search_btn.setStyleSheet('background-image: url(img/btns/on/search_btn.png);')
        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(self.width_, self.height_)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)

    def showDetailsForm(self, event):
        self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/on/detais.png);')
        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/off/statistiques_btn.png);')
        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(self.width_, self.height_)
        ##### Séance
        self.Statistiques_frame.resize(1, 1)




    def showStatistiquesForm(self, event):
        self.add_person_btn.setStyleSheet('background-image: url(img/btns/off/add_person_btn.png);')
        self.RDV_btn.setStyleSheet('background-image: url(img/btns/off/RDV_btn.png);')
        self.search_btn.setStyleSheet('background-image: url(img/btns/off/search_btn.png);')
        self.sessions_btn.setStyleSheet('background-image: url(img/btns/off/seionse_btn.png);')
        self.Ditails_btn.setStyleSheet('background-image: url(img/btns/off/detais.png);')
        self.Statistiques_btn.setStyleSheet('background-image: url(img/btns/on/statistiques_btn.png);')
        self.home_frame.resize(1, 1)
        self.add_person_frame.resize(1, 1)
        self.RDV_frame.resize(1, 1)
        self.search_frame.resize(1, 1)
        self.Ditails_frame.resize(1, 1)
        ##### Séance
        self.Statistiques_frame.resize(self.width_, self.height_)










def main():
    app = QtWidgets.QApplication(sys.argv)
    Sign_in_up_wn = Main()
    Sign_in_up_wn.show()
    sys.exit(app.exec_())


if __name__ == '__main__' :
    main()