
import pymysql
from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *
import os
from os import path
import sys
import sqlite3
import time

import index



adminSetting_win_dir,_ = loadUiType(path.join(path.dirname(__file__), "ui/today_money_details.ui"))


class Today_money_details(QWidget, adminSetting_win_dir):
    def __init__(self, data, parent = None):
        super(Today_money_details, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        item = []
        self.treeWidget.clear()
        for i in data:
            # self.treeWidget.addTopLevelItem(QTreeWidgetItem(i))
            self.treeWidget.addTopLevelItem(QTreeWidgetItem([i[0], i[1], i[2], str(i[3]).split(' ')[1][:-3], i[4]]))