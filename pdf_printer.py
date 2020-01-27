#!/usr / bin / env python
import sys

from PyQt5 import QtWidgets
from selenium import webdriver 
import time 

# set webdriver path here it may vary
# from selenium.webdriver.chrome import options


class PDF_Printer():
	def __init__(self, path):
		super(PDF_Printer, self).__init__()

		options = webdriver.ChromeOptions()
		self.path =  path
		profile = {"plugins.plugins_list": [{"enabled": True, "name": "Chrome PDF Viewer"}]} # Disable Chrome's PDF Viewer
		options.add_experimental_option("prefs", profile)

		self.brower = webdriver.Chrome(executable_path ="src/chromedriver", chrome_options=options)

		# self.brower.maximize_window()
		# website_URL ="https://www.google.co.in/"
		# website_URL ="file:///home/yassine-baghdadi/works/Desktop/DEGITAL-M.O.Y-Dc-.-management/src/print.pdf"
		self.openPdf()


	def openPdf(self):
		self.brower.get('file://' + self.path)
		# self.brower.find_element_by_xpath("//cr-icon-button[@id ='print']body/viewer-pdf-toolbar/div/div/div/cr-icon-button").click()



if __name__ == '__main__':
	window = PDF_Printer('/home/yassine-baghdadi/works/Desktop/DEGITAL-M.O.Y-Dc-.-management/src/print.pdf')