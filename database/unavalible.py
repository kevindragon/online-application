# -*- coding: utf-8 -*-

import sqlite3 

cx = sqlite3.connect("sqlite.db")

for idnumber in open("id_list.txt"):
    idnumber = idnumber.strip("\n").strip("\r")
    if idnumber == "":
        continue

    cu = cx.cursor()

    cu.execute("select id from app_people where id_number = %s limit 1" % idnumber)
    row = cu.fetchone()
    if len(row) < 1:
        continue
    print idnumber, row

    cu.execute(u"update app_people set audit_step = 8 where id = %d" % row[0])
    cx.commit()

    #cu.execute("select id from app_peopleextra where people_id = %d" % row[0])
    #r = cu.fetchone()

    cu.execute(u"update app_peopleextra set audit_step = 8, reason = '' where people_id = %d" % row[0])
    cx.commit()

cx.close()
