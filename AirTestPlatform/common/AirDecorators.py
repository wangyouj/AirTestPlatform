'''
@author: No.47
@file: AirDecorators.py
@time: 2024/9/1 19:35
@desc: Air装饰器管理
'''
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


def AirIntervalScheduler(seconds=None):
    '''
    interval触发器-固定间隔多少s执行一次
    :param seconds: int型 间隔时长-单位：s
    :return:
    '''
    def AirScheduler(func):
        def wrapper(*args, **kwargs):
            scheduler = BackgroundScheduler()
            scheduler.add_job(func, 'interval', seconds=seconds)
            scheduler.start()
        return wrapper

    return AirScheduler


def AirCronScheduler(day_of_week=None,hour=None, minute=None, second=None):
    '''
    cron触发器-指定时间周期性执行
    :param day_of_week: 类型=str,周内第几天或者星期几 (范围0-6 或者 mon,tue,wed,thu,fri,sat,sun)
    :param hour: 时 类型=str (范围0-23)
    :param minute: 分 类型=str (范围0-59)
    :param second: 秒 类型=str (范围0-59)
    :return:
    '''
    def AirScheduler(func):
        def wrapper(*args, **kwargs):
            scheduler = BackgroundScheduler()
            scheduler.add_job(func, 'cron', day_of_week=day_of_week,hour=hour, minute=minute, second=second, timezone='Asia/Shanghai')
            scheduler.start()
        return wrapper
    return AirScheduler


def AirDateScheduler(runTime=None):
    '''
    date型触发器-在指定时间执行一次
    :param runTime: str型  格式必须为‘YYYY-MM-DD HH:mm:ss’
    :return:
    '''
    def AirScheduler(func):
        def wrapper(*args, **kwargs):
            scheduler = BlockingScheduler()
            scheduler.add_job(func, 'date', run_date=runTime,timezone='Asia/Shanghai')
            scheduler.start()
        return wrapper

    return AirScheduler