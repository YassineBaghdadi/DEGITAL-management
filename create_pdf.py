import os
import platform
import textwrap
from os import path
from time import strftime, gmtime

from PyQt5.QtWidgets import QFileDialog
from PyQt5.uic import loadUiType
from fpdf import FPDF
# Create instance of FPDF class
from reportlab.lib.enums import TA_CENTER

from reportlab.lib.pagesizes import A5, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus.para import Paragraph
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog
from pyqtgraph.graphicsItems.ScatterPlotItem import tr
from selenium import webdriver
import time

from reportlab.pdfgen import canvas
from PIL import Image
class Ppdf:
    def __init__(self, client = 'Nom Prenom', age = 'age', ordonance =None, DR_info = ['adress', 'city', '06.30.50.46.06'] , path = None, blink_page = False):
        self.blink_page = blink_page
        self.date_ = str(strftime("%d-%m-%Y %H:%M", gmtime()))
        self.client = client
        self.age = age
        self.pdf_ = canvas.Canvas(path, pagesize=A5)


        self.page_width, self.page_height = A5
        # print(f'A5 width : {width}')
        # print(f'A5 height : {height}')
        # print(A5)

        self.pdf_.setLineWidth(2)
        self.data = []
        # self.DR_name = 'Dr. Fatima Zahra Moumen'
        # self.DR_role = 'Médecine Générale'
        self.adress = DR_info[0]
        self.city = DR_info[1]
        # self.client_info = ['codeP', 'yassine', 'baghdadi', 22 ]
        self.tele = DR_info[2]



        self.DR_studies = 'Laureat de la faculte de medecine et de pharmacie - Fes, Diplome en gynecologie suivie de grossesse et infertilite de la faculte de bordeau - France, echographie - Elechogardigramme agrement de delivre les certificats d\'aptitude pour permis de conduite.'
            # for o in range(50):
            #     self.DR_studies += str(o) + ','
            #     if o % 5 == 0:
            #         self.DR_studies += ' '
            # print(len(self.DR_studies))
            #
            #
        # todo self.trass()

        self.head_img = Image.open('img/head.jpeg')
        # self.yy = self.page_height - self.head_img.size[1]
        self.yy = 380

        if blink_page:#todo set image as header

                self.draw_head()
                #todo
                #
                # ##############################
                # self.pdf_.setFont('Helvetica-Bold', 13)
                # self.pdf_.drawString(140, 560, self.DR_name)
                #
                # self.pdf_.setFont('Courier-BoldOblique', 9)
                # self.pdf_.drawString(178, 545, self.DR_role)
                # self.pdf_.line(182, 535, 267, 535)
                #
                # # if len(self.DR_studies) > 25:
                # #     self.yco = 520
                # #     for i in textwrap.wrap(self.DR_studies, width=26, alignment=TA_CENTER):
                # #     # wrap_text = textwrap.wrap(self.DR_studies, width=45)
                # #         self.pdf_.drawString(155, self.yco, i)
                # #         self.yco -= 15
                # #     self.yco = 520
                # # else:
                # #     self.pdf_.drawString(155, 520, self.DR_studies)
                #
                # self.pdf_.line(182, 535, 267, 535)
                # message_style = ParagraphStyle('Normal', alignment=TA_CENTER, fontName='Courier-BoldOblique',
                #                                fontSize=7, leading=9.6)
                # # message = self.DR_studies.replace('\n', '<br />')
                # message = Paragraph(self.DR_studies, style=message_style)
                # w, h = message.wrap(145, 90)
                #
                # message.drawOn(self.pdf_, 155, 530 - h)
                #
                # self.pdf_.line(182, 450, 267, 450)
                #
                # self.pdf_.setFont('Courier-BoldOblique', 7)
                # self.pdf_.drawString(12, 580, self.city + ', le : ' + self.today.split(' ')[0])
                # self.pdf_.drawString(120, 438, 'Nom et Prénom : ' + str(self.client_info[1]) + ' ' + str(
                #     self.client_info[2]) + ', `#{' + self.codeP + '} ' + ', Age : ' + str(
                #     self.client_info[3]) + ' ans. ')
                #
                # self.pdf_.line(30, 430, 380, 430)

                #########################################
                #
                # self.pdf_.line(30, 35, 380, 35)
                #
                # self.pdf_.drawString(50, 18, str(self.adress) + ' - ' + str(self.city) + ' | Tel : ' + str(self.tele))

            # for i in str(ordonance).split('---'):
            #     self.data.append(str(self.yy) + '|' + str(i))
            #     if self.yy == 60:
            #         self.yy = 460
            #     else:
            #         self.yy -= 30

            # self.trass()
            # for i in self.data:
            #     if i != '':
            #         self.pdf_.drawString(40, i)

            #
            # self.pdf_.showPage()
        # for font in self.pdf_.getAvailableFonts():
        #         print(font)
        #         self.pdf_.setFont(font, 11)
        #         self.pdf_.drawString(140, self.yy, 'this is the "{}" font '.format(font))
        #         self.yy -= 15



        self.draw_footer()
        self.pdf_.setFont('Courier-Bold', 12)
        for i in str(ordonance).split('---'):
                if i :
                    self.pdf_.drawString(40, self.yy, str(i))

                    if self.yy <= 60:
                        self.yy = 380
                        self.pdf_.showPage()
                        self.draw_head()
                        self.draw_footer()
                        self.pdf_.setFont('Courier-Bold', 12)
                    else:
                        self.yy -= 25


        self.pdf_.save()
        options = webdriver.ChromeOptions()
        # self.path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', 'PDF files (*.pdf)')[0]
        self.path = path
        profile = {
            "plugins.plugins_list": [{"enabled": True, "name": "Chrome PDF Viewer"}]}  # Disable Chrome's PDF Viewer
        options.add_experimental_option("prefs", profile)
        self.brower = None
        try:
            try:
                self.brower = webdriver.Chrome(executable_path= os.path.dirname(os.path.realpath(__file__)) + '/src/chromedriver_V78', chrome_options=options)
            except Exception as e:
                print(e)
                self.brower = webdriver.Chrome(executable_path= os.path.dirname(os.path.realpath(__file__)) + '/src/chromedriver_V77', chrome_options=options)
            print(f'your OS is : {platform.system()}')

        except Exception as e:
            print(e)
            self.brower = webdriver.Chrome(executable_path=os.path.dirname(os.path.realpath(__file__)) + '/src/chromedriver.exe', chrome_options=options)

        # try:
        # except Exception as e:
        #     print(e)
            # self.brower = webdriver.Chrome(executable_path="src/chromedriver_V77", chrome_options=options)

        # self.brower.maximize_window()
        # website_URL ="https://www.google.co.in/"
        # website_URL ="file:///home/yassine-baghdadi/works/Desktop/DEGITAL-M.O.Y-Dc-.-management/src/print.pdf"

        self.brower.get('file://' + str(self.path))

    def draw_head(self):
        self.pdf_.setFont('Courier', 9)
        self.pdf_.drawImage('img/head.jpeg', 0, self.page_height - 180, 420, 180)
        self.pdf_.drawString(140, 420, f'Guercif, le : {self.date_} ')
        self.pdf_.drawString(100, 410, f'Client : {self.client}, Age : {self.age} ans .')


    def draw_footer(self):
        self.pdf_.setFont('Courier', 9)

        self.pdf_.line(30, 35, 380, 35)

        self.pdf_.drawString(50, 18, str(self.adress) + ' - ' + str(self.city) + ' | Tel : ' + str(self.tele))
        self.pdf_.drawString(400, 8,str(self.pdf_.getPageNumber()))


    # def get_path(self):
    #     return QFileDialog.getSaveFileName(caption='حفظ في :', directory='.', filter="text files (*.doc *.docx)")

    def trass(self):

        self.pdf_.drawString(420, 400, 'x420')
        self.pdf_.drawString(400, 400, 'x400')
        self.pdf_.drawString(380, 400, "x380")
        self.pdf_.drawString(360, 400, "x360")
        self.pdf_.drawString(340, 400, "x340")
        self.pdf_.drawString(320, 400, "x320")
        self.pdf_.drawString(300, 400, "x300")
        self.pdf_.drawString(280, 400, "x280")
        self.pdf_.drawString(260, 400, "x260")
        self.pdf_.drawString(240, 400, "x240")
        self.pdf_.drawString(220, 400, "x220")
        self.pdf_.drawString(200, 400, "x200")
        self.pdf_.drawString(180, 40, "x180")
        self.pdf_.drawString(160, 400, "x160")
        self.pdf_.drawString(140, 400, "x140")
        self.pdf_.drawString(120, 400, "x120")
        self.pdf_.drawString(100, 400, "x100")
        self.pdf_.drawString(80, 400, "x80")
        self.pdf_.drawString(60, 400, "x60")
        self.pdf_.drawString(40, 400, "x40")
        self.pdf_.drawString(20, 400, "x20")
        self.pdf_.drawString(00, 400, "x00")

        self.pdf_.drawString(10, 580, 'y580')
        self.pdf_.drawString(10, 560, 'y560')
        self.pdf_.drawString(10, 540, 'y540')
        self.pdf_.drawString(10, 520, 'y520')
        self.pdf_.drawString(10, 500, 'y500')
        self.pdf_.drawString(10, 480, 'y480')
        self.pdf_.drawString(10, 460, 'y460')
        self.pdf_.drawString(10, 440, 'y440')
        self.pdf_.drawString(10, 420, 'y420')
        self.pdf_.drawString(10, 400, 'y400')
        self.pdf_.drawString(10, 380, "y380")
        self.pdf_.drawString(10, 360, "y360")
        self.pdf_.drawString(10, 340, "y340")
        self.pdf_.drawString(10, 320, "y320")
        self.pdf_.drawString(10, 300, "y300")
        self.pdf_.drawString(10, 280, "y280")
        self.pdf_.drawString(10, 260, "y260")
        self.pdf_.drawString(10, 240, "y240")
        self.pdf_.drawString(10, 220, "y220")
        self.pdf_.drawString(10, 200, "y200")
        self.pdf_.drawString(10, 180, "y180")
        self.pdf_.drawString(10, 160, "y160")
        self.pdf_.drawString(10, 140, "y140")
        self.pdf_.drawString(10, 120, "y120")
        self.pdf_.drawString(10, 100, "y100")
        self.pdf_.drawString(10, 80, "y80")
        self.pdf_.drawString(10, 60, "y60")
        self.pdf_.drawString(10, 40, "y40")
        self.pdf_.drawString(10, 20, "y20")
        self.pdf_.drawString(10, 00, "y00")

