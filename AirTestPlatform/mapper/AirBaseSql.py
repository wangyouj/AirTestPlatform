'''
# @Author  : No.47
# @Time    : 2023/1/9 10:54
# @Function: 
'''
from config.DBconfig import db_airSit, db_airTest, db_report

from common.DBUtil import do_sql


def airDB(sql):
    conf = db_airSit()
    # print(sql)
    return do_sql(conf, sql)

def airTest(sql):
    conf = db_airTest()
    # print(sql)
    return do_sql(conf, sql)

def airReportDB(sql):
    conf=db_report()
    # print(sql)
    return do_sql(conf,sql)


def getAirSysConfig(keyCode):
    sql='''SELECT * FROM  `ts_air_sysconfig` p WHERE p.`key_code`='{}' LIMIT 1;'''.format(keyCode)
    sysConfigList=airDB(sql)
    if len(sysConfigList)>0:
        return sysConfigList[0]
    else:
        return []

def updateAirSysConfig(configValue,keyCode):
    sql='''UPDATE ts_air_sysconfig p SET p.`config_value`='{}' WHERE p.`key_code`='{}';'''.format(configValue,keyCode)
    airDB(sql)

