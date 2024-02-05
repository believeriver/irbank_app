import logging
import sqlite3
import sys
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(PROJECT_PATH)
import config.settings

logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
logger = logging.getLogger(__name__)
# logging.info({'dao_sqlite3_path': PROJECT_PATH})
# logging.info({'DB': config.settings.DB_NAME})


class DaoSQLite3(object):
    def __init__(self, dbname: str = config.settings.DB_NAME):
        self.db_name = dbname
        self._conn = None
        self._curs = None
        self._conn_db()

    def __del__(self):
        self._close_db()

    def _conn_db(self):
        self._conn = sqlite3.connect(self.db_name)
        self._curs = self._conn.cursor()

    def _close_db(self):
        self._curs.close()
        self._conn.close()
        # print('--- close ' + self.db_name + ' database ---')
        # logging.info({'close database': self.db_name})

    # sample create sql(please override)
    def create_table(self, table_name):
        if self._conn is None:
            self._conn_db()
        # sample create sql
        self._curs.execute(
            'CREATE TABLE IF NOT EXISTS ' + table_name + '(id INTEGER PRIMARY KEY AUTOINCREMENT, name STRING)')
        self._conn.commit()

    # sample insert sql(please override)
    def insert(self, name):
        if self._conn is None:
            self._conn_db()
        # sample insert sql
        self._curs.execute(
            'INSERT INTO persons(name) values ("' + name + '")'
        )
        self._conn.commit()

    # sample update sql(please override)
    def update(self, table_name, pre_name, ch_name):
        if self._conn is None:
            self._conn_db()
        # sample update sql
        self._curs.execute(
            'UPDATE ' + table_name + ' set name = "' + ch_name + '" WHERE name = "' + pre_name + '"')
        self._conn.commit()

    # sample delete sql(please override)
    def delete_item(self, table_name, del_item):
        if self._conn is None:
            self._conn_db()
        # sample delete sql
        self._curs.execute(
            'DELETE FROM ' + table_name + ' WHERE name = "' + del_item + '"')
        self._conn.commit()

    # sample select sql(please override)
    def select_all(self, table_name):
        if self._conn is None:
            self._conn_db()
        # sample select all data sql
        self._curs.execute('SELECT * FROM ' + table_name)
        # logging.info({'select_all': self._curs.fetchall()})


"""
Test this code at main.

"""


def test():
    table_name = 'companies'
    db = DaoSQLite3()

    # test to create table
    # db.create_table(table_name)
    db.select_all(table_name)
    del db


if __name__ == '__main__':
    test()
