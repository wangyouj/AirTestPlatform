'''
@author: No.47
@file: AirTaskSql.py
@time: 2024/8/25 11:01
@desc:
'''
import logging

from common.DBUtil import airSitDB

log = logging.getLogger('log')


def getDispatchData(businessId, sendId, exceptionId, currentPage, pageSize):
    '''

    :param businessId: 业务ID
    :param sendId: 发货ID
    :param exceptionId: 异常ID
    :param currentPage:
    :param pageSize:
    :return:
    '''
    start = (currentPage - 1) * pageSize
    querySql = '''SELECT * FROM  tl_send_exception_dispatch WHERE create_time >DATE_ADD(current_date() , INTERVAL -360 DAY)
                and send_date is not null and tranfer_date  is not null
                and (business_id='{0}' or '{0}'='') and (send_id='{1}' or '{1}'='')  and  (exception_id='{2}' or '{2}'='')
                order by create_time desc limit {3},{4};'''.format(businessId, sendId, exceptionId, start, pageSize)
    countSql = '''SELECT count(*) FROM  tl_send_exception_dispatch WHERE create_time >DATE_ADD(current_date() , INTERVAL -360 DAY) and
                (business_id='{0}' or '{0}'='') and (send_id='{1}' or '{1}'='')  and
                (exception_id='{2}' or '{2}'='');'''.format(businessId, sendId, exceptionId)
    log.info(querySql)
    log.info('------------------------')
    log.info(countSql)
    result = airSitDB(querySql)
    total = airSitDB(countSql)[0]['count(*)']
    return result, total
