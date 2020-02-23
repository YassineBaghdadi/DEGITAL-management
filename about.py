import pipes
from webbrowser import Chrome

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
import os

from selenium.webdriver import Chrome, ChromeOptions
import time
file = os.path.abspath ("src/about/about_us.html")



class About:
    def __init__(self):

        options = ChromeOptions()
        # self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', 'PDF files (*.pdf)')[0]

        profile = {
            "plugins.plugins_list": [{"enabled": True, "name": "Chrome PDF Viewer"}]}  # Disable Chrome's PDF Viewer
        options.add_experimental_option("prefs", profile)
        self.brower = None
        try:
            try:
                self.brower = Chrome(
                    executable_path=os.path.dirname(os.path.realpath(__file__)) + '/src/chromedriver_V78',
                    chrome_options=options)

            except Exception as e:
                print(e)
                self.brower = Chrome(
                    executable_path=os.path.dirname(os.path.realpath(__file__)) + '/src/chromedriver_V77',
                    chrome_options=options)


        except Exception as e:
            print(e)
            self.brower = Chrome(executable_path=os.path.dirname(os.path.realpath(__file__)) + '/src/chromedriver.exe',
                                 chrome_options=options)

        # self.brower = Chrome()

        # try:
        # except Exception as e:
        #     print(e)
        # self.brower = webdriver.Chrome(executable_path="src/chromedriver_V77", chrome_options=options)

        # self.brower.maximize_window()
        # website_URL ="https://www.google.co.in/"
        # website_URL ="file:///home/yassine-baghdadi/works/Desktop/DEGITAL-M.O.Y-Dc-.-management/src/print.pdf"

        self.brower.get('file://' + str(file))
        self.brower.maximize_window()


#
#
if __name__ == '__main__' :
    o = About()
