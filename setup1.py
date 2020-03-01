from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('index.py', base=base, targetName = 'DocManager')
]

setup(name='DocManager - by SoftMOY',
      version = '0.1',
        options = {
		'build_exe':{
			'packages':[ 'sqlite3', 'socket', 'random', 'pyqtgraph', 'pymysql', 'textwrap', 'reportlab'],
				'include_files':['icon.ico', 'about.py', 'admin_settings.py', 'back_up.py', 'bilan.py',
				'create_pdf.py', 'db_m.py', 'graph.py', 'logIn.py', 'main.py', 'noInternetAlert.py',
				'pdf_printer.py', 'setting.py', 'ss.txt', 'test.py', 'test_1.py', 'test_2.py', 'test_3.py', 'ttt.png',
				'img', 'src', 'ui']
				}
			},
      description = 'An Doctor manager app made by SoftMOY',
      options = dict(build_exe = buildOptions),
      executables = executables)
