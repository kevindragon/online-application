#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import sys
import sqlite3
import tornado.web
from bottle import route, get, post, template, static_file, request
import settings


@route("/upload/<filename:path>")
@route("/static/<filename:path>")
def static_files(filename):
    return static_file(filename, root='static/')

@route("/static/flash/<filename:path>")
def static_flash_file(filename):
    return static_file(filename, root="static/flash", 
                       mimetype="application/x-shockwave-flash")

@get("/")
def index():
    return template(settings.app_tpl_path+"index.htm", nav=1)

'''
@route("/uploadimage")
def upload_image():
    '' '
    avatar_file = "%s/%s" % (settings.upload_tmp_path,  
                             request.files["avatar"][0]["filename"])
    if request.files["avatar"][0]["filename"]:
        if not os.path.exists(settings.upload_tmp_path):
            os.mkdir(settings.upload_tmp_path)
        open(avatar_file, "w").write(request.files["avatar"][0]["body"])
    '' '
    print request
    return "haha"
'''

class Home(tornado.web.RequestHandler):
    def get(self):
        self.render(settings.app_tpl_path+"index.htm", nav=1)


class PostInfo(tornado.web.RequestHandler):
    def post(self):
        name_str = ["name", "gender", "id_number", "university",
                    "major", "email", "phone"]
        info = [self.get_argument(x) for x in name_str]
        avatar_path = "%s%s" % (settings.upload_path, 
                                 self.get_argument("id_number"))
        avatar_file = "%s/%s" % (avatar_path,  
                                 self.request.files["avatar"][0]["filename"])
        info.append(avatar_file)
        if self.request.files["avatar"][0]["filename"]:
            if not os.path.exists(avatar_path):
                os.mkdir(avatar_path)
            open(avatar_file, "w").write(self.request.files["avatar"][0]["body"])
        
        connect = sqlite3.connect(settings.db_path)
        cursor = connect.cursor()
        sql = ("INSERT INTO master_info (id, name, gender, id_number, "
               "university, major, email, phone, avatar) VALUES ("
               "NULL, ?, ?, ?, ?, ?, ?, ?, ?)")
        try:
            cursor.execute(sql, info)
            connect.commit()
        except Exception, e:
            print "unique"
        connect.close()
        
        data = dict(zip(name_str+["avatar"], info))
        self.render(settings.app_tpl_path+"applyinfo.htm", data=data, nav=1)



class InfoQuery(tornado.web.RequestHandler):
    def get(self):
        self.render(settings.app_tpl_path+"infoquery.htm", nav=3)
    
    def post(self):
        data = {}
        not_found = False
        job = int(self.get_argument("job"))
        nav = 1
        if 1==job:
            fields = ("id", "name", "gender", "id_number", "university", 
                      "major", "email", "phone", "avatar")
            table_name = "master_info"
        elif 2==job:
            fields = ("id", "name", "gender", "id_number", "university", 
                      "major", "email", "phone", "avatar")
            table_name = "doctor_info"
            nav = 2
        else:
            not_found = True
        
        if not not_found:
            connect = sqlite3.connect(settings.db_path)
            cursor = connect.cursor()
            sql = ("SELECT %s FROM %s WHERE name=? AND id_number=?" % 
                   (",".join(fields), table_name))
            print sql
            cursor.execute(sql, (self.get_argument("name"), self.get_argument("id_number")))
            rows = cursor.fetchall()
            connect.close()
            if len(rows):
                data.update(dict(zip(fields, rows[0])))
            else:
                not_found = False
        self.render(settings.app_tpl_path+"applyinfo.htm", data=data, nav=nav)


class DoctorApply(tornado.web.RequestHandler):
    def get(self):
        self.render(settings.app_tpl_path+"doctorapply.htm", nav=2)

    def post(self):
        name_str = ["name", "gender", "id_number", "university",
                    "major", "email", "phone"]
        info = [self.get_argument(x) for x in name_str]
        avatar_path = "%s%s" % (settings.upload_path, 
                                 self.get_argument("id_number"))
        avatar_file = "%s/%s" % (avatar_path,  
                                 self.request.files["avatar"][0]["filename"])
        info.append(avatar_file)
        if self.request.files["avatar"][0]["filename"]:
            if not os.path.exists(avatar_path):
                os.mkdir(avatar_path)
            open(avatar_file, "w").write(self.request.files["avatar"][0]["body"])
        
        connect = sqlite3.connect(settings.db_path)
        cursor = connect.cursor()
        sql = ("INSERT INTO doctor_info (id, name, gender, id_number, "
               "university, major, email, phone, avatar) VALUES ("
               "NULL, ?, ?, ?, ?, ?, ?, ?, ?)")
        try:
            cursor.execute(sql, info)
            connect.commit()
        except Exception, e:
            print "unique"
        connect.close()

        data = dict(zip(name_str+["avatar"], info))
        self.render(settings.app_tpl_path+"applyinfo.htm", data=data, nav=2)


class UploadImage(tornado.web.RequestHandler):
    def post(self):
        '''
        avatar_file = "%s/%s" % (settings.upload_tmp_path,  
                                 self.request.files["avatar"][0]["filename"])
        info.append(avatar_file)
        if self.request.files["avatar"][0]["filename"]:
            if not os.path.exists(avatar_path):
                os.mkdir(avatar_path)
            open(avatar_file, "w").write(self.request.files["avatar"][0]["body"])
        '''
        print self.request
        self.write("post")

    def get(self):
        self.write('get')
