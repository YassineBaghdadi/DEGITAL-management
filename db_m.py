import pymysql



class DB_m:
    def __init__(self, host, user, psw, db, port  = 3306):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            passwd=psw,
            db = db,
            port = port

        )

        self.curs = self.conn.cursor()


    def query_(self, sql_):
        self.curs.execute(sql_)
        self.conn.commit()

    def close_db(self):
        self.conn.close()

    def logIn(self, u, p):
        try:
            try:
                self.curs.execute('select role from users where username = "{}" and passwrd = "{}"'.format(u, p))
                return self.curs.fetchone()[0]

            except:
                return 'wrong'
        except:
            return 'error'



