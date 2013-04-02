#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import time
import datetime
import hashlib
import tornado.web
import sqlite3
import settings

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