#
# class Create_PDF(FPDF):
#     def __init__(self):
#
#         # Add new page. Without this you cannot create the document.
#         super().__init__()
#
#         # ###################################
#         # Help
#         def drawMyRuler(pdf):
#             pdf.drawString(100, 810, 'x100')
#             pdf.drawString(200, 810, 'x200')
#             pdf.drawString(300, 810, 'x300')
#             pdf.drawString(400, 810, 'x400')
#             pdf.drawString(500, 810, 'x500')
#
#             pdf.drawString(10, 100, 'y100')
#             pdf.drawString(10, 200, 'y200')
#             pdf.drawString(10, 300, 'y300')
#             pdf.drawString(10, 400, 'y400')
#             pdf.drawString(10, 500, 'y500')
#             pdf.drawString(10, 600, 'y600')
#             pdf.drawString(10, 700, 'y700')
#             pdf.drawString(10, 800, 'y800')
#
#             # ###################################
#
#         # Content
#         fileName = 'MyDoc.pdf'
#         documentTitle = 'Document title!'
#         title = 'Tasmanian devil'
#         subTitle = 'The largest carnivorous marsupial'
#
#         textLines = [
#             'The Tasmanian devil (Sarcophilus harrisii) is',
#             'a carnivorous marsupial of the family',
#             'Dasyuridae.'
#         ]
#
#         image = 'tasmanianDevil.jpg'
#
#         # ###################################
#         # 0) Create document
#         from reportlab.pdfgen import canvas
#
#         pdf = canvas.Canvas(fileName)
#         pdf.setTitle(documentTitle)
#
#         drawMyRuler(pdf)
#         # ###################################
#         # 1) Title :: Set fonts
#         # # Print available fonts
#         # for font in pdf.getAvailableFonts():
#         #     print(font)
#
#         # Register a new font
#         from reportlab.pdfbase.ttfonts import TTFont
#         from reportlab.pdfbase import pdfmetrics
#
#         # pdfmetrics.registerFont(
#         #     TTFont('abc', 'SakBunderan.ttf')
#         # )
#         # pdf.setFont('abc', 36)
#         pdf.drawCentredString(300, 770, title)
#
#         # ###################################
#         # 2) Sub Title
#         # RGB - Red Green and Blue
#         pdf.setFillColorRGB(0, 0, 255)
#         pdf.setFont("Courier-Bold", 24)
#         pdf.drawCentredString(290, 720, subTitle)
#
#         # ###################################
#         # 3) Draw a line
#         pdf.line(30, 710, 550, 710)
#
#         # ###################################
#         # 4) Text object :: for large amounts of text
#         from reportlab.lib import colors
#
#         text = pdf.beginText(40, 680)
#         text.setFont("Courier", 18)
#         text.setFillColor(colors.red)
#         for line in textLines:
#             text.textLine(line)
#
#         pdf.drawText(text)
#
#         # ###################################
#         # 5) Draw a image
#         # pdf.drawInlineImage(image, 130, 400)
#
#         pdf.save()
#


