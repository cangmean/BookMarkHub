# coding=utf-8

import pymysql
import functools
import threading
import logging

logger = logging.getLogger(__name__)

_connection_settings = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'passwd': '654321',
    'db': 'bookmarkhub',
    'charset': 'utf8',
}

_connection = None


def _get_connection(dictcursor=True):
    global _connection
    if _connection is None:
        if dictcursor:
            _connection_settings.update({
                'cursorclass': pymysql.cursors.DictCursor
            })
        _connection = pymysql.connect(**_connection_settings)
    return _connection


def _log(msg, level='debug'):
    level_dict = {
        'debug': logger.debug,
        'info': logger.info,
        'error': logger.error,
    }
    log = level_dict.get(level, 'debug')
    log(msg)


class ConnectionError(Exception):
    pass


class ConnectCtx(object):

    def __init__(self):
        self.conn = None

    @property
    def init(self):
        raise AttributeError('Context init is not a readle attribute.')

    @init.setter
    def init(self, conn):
        self.conn = conn
        self.cursor = conn.cursor()

    def is_init(self):
        if not self.conn:
            raise ConnectionError('Not connection. please initialize connection.')

    def query_(self, sql):
        self.is_init()
        cur = self.cursor
        try:
            cur.execute(sql)
            result = cur.fetchall()
            return result
        except Exception as e:
            print(e)
            # _log(e, 'error')

    def execute_(self, sql):
        self.is_init()
        cur = self.cursor
        try:
            cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            # self.conn.rollback()
            print(e)
            # _log(e, 'error')

    def executemany_(self, sql, data):
        self.is_init()
        cur = self.cursor
        try:
            cur.executemany(sql, data)
            self.conn.commit()
        except Exception as e:
            # self.conn.rollback()
            print(e)
            # _log(e, 'error')

    def __enter__(self):
        return self

    def __exit__(self, type_, val_, traceback_):
        self.cursor.close()
        if self.conn:
            conn = self.conn
            self.conn = None
            conn.close()


def execute(sql):
    with ConnectCtx() as ctx:
        ctx.init = _get_connection()
        ctx.execute_(sql)


def execute_many(sql, data):
    with ConnectCtx() as ctx:
        ctx.init = _get_connection()
        ctx.executemany_(sql, data)


def execute_sql_list(sql_list):
    with ConnectCtx() as ctx:
        ctx.init = _get_connection()
        for sql in sql_list:
            ctx.execute_(sql)


def query(sql):
    with ConnectCtx() as ctx:
        ctx.init = _get_connection()
        rows = ctx.query_(sql) or []
    return rows
