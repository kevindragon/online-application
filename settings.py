#!/usr/bin/env python
# -*- coding: utf-8 -*-


import tornado.web
import app
import admin

urls = [
    (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static/"}),
    (r"/upload/(.*)", tornado.web.StaticFileHandler, {"path": "upload/"}),
    (r"/", app.Home),
    (r"/doctorapply", app.DoctorApply), 
    (r"/postinfo", app.PostInfo),
    (r"/infoquery", app.InfoQuery), 
    (r"/uploadimage", app.UploadImage), 
    (r"/admin", admin.Admin), 
    (r"/admin/login", admin.Login), 
    (r"/admin/applylist/([12])", admin.ApplyList)
]

cookie_secret = "c00667408975a58d958a302d9073ce84e246cac1"

db_path = "database/database.db"

# template settings
admin_tpl_path = "template/admin/"
app_tpl_path = "template/"

upload_path = "upload/"
upload_tmp_path = "upload/tmp/"
