#Import FPDF class
import textwrap
from time import strftime, gmtime

from fpdf import FPDF
# Create instance of FPDF class
from reportlab.lib.enums import TA_CENTER

from reportlab.lib.pagesizes import A5, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus.para import Paragraph
from emoji import emojize

class Ppdf:
    def __init__(self, ordonance):
        from reportlab.pdfgen import canvas
        self.pdf_ = canvas.Canvas('src/myfile.pdf', pagesize=A5)
        width, height = A5
        print(A5)

        self.today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        self.pdf_.setLineWidth(.3)
        self.yy = 450
        self.data = []
        self.DR_name = 'Dr. Fatima Zahra Moumen'
        self.DR_role = 'Médecine Générale'
        self.city = 'Guercif'
        self.client_info = ['codeP', 'yassine', 'baghdadi', 22 ]
        self.adress = 'hay hamria Guercif'
        self.tele = '06.30.50.46.06'
        self.codeP = 'thsg753'


        self.DR_studies = 'Laureat de la faculte de medecine et de pharmacie - Fes, Diplome en gynecologie suivie de grossesse et infertilite de la faculte de bordeau - France, echographie - Elechogardigramme agrement de delivre les certificats d\'aptitude pour permis de conduite.'
        # for o in range(50):
        #     self.DR_studies += str(o) + ','
        #     if o % 5 == 0:
        #         self.DR_studies += ' '
        # print(len(self.DR_studies))
        #
        #

        # for i in ordonance.split('\n'):
        #     self.data.append(str(self.yy) + '|' + str(i) )
        #     if self.yy == 60:
        #         self.yy = 460
        #     else:
        #         self.yy -= 30

        # print('the data :')
        # print(self.data)
        self.trass()
        # for i in self.data:
        #     if int(i.split('|')[0]) == 60:
        #         self.pdf_.
        #     self.pdf_.drawString(40, int(i.split('|')[0]), i.split('|')[1])

        #
        # self.pdf_.showPage()
        # for font in self.pdf_.getAvailableFonts():
        #     print(font)
            # self.pdf_.setFont(font, 11)
        #     self.pdf_.drawString(140, self.yy, 'this is the "{}" font '.format(font))
        #     self.yy -= 15
        # self.yy = 415
        # self.pdf_.setFont('Helvetica', 11)
        # for i in ordonance.split('\n'):
        #     if i == '':
        #         print('')
        #     else:
        #         self.pdf_.drawString(40, self.yy,'-> ' +  str(i))
        #         if self.yy <= 50:
        #             self.yy = 415
        #             self.pdf_.showPage()
        #         else:
        #             self.yy -= 25


        self.pdf_.save()

    def trass(self):

        self.pdf_.setFont('Helvetica-Bold', 13)
        self.pdf_.drawString(140, 560, self.DR_name)

        self.pdf_.setFont('Courier-BoldOblique', 9)
        self.pdf_.drawString(178, 545, self.DR_role)
        self.pdf_.line(182, 535, 267, 535)

        # if len(self.DR_studies) > 25:
        #     self.yco = 520
        #     for i in textwrap.wrap(self.DR_studies, width=26, alignment=TA_CENTER):
        #     # wrap_text = textwrap.wrap(self.DR_studies, width=45)
        #         self.pdf_.drawString(155, self.yco, i)
        #         self.yco -= 15
        #     self.yco = 520
        # else:
        #     self.pdf_.drawString(155, 520, self.DR_studies)

        self.pdf_.line(182, 535, 267, 535)
        message_style = ParagraphStyle('Normal', alignment=TA_CENTER, fontName='Courier-BoldOblique', fontSize=7, leading=9.6)
        # message = self.DR_studies.replace('\n', '<br />')
        message = Paragraph(self.DR_studies, style=message_style)
        w, h = message.wrap(145, 90)

        message.drawOn(self.pdf_, 155, 530 - h)

        self.pdf_.line(182, 450, 267, 450)

        self.pdf_.setFont('Courier-BoldOblique', 7)
        self.pdf_.drawString(12, 580, self.city + ', le : ' + self.today.split(' ')[0])
        self.pdf_.drawString(120, 438, 'Nom et Prénom : ' + str(self.client_info[1])+ ' ' + str(self.client_info[2]) + ', `#{' + self.codeP + '} ' +  ', Age : ' + str(self.client_info[3]) + ' ans. ')

        self.pdf_.line(30, 430, 380, 430)


        self.pdf_.line(30, 35, 380, 35)

        self.pdf_.drawString(50, 18,  str(self.adress)+ ' - ' + str(self.city) + ' | Tel : ' + str(self.tele))

        # self.pdf_.drawString(420, 580, 'x420')
        # self.pdf_.drawString(400, 580, 'x400')
        # self.pdf_.drawString(380, 580, "x380")
        # self.pdf_.drawString(360, 580, "x360")
        # self.pdf_.drawString(340, 580, "x340")
        # self.pdf_.drawString(320, 580, "x320")
        # self.pdf_.drawString(300, 580, "x300")
        # self.pdf_.drawString(280, 580, "x280")
        # self.pdf_.drawString(260, 580, "x260")
        # self.pdf_.drawString(240, 580, "x240")
        # self.pdf_.drawString(220, 580, "x220")
        # self.pdf_.drawString(200, 580, "x200")
        # self.pdf_.drawString(180, 580, "x180")
        # self.pdf_.drawString(160, 580, "x160")
        # self.pdf_.drawString(140, 580, "x140")
        # self.pdf_.drawString(120, 580, "x120")
        # self.pdf_.drawString(100, 580, "x100")
        # self.pdf_.drawString(80, 580, "x80")
        # self.pdf_.drawString(60, 580, "x60")
        # self.pdf_.drawString(40, 580, "x40")
        # self.pdf_.drawString(20, 580, "x20")
        # self.pdf_.drawString(00, 580, "x00")
        #
        # self.pdf_.drawString(10, 580, 'y580')
        # self.pdf_.drawString(10, 560, 'y560')
        # self.pdf_.drawString(10, 540, 'y540')
        # self.pdf_.drawString(10, 520, 'y520')
        # self.pdf_.drawString(10, 500, 'y500')
        # self.pdf_.drawString(10, 480, 'y480')
        # self.pdf_.drawString(10, 460, 'y460')
        # self.pdf_.drawString(10, 440, 'y440')
        # self.pdf_.drawString(10, 420, 'y420')
        # self.pdf_.drawString(10, 400, 'y400')
        # self.pdf_.drawString(10, 380, "y380")
        # self.pdf_.drawString(10, 360, "y360")
        # self.pdf_.drawString(10, 340, "y340")
        # self.pdf_.drawString(10, 320, "y320")
        # self.pdf_.drawString(10, 300, "y300")
        # self.pdf_.drawString(10, 280, "y280")
        # self.pdf_.drawString(10, 260, "y260")
        # self.pdf_.drawString(10, 240, "y240")
        # self.pdf_.drawString(10, 220, "y220")
        # self.pdf_.drawString(10, 200, "y200")
        # self.pdf_.drawString(10, 180, "y180")
        # self.pdf_.drawString(10, 160, "y160")
        # self.pdf_.drawString(10, 140, "y140")
        # self.pdf_.drawString(10, 120, "y120")
        # self.pdf_.drawString(10, 100, "y100")
        # self.pdf_.drawString(10, 80, "y80")
        # self.pdf_.drawString(10, 60, "y60")
        # self.pdf_.drawString(10, 40, "y40")
        # self.pdf_.drawString(10, 20, "y20")
        # self.pdf_.drawString(10, 00, "y00")

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
f =''
for i in open('src/login_logs.txt', 'r').readlines():
    f += str(i)
w = Ppdf(f)