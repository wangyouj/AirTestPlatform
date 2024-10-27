'''
# @Author  : No.47
# @Time    : 2023/1/31 16:47
# @Function: 
'''
import logging

from mapper.AirSql import setDistanceAndTm

log = logging.getLogger('log')

def setDistanceAndTmForShort():
    log.info('开始刷新运力信息运输距离...')
    setDistanceAndTm()
    log.info('刷新运力信息运输距离OK...')
