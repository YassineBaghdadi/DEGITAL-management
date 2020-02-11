import socket

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



adminSetting_win_dir,_ = loadUiType(path.join(path.dirname(__file__), "ui/AdminSettings.ui"))


class AdminSetting(QWidget, adminSetting_win_dir):
    def __init__(self, parent = None):
        super(AdminSetting, self).__init__(parent)
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowTitle('Setting For Admin')
        self.save.clicked.connect(self.save_)
        self.quit.clicked.connect(self.quit_)
        self.conn = sqlite3.connect('src/setting.db')
        self.cursor = self.conn.cursor()
        self.tst_con.clicked.connect(self.test_con)
        self.today = str(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        self.exic.clicked.connect(self.exicQuiry)
        try:
            self.cursor.execute('select host, db_user, db_pass, port, db_name from admin_setting')
            self.dt = self.cursor.fetchone()
        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n' + self.today + ' '  + str(e))
            self.cursor.execute(
                'create table if not exists admin_setting ( host text, db_user text, db_pass text, port text , db_name text)')
            self.conn.commit()

        try:
            self.db_host.setText(str(self.dt[0]))
            self.db_username.setText(str(self.dt[1]))
            self.db_passwrd.setText(str(self.dt[2]))
            self.db_port.setText(str(self.dt[3]))
            self.db_name.setText(str(self.dt[4]))
            # cursor.execute('select days, serialK from delay where id = 1')
            # dt1 = cursor.fetchone()
            # self.delay.setText(dt1[0])
            # self.serial_key.setText(dt1[1])
        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n' + self.today + ' '  + str(e))
        try:
            logins = '---------------------- logins history ------------------------'
            login_logs_file = open('src/login_logs.txt', 'r')
            for i in login_logs_file.readlines():
                logins += i

            self.login_time.append(logins)

        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n' + self.today + ' '  + str(e))

        try:
            errs = '---------------------- Errors history ------------------------'
            err_log_file = open('src/logs.txt', 'r')
            for i in err_log_file.readlines():
                errs += i

            self.logs_.append(errs)

        except Exception as e:
            print(e)
            err_log = open('src/logs.txt', 'a')
            err_log.write('\n' + self.today + ' '  + str(e))

    def exicQuiry(self):
        self.mysqlconn = pymysql.connect(
                host=self.db_host.text(),
                user=self.db_username.text(),
                passwd=self.db_passwrd.text(),
                db=self.db_name.text(),
                port=int(self.db_port.text())

            )
        self.mysqlCurs = self.mysqlconn.cursor()
        if self.quiryline.text() != '':
            self.mysqlCurs.execute(self.quiryline.text())
            self.login_time.clear()
            self.login_time.append(str(self.mysqlCurs.fetchall()))

        self.mysqlconn.commit()
        self.mysqlconn.close()


    def test_con(self):
        try:
            self.mysqlconn = pymysql.connect(
                host=self.db_host.text(),
                user=self.db_username.text(),
                passwd=self.db_passwrd.text(),
                db=self.db_name.text(),
                port=int(self.db_port.text())

            )
            self.mysqlCurs = self.mysqlconn.cursor()
            success = QMessageBox.question(self, 'info', "connected successfully\nDo you want to create tables right now ?\n",QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if success == QMessageBox.Yes:
                try:

                    self.mysqlCurs.execute('''create database if not exists MOY;''')
                    self.mysqlconn.commit()

                    self.mysqlCurs.execute('''use MOY;''')


                    self.mysqlCurs.execute('''create table if not exists users (id int auto_increment primary key not null, username varchar(30),
                                                                                     passwrd varchar(100), role varchar(20))
                                                                                     ENGINE=INNODB default charset = utf8;''')
                    self.mysqlconn.commit()
                    self.mysqlCurs.execute('select count(id) from users;')
                    if not self.mysqlCurs.fetchone()[0]:
                        self.mysqlCurs.execute('insert into users (username, passwrd, role) values("admin", "admin", "admin");')
                        self.mysqlconn.commit()


                    self.mysqlCurs.execute('''create table if not exists person (codeP varchar(10) PRIMARY KEY, F_name varchar(20),
                                                                 L_name varchar(30), birth_date varchar(30) , sex varchar(10), cne varchar(12), family_status varchar (15),
                                                                 childs int , address varchar(255), tel varchar(20),
                                                                  assirance varchar(255), working varchar(40), note text, inscri_date varchar(20), inscri_time varchar(20))
                                                                 ENGINE=INNODB default charset = utf8;''')
                    self.mysqlconn.commit()
                    self.mysqlCurs.execute('''
                                        create table if not exists RDV (
                                            id int auto_increment primary key not null,
                                             client_code varchar(10), token_time varchar(30), rdv_date varchar(30), note varchar(255),
                                             foreign key (client_code) references person(codeP) ON DELETE CASCADE ) ENGINE=INNODB default charset = utf8;
                                    ''')



                    self.mysqlconn.commit()
                    self.mysqlCurs.execute('''
                                        create table if not exists sessions (
                                        id int auto_increment primary key not null,
                                         client_code varchar(10) ,
                                         S_date varchar(20),
                                         checking text,
                                         price varchar(255),
                                         ordonance varchar(255),
                                         reason text,
                                         foreign key (client_code) references person(codeP) ON DELETE CASCADE ) ENGINE=INNODB default charset = utf8;
                                    ''')

                    self.mysqlconn.commit()
                    # self.mysqlCurs.execute('''
                    #                     create table if not exists checking (
                    #                     id int auto_increment primary key not null,
                    #                      session_id int,
                    #                      Medicaux varchar(255),
                    #                      chirurgicaux varchar(255),
                    #                      Gyneco varchar(255),
                    #                      Accauchement varchar(255)
                    #
                    #                      foreign key (session_id) references sessions(id) ON DELETE CASCADE ) ENGINE=INNODB default charset = utf8;
                    #                 ''')
                    #
                    # self.mysqlconn.commit()
                    #
                    # self.mysqlCurs.execute('''
                    #                     create table if not exists malades (id int auto_increment primary key not null, name varchar(30), type varchar(10) )ENGINE=INNODB default charset = utf8;
                    #                 ''')
                    #
                    #
                    #
                    # self.mysqlconn.commit()
                    self.mysqlCurs.execute('''
                                        create table if not exists nums (id int auto_increment primary key not null, 
                                        num int, 
                                        client_code varchar(12),
                                         token_date varchar(20) ,
                                         foreign key (client_code) references person(codeP) ON DELETE CASCADE)ENGINE=INNODB default charset = utf8;
                                    ''')

                    self.mysqlconn.commit()

                    self.mysqlCurs.execute('''
                                        create table if not exists tools (id int auto_increment primary key not null, st varchar(20))ENGINE=INNODB default charset = utf8;
                                    ''')

                    self.mysqlconn.commit()

                    self.mysqlCurs.execute('''
                                        create table if not exists dwayat (id int auto_increment primary key not null, dwa_name varchar(255))ENGINE=INNODB default charset = utf8;
                                    ''')

                    self.mysqlconn.commit()

                    self.mysqlCurs.execute('select count(id) from tools')
                    if not self.mysqlCurs.fetchone()[0]:
                        self.mysqlCurs.execute('''
                                            insert into tools (st) value("o")
                                        ''')

                    self.mysqlconn.commit()

                except Exception as e:
                    print(e)
            else:
                pass

        except Exception as e:

            err_log = open('src/logs.txt', 'a')
            err_log.write('\n' + self.today + ' '  + str(e))
            err = QMessageBox.information(self, 'Error', str(e), QMessageBox.Ok)

    def save_(self):
            self.cursor.execute('DELETE FROM admin_setting')
            self.conn.commit()
            self.cursor.execute('insert into admin_setting (host, db_user, db_pass, port, db_name) values ("{}", "{}", "{}", {}, "{}")'.format(
                    self.db_host.text(), self.db_username.text(), self.db_passwrd.text(), int(self.db_port.text()),
                    self.db_name.text()))
            self.conn.commit()
            done = QMessageBox.information(self, 'DONE', 'info saved successfully', QMessageBox.Ok)
        # try:
        #     self.cursor.execute('DELETE FROM admin_setting')
        #     self.conn.commit()
        #     self.cursor.execute('insert into admin_setting (host, db_user, db_pass, port, db_name) values ("{}", "{}", "{}", {}, "{}")'.format(
        #             self.db_host.text(), self.db_username.text(), self.db_passwrd.text(), self.db_port.text(),
        #             self.db_name.text()))
        #     self.conn.commit()
        #     done = QMessageBox.information(self, 'DONE', 'info saved successfully', QMessageBox.Ok)
        # except Exception as e:
        #     done = QMessageBox.information(self, 'ERRor ', 'info not saved : ' + str(e), QMessageBox.Ok)


            #TODO delay
        #
        # if self.delay.text() != '' and self.serial.text() != '':
        #     if cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="delay";').fetchone():
        #         if cursor.execute('SELECT * FROM delay;').fetchall():
        #             cursor.execute('update delay set days = {}, serialK = "{}" where id = 1'.format(self.delay.text(), self.serial_key.text()))
        #         else:
        #             cursor.execute('insert into delay (days, serialK ) values ({}, "{}")'.format(self.delay.text(), self.serial_key.text()))
        #     else:
        #         cursor.execute('create table if not exists delay (id INTEGER PRIMARY KEY AUTOINCREMENT, days int, serialK text)')
        #         conn.commit()
        #         cursor.execute('insert into delay (days, serialK ) values ({}, "{}")'.format(self.delay.text(),
        #                                                                                      self.serial_key.text()))



    def quit_(self):
        self.conn.close()
        self.spl = index.Splash()
        self.spl.show()
        self.close()




