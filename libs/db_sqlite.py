from .db import Database
import sqlite3
from itertools import zip_longest as izip_longest
import numpy as np


class SqliteDatabase(Database):
    TABLE_SONGS = 'songs'
    TABLE_FINGERPRINTS = 'fingerprints'

    def __init__(self):
        self.conn = None
        self.cur = None
        self.connect()
        sqlite3.register_adapter(np.int64, lambda val: int(val))
        sqlite3.register_adapter(np.int32, lambda val: int(val))

    def connect(self):
        self.conn = sqlite3.connect("db/fingerprints.db")
        self.conn.text_factory = str
        self.cur = self.conn.cursor()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def query(self, query, values=()):
        self.cur.execute(query, values)

    def executeOne(self, query, values=()):
        self.cur.execute(query, values)
        return self.cur.fetchone()

    def executeAll(self, query, values=()):
        self.cur.execute(query, values)
        return self.cur.fetchall()

    def buildSelectQuery(self, table, params):
        conditions = []
        values = []

        for k, v in enumerate(params):
            key = v
            value = params[v]
            conditions.append("%s = ?" % key)
            values.append(value)

        conditions = ' AND '.join(conditions)
        query = "SELECT * FROM %s WHERE %s" % (table, conditions)

        return {
            "query": query,
            "values": values
        }

    def findOne(self, table, params):
        select = self.buildSelectQuery(table, params)
        return self.executeOne(select['query'], select['values'])

    def findAll(self, table, params):
        select = self.buildSelectQuery(table, params)
        return self.executeAll(select['query'], select['values'])

    def insert(self, table, params):
        keys = ', '.join(params.keys())
        values = list(params.values())

        query = "INSERT INTO songs (%s) VALUES (?, ?)" % keys

        self.cur.execute(query, values)
        self.conn.commit()

        return self.cur.lastrowid

    def insertMany(self, table, columns, values):
        def grouper(iterable, n, fillvalue=None):
            args = [iter(iterable)] * n
            return (filter(None, values) for values
                    in izip_longest(fillvalue=fillvalue, *args))

        for split_values in grouper(values, 1000):
            query = "INSERT OR IGNORE INTO %s (%s) VALUES (?, ?, ?)" % (table, ", ".join(columns))
            self.cur.executemany(query, split_values)

        self.conn.commit()

    def get_song_hashes_count(self, song_id):
        query = 'SELECT count(*) FROM %s WHERE song_fk = %d' % (self.TABLE_FINGERPRINTS, song_id)
        rows = self.executeOne(query)
        return int(rows[0])
