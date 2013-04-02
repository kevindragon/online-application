#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
import config

if not config.DEBUG:
    print "server is running"
    sys.stderr = open("app_err.log", "a")
    sys.stdout = open("app.log", "a")
"""

import sys
import tornado.ioloop
import tornado.web
import tornado.autoreload
import settings

reload(sys)
sys.setdefaultencoding("utf-8")

application = tornado.web.Application(
    settings.urls, 
    cookie_secret = settings.cookie_secret, 
    debug=True, 
    xsrf_cookies=True,)

if __name__ == "__main__":
    application.listen(8888)
    loop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(loop)
    loop.start()
