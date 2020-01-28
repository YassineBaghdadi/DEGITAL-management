#!/usr / bin / env python
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pyqtgraph.graphicsItems.ScatterPlotItem import tr
from selenium import webdriver 
import time 

# set webdriver path here it may vary
# from selenium.webdriver.chrome import options


class PDF_Printer(QtWidgets.QWidget):
	def __init__(self, path):
		super(PDF_Printer, self).__init__()

		options = webdriver.ChromeOptions()
		# self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', 'PDF files (*.pdf)')[0]
		self.path =  path
		profile = {"plugins.plugins_list": [{"enabled": True, "name": "Chrome PDF Viewer"}]} # Disable Chrome's PDF Viewer
		options.add_experimental_option("prefs", profile)
		try:
			self.brower = webdriver.Chrome(executable_path ="src/chromedriver_V78", chrome_options=options)
		except Exception as e:
			print(e)
			self.brower = webdriver.Chrome(executable_path ="src/chromedriver_V77", chrome_options=options)

		# self.brower.maximize_window()
		# website_URL ="https://www.google.co.in/"
		# website_URL ="file:///home/yassine-baghdadi/works/Desktop/DEGITAL-M.O.Y-Dc-.-management/src/print.pdf"
		self.openPdf()


	def openPdf(self):
		self.brower.get('file://' + str(self.path))
