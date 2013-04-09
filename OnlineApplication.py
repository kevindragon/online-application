#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
import config

if not config.DEBUG:
    print "server is running"
    sys.stderr = open("app_err.log", "a")
    sys.stdout = open("app.log", "a")
"""


from bottle import route, run, template
import settings


if __name__ == "__main__":
    import app
    run(host='0.0.0.0', port=8888, debug=True, reloader=True)
