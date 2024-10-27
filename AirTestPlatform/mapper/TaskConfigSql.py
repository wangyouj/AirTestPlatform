'''
@author: No.47
@file: TaskConfigSql.py
@time: 2024/8/18 18:02
@desc: 任务管理、系统配置
'''
from common.DBUtil import airTestDB


# 查询定时任务配置
def getAirSysConfig(currentPage, pageSize):
    start = (currentPage - 1) * pageSize
    sql1 = '''select * from air_scheduler_config where config_type=2 order by id limit {0},{1};'''.format(start, pageSize)
    sql2 = '''select count(*) from air_scheduler_config where config_type=2;'''
    result = airTestDB(sql1)
    total = airTestDB(sql2)[0]['count(*)']
    return result, total