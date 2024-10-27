'''
@author: No.47
@file: DBUtil.py
@time: 2024/7/16 19:00
@desc: API处理通用
'''

import pymysql

from common.Tools import getOrgStr
from config.DBconfig import db_airOpen, db_airTest, db_airSit


# 连接DB执行sql并返回执行结果
def do_sql(conf, sql):
    '''
    依赖库：下载pymysql: pip install pymysql
    注意：
        1-charset 不能使用utf-8,而需要使用utf8
        2-密码必须是字符串
    :param sql:
    :return: sql执行结果
    '''
    host, user, password, database, port, charset = conf
    db = pymysql.connect(host=getOrgStr(host), user=getOrgStr(user), password=getOrgStr(str(password)),
                         database=getOrgStr(database), port=port, charset=charset)
    # 建立一个游标,加入参数pymysql.cursors.DictCursor控制返回结果为字典
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 运行sql语句
    cursor.execute(sql)
    db.commit()
    # 将sql查询结果存放在data变量中
    data = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 断开数据库连接
    db.close()
    return data


# open库操作
def DBUtil(DB, sql):
    '''
    :param DB: 指定实例
    :param sql: sql
    :return:
    '''
    return do_sql(DB, sql)


# open库操作
def airOpenDB(sql):
    conf = db_airOpen()
    return do_sql(conf, sql)

def airTestDB(sql):
    conf = db_airTest()
    return do_sql(conf, sql)

def airSitDB(sql):
    conf = db_airSit()
    return do_sql(conf, sql)

