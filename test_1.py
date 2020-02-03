# import sys
#
# from PyQt5 import QtWidgets, QtCore, QtPrintSupport
#
#
# class Window(QtWidgets.QWidget):
#     def __init__(self):
#         super(Window, self).__init__()
#         self.setWindowTitle('Document Printer')
#         self.editor = QtWidgets.QTextEdit(self)
#         self.editor.textChanged.connect(self.handleTextChanged)
#         self.buttonOpen = QtWidgets.QPushButton('Open', self)
#         self.buttonOpen.clicked.connect(self.handleOpen)
#         self.buttonPrint = QtWidgets.QPushButton('Print', self)
#         self.buttonPrint.clicked.connect(self.handlePrint)
#         self.buttonPreview = QtWidgets.QPushButton('Preview', self)
#         self.buttonPreview.clicked.connect(self.handlePreview)
#         layout = QtWidgets.QGridLayout(self)
#         layout.addWidget(self.editor, 0, 0, 1, 3)
#         layout.addWidget(self.buttonOpen, 1, 0)
#         layout.addWidget(self.buttonPrint, 1, 1)
#         layout.addWidget(self.buttonPreview, 1, 2)
#         self.handleTextChanged()
#
#     def handleOpen(self):
#         path = QtWidgets.QFileDialog.getOpenFileName(
#             self, 'Open file', '',
#             'HTML files (*.html);;Text files (*.txt)')[0]
#         if path:
#             print(path)
#             file = QtCore.QFile(path)
#             if file.open(QtCore.QIODevice.ReadOnly):
#                 stream = QtCore.QTextStream(file)
#                 text = stream.readAll()
#                 info = QtCore.QFileInfo(path)
#                 if info.completeSuffix() == 'html':
#                     self.editor.setHtml(text)
#                 else:
#                     self.editor.setPlainText(text)
#                 file.close()
#
#     def handlePrint(self):
#         dialog = QtPrintSupport.QPrintDialog()
#         if dialog.exec_() == QtWidgets.QDialog.Accepted:
#             self.editor.document().print_(dialog.printer())
#
#     def handlePreview(self):
#         dialog = QtPrintSupport.QPrintPreviewDialog()
#         dialog.paintRequested.connect(self.editor.print_)
#         dialog.exec_()
#
#     def handleTextChanged(self):
#         enable = not self.editor.document().isEmpty()
#         self.buttonPrint.setEnabled(enable)
#         self.buttonPreview.setEnabled(enable)
#
# if __name__ == '__main__':
#
#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.resize(560, 700)
#     window.show()
#     sys.exit(app.exec_())



# t = 'test- '
# print(t.split('-'))
import json
session_json_data = {[{
            "Medicaux":{"Diabele":"n","hta":"n","Thyroide":"n","Cholesterolemie":"n","Anemie":"n","Autre":"n"}},{"chirurgicaux":{"Thyoide":"n","vb":"n","Amygdales":"n","Pelvienne":"n","Autre":"n"}}, {"Gyneco":{"first_regle_age":"n","Cycle_menstruel":"n","first_rapport_age":"n","G":"n","P":"n","fcs":"n","mfiu":"n","mort_ne":"n"}}, {"Accauchement":{"vb":"n","Cesarienne":"n","Grossesse_Actuale":"n"}}]}

# ss = session_json_data.replace("True", "true")
# dd = json.loads(ss)
# print(dd)
# {key:value mapping}
x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert into JSON:
y = json.dumps(session_json_data, indent=4)

# the result is a JSON string:
print(y["Medicaux"])