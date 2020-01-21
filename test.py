import pymysql
import datetime
import random

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

from time import gmtime, strftime


today = str(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
import noInternetAlert
from db_m import DB_m

main_ui,_ = loadUiType(path.join(path.dirname(__file__), "ui/test.ui"))

class Main(QWidget, main_ui):
    def __init__(self, parent = None):
        super(Main, self).__init__(parent)
        QWidget.__init__(self)

        self.setupUi(self)
        # Open database connection
#
        self.db = pymysql.connect("localhost","root","root","MOY" )

        # prepare a cursor object using cursor() method
        self.mysqlCurs = self.db.cursor()
        # self.mysqlCurs.execute('''select person.codeP, person.F_name, person.L_name, person.cne, RDV.rdv_date, RDV.note
        #             from person inner join RDV on person.codeP = RDV.client_code where RDV.rdv_date >= "{}" order by rdv_date asc'''.format(
        #     str(today.split(' ')[0])))
        # print(self.mysqlCurs.fetchall())
#         # self.mysqlCurs.execute("""create table if not exists person (codeP varchar(10) PRIMARY KEY, F_name varchar(20),
#         #                                     L_name varchar(30), birth_date varchar(30) , sex varchar(10), cne varchar(12), family_status varchar (15),
#         #                                     childs int , address varchar(255), tel varchar(20), assirance varchar(255), note text, inscri_date varchar(20))
#         #                                     ENGINE=INNODB default charset = utf8;""")
#         self.mysqlCurs.execute('''select codeP from person''')
#         self.codesP = self.mysqlCurs.fetchall()
#         print(self.codesP)
#         self.mysqlCurs.execute("select count(id) from RDV where rdv_date < '{}' ".format(str(today.split(' ')[0])))
#         print(self.mysqlCurs.fetchone()[0])
#         print(str(today))
#         self.mysqlCurs.execute('select codeP, F_name, L_name, cne, birth_date, family_status, address, tel, inscri_date from person order by F_name asc')
#         for i in self.mysqlCurs.fetchall():
#             print(i)
#         self.mysqlCurs.execute(
#             'select inscri_date from person')
#         print(self.mysqlCurs.fetchall())
#         for i in self.mysqlCurs.fetchall():
#             self.mysqlCurs.execute('update person set inscri_date = "{}"'.format(i[0].split(' ')[0]))
#             self.mysqlCurs.execute('update person set inscri_time = "{}"'.format(i[0].split(' ')[1]))
#             self.db.commit()
        # self.mysqlCurs.execute(
        #     '''select F_name, L_name, tel, address, assirance from person where codeP = "a3pj90V" ''')
        #
        # client_info = self.mysqlCurs.fetchone()
        #
        # print(client_info)

        # self.mysqlCurs.execute('''
        # select codeP, F_name, L_name, cne, max(S_date), note
        # from person inner join sessions on person.codeP = sessions.client_code
        # ''')

        # execute SQL query using execute() method.
        # cursor.execute("insert into stagaires (F_name, L_name, address, filiere) values ('عثمات ', 'chehboun', 'address 1', 'tsdi');")
        # cursor.execute("select count(id) from person")
        # print(cursor.fetchone())
        # self.mysqlCurs.execute('select * from person')
        # dt = self.mysqlCurs.fetchall()
        # print(dt)
        # for row_number, row_data in enumerate(dt):
        #     self.tbl.insertRow(row_number)
        #     for col_num, data in enumerate(row_data):
        #         if data == '':
        #             self.tbl.setItem(row_number, col_num, QtWidgets.QTableWidgetItem(str('-')))
        #         else:
        #             self.tbl.setItem(row_number, col_num, QtWidgets.QTableWidgetItem(str(data)))

        # clients = []
        # self.mysqlCurs.execute('select codeP, F_name, L_name, cne from person')
        # # print(self.mysqlCurs.fetchall())
        # for a in self.mysqlCurs.fetchall():
        #     clients.append(str(a[0]) + ' ' + str(a[1]) + ' ' + str(a[2] + ' ' + str(a[3])))
        #
        # self.comboBox.clear()
        # self.comboBox.addItems(clients)
        # print(clients)
        # self.mysqlCurs.execute('''select F_name, L_name, tel,
        #              address, assirance from person
        #
        #                where person.codeP = "a3pj90V" and person.F_name = "yassine" and person.L_name = "baghdadi" and person.cne = "ttttttt" and sessions.S_date = max(sessions.S_date)''')
        # client_info = self.mysqlCurs.fetchone()
        #
        # print(client_info)

    #
# # Fetch a single row using fetchone() method.r
#
# print (cursor.fetchall())
#
# # disconnect from server
# db.close()

#
# import sqlite3
#
# con = sqlite3.connect('src/setting.db')
# cur = con.cursor()
# cur.execute('select * from tttt')

# from db_m import *
# if DB_m('localhost', 'root', 'root', 'MOY'):
#     print('connected seccessfully')
# else:
#     print('error')

# print(str(open('ss.txt', 'r').readline()).split('.')[0])
# import datetime
# print(str(datetime.datetime.today().date()))
# d = datetime.datetime.today().date()
# print(d + 2020-01-00)
#todo
import random
chars = ['A', 'a', 0, 'B', 'b', 1, 'C', 'c', 2, 'D', 'd', 3, 'E', 'e', 4, 'F', 'f', 5, 'G', 'g', 6, 'H', 'h',
         'I', 'i', 'J', 'j', 7, 'L', 'l', 'M', 'm', 'N', 8, 'n', 'o', 'P', 'p', 'Q', 'q', 'R', 'r', 'S', 's',
         'T', 't', 'U', 'u', 'V', 'v', 'W', 'w', 'X', 'x', 'Y', 'y', 'Z', 'z', 9 ]
# id_ = ''
# for i in range(2):
#     id_+= str(random.choice(chars))
#     id_+= str(random.randint(0, 9))
#     id_+= str(random.choice(chars))
#     if i == 2:
#         id_+= str(random.choice(chars))
#         break


# for i in rr:
#     id_+=str(i)
#
# dates = ['1999-02-12', '2001-05-03', '2002-04-06', '2007-01-09', '2030-07-03', '2000-02-03', '2010-12-03']
#
# tt =[]
# for i in sorted(dates):
#     # print(i)
#     if '2000'<= str(i).split('-')[0] <= '2020':
#         tt.append(i)
#
# print(tt)
# print(sorted(dates))
# import sqlite3
#
# import pymysql
#
# sqliteConn = sqlite3.connect('src/setting.db')
# sqliteCurs = sqliteConn.cursor()
# dt = sqliteCurs.execute('select host, db_user, db_pass, db_name, port from admin_setting').fetchone()
# mysqlConn = pymysql.connect(host=dt[0], user=dt[1], passwd=dt[2], db = dt[3], port = dt[4] )
# mysqlCurs = mysqlConn.cursor()
# # mysqlCurs.execute("""insert into person_1 (codeP, F_name,L_name, birth_date, sex, cne, family_status,childs, address, tel, assirance, note )values (
# #                     'ttsjh6', 'yassine', 'baghdadi', '1998-08-23', 'h', 'kjhkh', 'kjhgkjg', 0, 'kjkjg', 'kjhkjh', 'khkj', 'lkjlk') ;""")
# #
# mysqlConn.commit()
# yy = []
# if yy:
#     print('yes')
# #
# #
# from time import gmtime, strftime
# print(str(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
#
names = ['yassine', 'med', 'otman', 'baghdadi', 'jilli', 'Aahron',
'Aakash','Aalam','Aamer','Aaren','Aarin','Aaron','Aaronn','Aarron',
'Aaryn','Abad','Abalard','Aban','Abba','Abban','Abbas','Abbe','Abbey',
         'Abbie','Abboid','Abbot','Abbott','Abby','Abdiel','Abdulaziz',
         'Abe','Abednego','Abel','Abelard','Abelardo','Abelhard','Abell',
         'Aberham','Abhay','Abhaya','Abhijeet','Abhijit','Abhiram','Abhor',
         'Abhorson',
'Abie','Abijah','Abilard','Able','Abna','Abnar','Abner','Abnor','Abo','Abra',
         'Abrahaim','Abraham','Abrahame','Abrahamo','Abrahan','Abraheem','Abrahem',
         'Abrahim','Abrahm','Abrahon','Abrahsa','Abram','Abramo','Absalon','Abselon',
         'Absolom','Absolum','Abtin','Abuna','Acacio','Ace','Acer',
]

con = sqlite3.connect('src/test.db')
cur = con.cursor()
# cur.execute('create table if not exists test ( name text, age int,  note text)')
# con.commit()
# note = ''
# for i in range(1, 101):
#     for j in range(20):
#         note += str(random.choice(chars))
#     cur.execute('insert into test values ("{}", {}, "{}")'.format(random.choice(names), random.randint(16, 70), note))
#     note = ''
#     con.commit()
#     print('row number {} added successfully'.format(str(i)))

# print(cur.execute('select name from test').fetchall())
# for i in cur.execute('select name from test').fetchall():
#     print(i[0])
# print(cur.execute('select host, db_user, db_pass, db_name, port from admin_setting').fetchone())

#
# ii = ''
# login_logs_file = open('src/login_logs.txt', 'r')
# for i in login_logs_file.readlines():
#     ii += i

# print(ii)

print(today.split(' ')[0])

















def main():
    app = QtWidgets.QApplication(sys.argv)
    main_wn = Main()
    main_wn.show()
    sys.exit(app.exec_())
if __name__ == '__main__' :
    main()

