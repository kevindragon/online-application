#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import shutil
import hashlib
import time
import sqlite3
from bottle import route, get, post, template, static_file, request
import settings


@route("/upload/<filename:path>")
def static_upload_files(filename):
    return static_file(filename, root='upload/')

@route("/static/<filename:path>")
def static_files(filename):
    return static_file(filename, root='static/')

@get("/")
def index():
    return template(settings.app_tpl_path+"masterapply.htm", nav=1)

@post("/uploadimage")
def upload_image():
    filename = ""
    filedata = request.files.get("Filedata")
    if filedata.file:
        filename = ("%s%s%s" % 
                    (settings.upload_tmp_path, 
                     hashlib.md5(str(time.time())).hexdigest(),
                     filedata.filename))
        open(filename, "wb").write(filedata.file.read())
    return "/%s" % filename

@post("/postinfo")
def post_master_form():
    '''硕士研究生表单提交处理'''
    name_str = ["name", "gender", "id_number", "university", "major", 
                "email", "phone", "avatar", "prov", "city", "birthday", 
                "political_status", "graduate_date", "special_skill"]
    post_data = [request.forms.get(x, "") for x in name_str]
    pd_dict = dict(zip(name_str, post_data))

    # 复制图片到相应目录
    avatar_path = "/".join((settings.upload_path, pd_dict["id_number"]))
    if not os.path.exists(avatar_path):
        os.mkdir(avatar_path)
    src_file = pd_dict["avatar"][1:]
    dst_file = "/".join((avatar_path, os.path.basename(pd_dict["avatar"])))
    if src_file!=dst_file:
        try:
            shutil.move(src_file, dst_file)
        except Exception:
            pass
    # update upload_path to new file path
    post_data[7] = dst_file

    connect = sqlite3.connect(settings.db_path)
    connect.text_factory = str
    cursor = connect.cursor()
    edit = False
    if "1"==request.forms.get("edit"):
        fields = []
        for item in zip(name_str, post_data):
            fields.append("%s='%s'" % item)
        sql = "UPDATE master_info SET %s WHERE id=?" % ",".join(fields)
        params = (int(request.forms.get("lastrowid", 0)), )
        pd_dict.update(lastrowid=int(request.forms.get("lastrowid", 0)))
        edit = True
    else:
        sql = ("INSERT INTO master_info (id, name, gender, id_number, "
               "university, major, email, phone, avatar, prov, city, birthday, "
               "political_status, graduate_date, special_skill) VALUES ("
               "NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        params = post_data
    
    try:
        cursor.execute(sql, params)
        connect.commit()
        if not edit:
            pd_dict.update(lastrowid=cursor.lastrowid)
    except Exception:
        sql = "select id from master_info where id_number=? and name=?"
        cursor.execute(sql, (pd_dict["id_number"], pd_dict["name"]))
        row = cursor.fetchall()
        if len(row):
            pd_dict.update(lastrowid=row[0][0])
    connect.close()
    
    pd_dict.update(avatar=("/%s" % dst_file))
    pd_dict.update(gender_mc="checked='true'" if "男"==pd_dict["gender"] else "")
    pd_dict.update(gender_wc="checked='true'" if "女"==pd_dict["gender"] else "")
    return template(settings.app_tpl_path+"applyinfo.htm", nav=1, **pd_dict)

@get("/infoquery")
def infoquery():
    return template(settings.app_tpl_path+"infoquery.htm", nav=2)    

@post("/infoquery")
def doquery():
    params = [request.forms.get("name"), request.forms.get("id_number")]
    
    connect = sqlite3.connect(settings.db_path)
    connect.text_factory = str
    cursor = connect.cursor()
    
    sql = "SELECT * FROM master_info WHERE name=? AND id_number=?"
    cursor.execute(sql, params)
    row = cursor.fetchall()
    
    name_str = ["id", "name", "gender", "id_number", "university", "major", 
                "email", "phone", "avatar", "prov", "city", "birthday", 
                "political_status", "graduate_date", "special_skill"]
    info_dict = {}
    if len(row):
        info_dict = dict(zip(name_str, row[0]))
        tpl = settings.app_tpl_path+"applyinfo.htm"
        info_dict.update(lastrowid=info_dict["id"])
        info_dict.update(gender_mc="checked='true'" if "男"==info_dict["gender"] else "")
        info_dict.update(gender_wc="checked='true'" if "女"==info_dict["gender"] else "")
    else:
        tpl = settings.app_tpl_path+"error.htm"
    connect.close()
    
    if "1"==request.forms.get("query"):
        info_dict.update(query=1)

    return template(tpl, nav=1, **info_dict)

