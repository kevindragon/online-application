#!/usr/bin/env python
# -*- coding: utf-8 -*-

import settings

if __name__ == "__main__":
    conn = sqlite3.connect(settings.db_path)
    c = conn.cursor()
    create_sql = '''CREATE TABLE test
             (id integer PRIMARY KEY)'''

