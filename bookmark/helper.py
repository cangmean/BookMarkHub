# coding=utf-8

import datetime
from database import query, execute, execute_sql_list
import logging


def init_db():
    user_sql = """
    CREATE TABLE if NOT exists user(
        id int primary key auto_increment,
        username varchar(20) not null unique,
        email varchar(100) not null,
        password varchar(300) not null,
        status varchar(1) not null default 0,
        create_time varchar(20) not null
    );
    """
    scene_sql = """
    CREATE TABLE if NOT exists scene(
        id int primary key auto_increment,
        name varchar(50) not null,
        user_id int not null,
        create_time varchar(20) not null
    );
    """
    folder_sql = """
    CREATE TABLE if NOT exists folder(
        id int primary key auto_increment,
        name varchar(50) not null,
        scene_id int not null,
        create_time varchar(20) not null
    );
    """
    mark_sql = """
    CREATE TABLE if NOT exists mark(
        id int primary key auto_increment,
        url varchar(100) not null,
        folder_id int not null,
        create_time varchar(20) not null
    );
    """
    sql_list = [user_sql, scene_sql, folder_sql, mark_sql]
    execute_sql_list(sql_list)


def drop_db():
    sql_list = []
    for table in ('scene', 'folder', 'mark', 'user'):
        sql_list.append('drop table if exists {};'.format(table))
    execute_sql_list(sql_list)


def create_user(username, email, password):
    now = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S')
    sql = """
    INSERT INTO user (username, email, password, create_time)
    values ('%s', '%s', '%s', '%s')
    """ % (username, email, password, now)
    execute(sql)
