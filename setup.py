import sys, os
import cx_Freeze
import pymysql
import reportlab
from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import *

#from cx_Freeze import setup, Executable
"""
__version__ = "1.1.0"

include_files = ['logging.ini', 'config.ini', 'running.png']
excludes = ["tkinter"]
packages = ["os", "idna", "requests","json","base64","pyodbc"]

setup(
    name = "appname",
    description='App Description',
    version=__version__,
    options = {"build_exe": {
    'packages': packages,
    'include_files': include_files,
    'excludes': excludes,
    'include_msvcr': True,
}},
executables = [Executable("b2b_conn.py",base="Win32GUI")]
)
"""
base = None
if sys.platform == 'win32':
	base = 'Win32GUI'

executables = [cx_Freeze.Executable('index.py', base = base, icon = 'icon.ico')]

cx_Freeze.setup(
	name = 'DocManager',
	options = {
		'build_exe':{
			'packages':[ 'sqlite3', 'socket', 'random', 'pyqtgraph', 'pymysql', 'textwrap', 'reportlab'],
				'include_files':['icon.ico', 'about.py', 'admin_settings.py', 'back_up.py', 'bilan.py',
				'create_pdf.py', 'db_m.py', 'graph.py', 'logIn.py', 'main.py', 'noInternetAlert.py',
				'pdf_printer.py', 'setting.py', 'ss.txt', 'test.py', 'test_1.py', 'test_2.py', 'test_3.py', 'ttt.png',
				'img', 'src', 'ui']
				}
			},
	version = '0.1',
	description = 'app for doctors management made by SoftMOY',
	executables = executables
		
)