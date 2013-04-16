#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import datetime
import hashlib
import sqlite3
import settings
from bottle import route, get, post, template, request, response, redirect

user = {}

def check_login(fun):
    def inner(*args, **argkw):
        sessionId = request.get_cookie("session_id")
        if not sessionId:
            rand = os.urandom(16)
            now = time.time()
            session_id = hashlib.sha1("%s%s" % (rand, now)).hexdigest()
            response.set_cookie("session_id", session_id)
            redirect("/admin/login")
        connect = sqlite3.connect(settings.db_path)
        cursor = connect.cursor()
        sql = ("SELECT session_id, username, update_time FROM admin_session "
               "WHERE session_id=?")
        cursor.execute(sql, (sessionId, ))
        rows = cursor.fetchone()
        connect.close()
        if not rows:
            redirect("/admin/login")
        if not user.has_key("session_id"):
            user["session_id"] = rows[0]
            user["username"] = rows[1]
            user["update_time"] = rows[2]
        return fun(*args, **argkw)
    return inner

@route("/admin")
@check_login
def admin():
    return template(settings.admin_tpl_path+"admin.htm", user=user)

@get("/admin/login")
def login_form():
    return template(settings.admin_tpl_path+"login.htm")

@post("/admin/login")
def login():
    connect = sqlite3.connect(settings.db_path)
    cursor = connect.cursor()
    username = request.forms.get("username")
    password = request.forms.get("password")
    if username and password:
        sql = ("SELECT id, username, password, create_at FROM admin "
               "WHERE username=? AND password=?")
        cursor.execute(sql, (username, hashlib.md5(password).hexdigest()))
        rows = cursor.fetchone()
        if rows:
            # insert record into admin_session
            ssql = ("REPLACE INTO admin_session (session_id, username, update_time) "
                    "VALUES (?, ?, datetime('now', 'localtime'))")
            cursor.execute(ssql, (request.get_cookie("session_id"), username))
            connect.commit()
            connect.close()
            redirect("/admin")
    redirect("/admin/login")

@get("/admin/passwd")
@check_login
def change_passwd_form():
    return template(settings.admin_tpl_path+"change_passwd.htm")

@post("/admin/passwd")
@check_login
def change_passwd():
    old_passwd = request.forms.get("old_password").strip()
    old_passwd_hash = hashlib.md5(old_passwd).hexdigest()
    new_passwd = request.forms.get("password").strip()
    confirm_passwd = request.forms.get("confirm_password").strip()
    if new_passwd!=confirm_passwd:
        return template(settings.admin_tpl_path+"change_passwd.htm", 
                        message="两次输入的新密码不同。")
    connect = sqlite3.connect(settings.db_path)
    cursor = connect.cursor()
    sql = ("SELECT COUNT(*) FROM admin WHERE username=? AND password=?")
    cursor.execute(sql, (user["username"], old_passwd_hash))
    rows = cursor.fetchone()
    if not rows[0]:
        return template(settings.admin_tpl_path+"change_passwd.htm", 
                        message="旧密码不正确。")
    sql = ("UPDATE admin SET password=? WHERE username=?")
    password = hashlib.md5(new_passwd).hexdigest()
    cursor.execute(sql, (password, user["username"]))
    connect.commit()
    connect.close()
    redirect("/admin")

@get("/admin/masterlist")
@check_login
def masterlist():
    connect = sqlite3.connect(settings.db_path)
    cursor = connect.cursor()
    page = 0
    sql = ("SELECT * FROM master_info LIMIT 0, 30;")
    cursor.execute(sql)
    rows = cursor.fetchall()
    return template(settings.admin_tpl_path+"masterlist.htm",
                    rows=rows, settings=settings, time=time)

@get("/admin/logout")
def logout():
    connect = sqlite3.connect(settings.db_path)
    cursor = connect.cursor()
    sql = ("DELETE FROM admin_session WHERE username=? and session_id=?")
    cursor.execute(sql, (user['username'], request.get_cookie("session_id")))
    connect.commit()
    connect.close()
    redirect("/admin/login")


"""
class AdminBaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.connect = sqlite3.connect(settings.db_path)
        self.cursor = self.connect.cursor()
        if not self.get_cookie("session_id"):
            rand = os.urandom(16)
            now = time.time()
            session_id = hashlib.sha1("%s%s" % (rand, now)).hexdigest()
            self.set_cookie("session_id", session_id)

    def authenticate(self, username, password):
        self.cursor.execute('SELECT id, username FROM admin WHERE username=? and password=?', 
                            (username, password))
        return self.cursor.fetchone()

    def update_current_user(self, username):
        rows = self.get_current_user()
        if not rows or len(rows)==0:
            self.cursor.execute(
                'insert into admin_session values (?, ?, datetime("now", "localtime"))', 
                (self.get_cookie("session_id"), username))
        else:
            self.cursor.execute(
                "update admin_session set update_time=datetime('now', 'localtime') "
                "where session_id=?", (self.get_cookie("session_id"), ))
        self.connect.commit()

    def get_current_user(self):
        self.cursor.execute(
            "select session_id, username, update_time "
            "from admin_session where session_id=?", 
            (self.get_cookie("session_id"),))
        row = self.cursor.fetchone()
        if row:
            login_time = time.strptime(row[2], "%Y-%m-%d %H:%M:%S")
            now = datetime.datetime.now()
            utime = datetime.datetime(*login_time[:6])
            if ((now-utime).seconds - 3600) > 0:
                self.cursor.execute(
                    "delete from admin_session where session_id=?", 
                    (self.get_cookie("session_id"), ))
                self.connect.commit()
                row = None
            else:
                self.cursor.execute(
                    "update admin_session set update_time=datetime('now', 'localtime') "
                    "where session_id=?", 
                    (self.get_cookie("session_id"), ))
                self.connect.commit()
        return row


class Admin(AdminBaseHandler):
    def get(self):
        user = self.get_current_user()
        if not user:
            self.redirect("/admin/login")
        self.render(settings.admin_tpl_path+"admin.htm")

class Login(AdminBaseHandler):
    def get(self):
        self.render(settings.admin_tpl_path+"login.htm")

    def post(self):
        user = self.get_current_user()
        if not user:
            username = self.get_argument("username")
            password = hashlib.md5(self.get_argument("password")).hexdigest()
            rows = self.authenticate(username, password)
            if rows:
                self.update_current_user(username)
            user = self.get_current_user()
        if user:
            self.redirect("/admin")


class ApplyList(AdminBaseHandler):
    def get(self, job):
        job = int(job)
        print job
        if 1==job:
            table_name = "master_info"
        elif 2==job:
            table_name = "doctor_info"
        else:
            raise tornado.web.HTTPError(404)
        sql = "SELECT * FROM %s LIMIT 0, 30" % table_name
        rows = self.cursor.execute(sql)
        print rows
        self.render(settings.admin_tpl_path+"applylist.htm")
"""
