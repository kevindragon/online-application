#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import settings
import sqlite3

def _get_db(cursor=True):
    """获取操作数据库的句柄"""
    if not os.path.exists(settings.db_path):
        return None
    conn = sqlite3.connect(settings.db_path)
    if cursor:
        return conn.cursor()
    else:
        return conn

def insert(sql):
    conn = _get_db(False)
    c = conn.cursor()
    c.execute(sql)
    conn.commit()

def fetchone(sql):
    c = _get_db()
    c.execute(sql)
    return c.fetchone()

def fetchall(sql):
    c = _get_db()
    yield c.execute(sql)
