# -*- coding: utf-8 -*-

import sqlite3 

cx = sqlite3.connect("sqlite.db")

i = 1
for line in open("score.txt"):
    score = line.strip("\n").strip("\r").split(",")
    if len(score) != 2 or score[0] == "" or score[1] == "":
        print "error: line %s was incorrect." % i
        i += 1
        continue

    cu = cx.cursor()

    cu.execute(u"update app_peopleextra set reason = reason || \"&lt;br&gt;您的笔试成绩为：%s分\" where ticket_number = %s" % (str(score[1]), str(score[0])))
    cx.commit()
    i += 1

cx.close()