# w = Create_PDF()

# f ='''
# --> dfssf-----> dddddddd-----> ssssssss-----> ddddddddddd-----> vvvvvvvvvvvv-----> errrrrre---
# --> sssssssss-----> sssssssssssss-----> ssssssssssss-----> svvvvvvvvvv-----> ssssssssssssss-----> sssssssssssssss---
# --> ssssssssssssssssss-----> ssssssssssssssss-----> sssssssssss-----> ssssssssss-----> sssssssssssssssssss-----> dddddddddddd---
# --> eeeeeeeeeee-----> xxxxxxxxxxxxx-----> ssssssssssssssssd-----> ssssssssse-----> wwwwwwwwwwwwww-----> ssssssssssss-----> svvvvvvvvvv-----> ssssssssssssss-----> sssssssssssssss---
# --> ssssssssssssssssss-----> ssssssssssssssss-----> sssssssssss-----> ssssssssss-----> sssssssssssssssssss-----> dddddddddddd---
# --> eeeeeeeeeee-----> xxxxxxxxxxxxx-----> ssssssssssssssssd-----> ssssssssse-----> wwwwwwwwwwwwww-----> ssssssssssss-----> svvvvvvvvvv-----> ssssssssssssss-----> sssssssssssssss---
# --> ssssssssssssssssss-----> ssssssssssssssss-----> sssssssssss-----> ssssssssss-----> sssssssssssssssssss-----> dddddddddddd---
# --> eeeeeeeeeee-----> xxxxxxxxxxxxx-----> ssssssssssssssssd-----> ssssssssse-----> wwwwwwwwwwwwww-----> ssssssssssss-----> svvvvvvvvvv-----> ssssssssssssss-----> sssssssssssssss---
# --> ssssssssssssssssss-----> ssssssssssssssss-----> sssssssssss-----> ssssssssss-----> sssssssssssssssssss-----> dddddddddddd---
# --> eeeeeeeeeee-----> xxxxxxxxxxxxx-----> ssssssssssssssssd-----> ssssssssse-----> wwwwwwwwwwwwww-----> ssssssssssss-----> svvvvvvvvvv-----> ssssssssssssss-----> sssssssssssssss---
# --> ssssssssssssssssss-----> ssssssssssssssss-----> sssssssssss-----> ssssssssss-----> sssssssssssssssssss-----> dddddddddddd---
# --> eeeeeeeeeee-----> xxxxxxxxxxxxx-----> ssssssssssssssssd-----> ssssssssse-----> wwwwwwwwwwwwww
# '''

# ppp = os.path.dirname(os.path.realpath(__file__)) + '/src/ordooooonnnnnnnn.pdf'
# print(ppp)
# # ppp = loadUiType(path.join(path.dirname(__file__), "src/ordooooonnnnnnnn.pdf"))
# # w = Ppdf(ordonance=f.replace('\n', ''), path='src/ordooooonnnnnnnn.pdf', blink_page=True)
# w = Ppdf(ordonance=f.replace('\n', ''), path=ppp, blink_page=True)