import _sqlite3 as sq

con = sq.connect("/home/yassine-baghdadi/windowsApp/test/db.db")
# curs = con.execute("create table users (username text);")
curs = con.cursor()
# curs.execute("create table users (username text);")
# curs.execute('insert into users values ("yassine")')
# con.commit()
curs.execute('select * from users')

print(curs.fetchall())
