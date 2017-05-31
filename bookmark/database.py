# coding=utf-8

import pymysql

def get_connect(db_name, kls=False):
    config = dict(
        host='localhost',
        user='root',
        passwd='xxxxx',
        db='{}'.format(db_name),
        charset='utf8'
    )
    if kls:
        config.update({'cursorclass': pymysql.cursors.DictCursor})
    conn = pymysql.connect(**config)
    return conn


def init_db():
    conn = get_connect('bookmarkhub')
    cursor = conn.cursor()
    user_sql = """
    CREATE TABLE if NOT exists user(
        id int primary key auto_increment,
        username varchar(20) not null unique,
        email varchar(100) not null,
        password varchar(300) not null,
        status varchar(1) not null default 0,
        create_time datetime not null
    );
    """
    scene_sql = """
    CREATE TABLE if NOT exists scene(
        id int primary key auto_increment,
        name varchar(50) not null,
        user_id int not null,
        create_time datetime not null
    );
    """
    folder_sql = """
    CREATE TABLE if NOT exists folder(
        id int primary key auto_increment,
        name varchar(50) not null,
        scene_id int not null,
        create_time datetime not null
    );
    """
    mark_sql = """
    CREATE TABLE if NOT exists mark(
        id int primary key auto_increment,
        url varchar(100) not null,
        folder_id int not null,
        create_time datetime not null
    );
    """
    cursor.execute(user_sql)
    cursor.execute(scene_sql)
    cursor.execute(folder_sql)
    cursor.execute(mark_sql)


def drop_db():
    conn = get_connect('bookmarkhub')
    cursor = conn.cursor()
    for table in ('scene', 'folder', 'mark', 'user'):
        cursor.execute('drop table if exists {};'.format(table))
