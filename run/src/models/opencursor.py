""" OpenCursor: context object for sqlite3 """

import sqlite3

DBNAME = "game.db"

def setDB(dbname):
    """ opencursor.setDB() sets the default DBNAME for OpenCursor objects """
    global DBNAME
    DBNAME = dbname


class OpenCursor:
    """ Context object for sqlite3 """

    def __init__(self, db=None, *args, **kwargs):
        """ db, args, kwargs passed to sqlite3.connect """
        if db is None:
            db = DBNAME

        # by default, set check_same_thread to False (optimization for single-
        # threaded applications)
        kwargs['check_same_thread'] = kwargs.get('check_same_thread', False)

        self.conn = sqlite3.connect(db, *args, **kwargs)

        # setting row_factory to sqlite3.Row makes fetch statements return
        # objects that can be indexed by column name
        self.conn.row_factory = sqlite3.Row  # access fetch results by col name

        self.cursor = self.conn.cursor()

    def __enter__(self):
        """ with OpenCursor as x returns self.cursor """
        return self.cursor

    def __exit__(self, extype, exvalue, extraceback):
        """ commit changes upon exiting a with block if no errors raised """
        if not extype:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
