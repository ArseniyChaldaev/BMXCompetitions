import os
import sqlite3

from GlobalVars import DB_PATH, DATABASE_INIT_SCRIPT


def init_database():
    if os.path.exists(DB_PATH):
        return
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.executescript(DATABASE_INIT_SCRIPT)
        con.commit()
    except sqlite3.Error as ex:
        print(ex)
    finally:
        if con:
            con.close()


def get_one_from_db(query):
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        return cur.execute(query).fetchone()
    except sqlite3.Error as ex:
        print(ex)
    finally:
        if con:
            con.close()


def get_all_from_db(query):
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        return cur.execute(query).fetchall()
    except sqlite3.Error as ex:
        print(ex)
    finally:
        if con:
            con.close()


def execute_many_on_db(query, values):
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.executemany(query, values)
        con.commit()
    except sqlite3.Error as ex:
        print(ex)
    finally:
        if con:
            con.close()


def execute_on_db(query, values=None):
    con = None
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        if values:
            cur.execute(query, values)
        else:
            cur.execute(query)
        con.commit()
    except sqlite3.Error as ex:
        print(ex)
    finally:
        if con:
            con.close()
