'''
# @Author  : No.47
# @Time    : 2023/3/15 14:42
# @Function: 
'''
from common.DBUtil import do_sql
from config.DBconfig import db_uranus


def airUranusDB(sql):
    conf=db_uranus()
    # print(sql)
    return do_sql(conf,sql)

def setAresShort():
    aresSendInitSql='''UPDATE `tt_air_short_send_task_info` p SET send_transport_tm=15,send_transport_distance=66 WHERE
     p.`cvy_type`=1 AND plan_send_batch_dt='2023-03-15' AND src_zone_code='755R';'''
    sendNotice='''UPDATE tt_air_short_send_task_info p SET update_tm = NOW() WHERE p.`cvy_type`=1 AND plan_send_batch_dt='2023-03-15' AND src_zone_code='755R';'''


