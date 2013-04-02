import hashlib
import sqlite3

dbfile = "database/database.db"

conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute("create table admin (id integer primary key, "
          "username varchar(50), password varchar(50), "
          "create_at datetime)")
c.execute("")
conn.commit()
c.execute("select * from admin")
print c.fetchall()

