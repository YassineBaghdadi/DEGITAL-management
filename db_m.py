import mysql.connector

class DB_m:
    def __init__(self, host, port, user, psw):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            passwd=psw
        )

        self.curs = self.conn.cursor()
        self.curs.execute('CREATE DATABASE IF NOT EXISTS {};'.format(db))
        self.conn.commit()
        self.curs.execute('use {};'.format(db))




    def query_(self, sql_):
        self.curs.execute(sql_)
        self.conn.commit()

    def close_db(self):
        self.conn.close()

db = DB_m('192.168.0.158', 3306, 'vmacc', 'root')

