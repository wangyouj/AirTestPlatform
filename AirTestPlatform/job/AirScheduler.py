'''
# @Author  : No.47
# @Time    : 2022/12/5 17:17
# @Function:
'''
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from business.AirSysConfig import checkRequirementConfig, airVisitLog
from common.AirDecorators import AirCronScheduler, AirIntervalScheduler
from mapper.AirSql import getTestConfigValues
from business.AIrRequirement import test_sendRequirement, addcostResource, \
    refreshCostResource, refreshCostResourceDeleted, test_sendRequirementTemp
from business.AirBooking import refreshRequirementMatch, AirBooking, setAutoReplaySpace
from business.AirShort import setDistanceAndTmForShort
from business.AirTask import addCnCarrPrice, AirBase, addKCgetBillByContractId, addIairBillByContractId, \
    sendBillConformByTaskId

log = logging.getLogger('log')


# 当上游不再推送测试环境订舱周计划、系统取消自动兜底功能时，采用该任务生成订舱计划数据
# def addBookingPlanJob():
#     addBookingPlan()
#
# def runAddBookingPlanJob():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(addBookingPlanJob, 'cron', day_of_week='fri',hour='08', minute='05', timezone='Asia/Shanghai')
#     scheduler.start()

# 提供给前台触发批量发起需求
def sendRequirement():
    checkRequirementConfig()
    test_sendRequirement()


# 定时调度执行
@AirCronScheduler(hour='00', minute='05')
def sendRequirementJob():
    sendRequirement()


# #初始化采集配置
# def initProxyConfigJob():
#     airBooking = AirBooking()
#     airBooking.setProxyConfig()
#
# def runInitProxyConfigJob():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(initProxyConfigJob, 'cron', hour='15',minute='35',timezone='Asia/Shanghai')
#     scheduler.start()


# 根据配置合同生成运价
def addCnCarrPrice():
    contractIdList = getTestConfigValues(taskName='addCnSendPriceByContractId')
    if len(contractIdList) > 0:
        for contractId in contractIdList:
            addCnCarrPrice(contractId)
    else:
        return
    airVisitLog("/air/excuteAirJob/")


# 根据配置中合同增量维护发货运价
@AirCronScheduler(hour='02', minute='05')
def addCnCarrPriceJob():
    addCnCarrPrice()



# 根据配置自动维护合同运力
def addContractAndCapaJob():
    airBase = AirBase()
    contractIdList = getTestConfigValues(taskName='addContractAndCapaByContractId')
    if len(contractIdList) > 0:
        for contractId in contractIdList:
            airBase.addBaseDataForAir(contractId)
    else:
        return
    airVisitLog("/air/excuteAirJob/")


# 根据配置合同每日增量维护合同运力
def runAddContractAndCapaJob():
    # print('自动生成合同运力+舱位...')
    scheduler = BackgroundScheduler()
    scheduler.add_job(addContractAndCapaJob, 'cron', hour='01', minute='05', timezone='Asia/Shanghai')
    scheduler.start()
    # print('已启动...执行中...')


def refreshRequirementMatchJob():
    refreshRequirementMatch()


# 每日刷新需求吻合度数据，确保前台可查询
def runRefreshRequirementMatchJob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(refreshRequirementMatchJob, 'cron', hour='07', minute='05', timezone='Asia/Shanghai')
    scheduler.start()


def sendSpaceApplyJob():
    airBooking = AirBooking()
    airBooking.sendSpaceApply()
    airVisitLog("/air/excuteAirJob/")


# 0105发送订舱申请
def runsendSpaceApplyJob():
    # scheduler= BlockingScheduler()
    scheduler = BackgroundScheduler()
    scheduler.add_job(sendSpaceApplyJob, 'cron', hour='01', minute='30', timezone='Asia/Shanghai')
    # scheduler.add_job(sendSpaceApplyJob,'interval', minutes = 2,timezone='Asia/Shanghai')
    scheduler.start()


def setAutoReplaySpaceJob():
    contractIdList = getTestConfigValues(taskName='autoReplaySpaceByContractId')
    if len(contractIdList) > 0:
        for contractId in contractIdList:
            setAutoReplaySpace(contractId)
    airVisitLog("/air/excuteAirJob/")


def runSetAutoReplaySpaceJob():
    # scheduler= BlockingScheduler()
    scheduler = BackgroundScheduler()
    scheduler.add_job(setAutoReplaySpaceJob, 'cron', hour='00', minute='30', timezone='Asia/Shanghai')
    # scheduler.add_job(setAutoReplaySpaceJob,'interval', minutes = 1,timezone='Asia/Shanghai')
    scheduler.start()


def addTaskJob():
    airBooking = AirBooking()
    airBooking.addTask()
    airVisitLog("/air/excuteAirJob/")


def runAddTaskJob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(addTaskJob, 'cron', hour='03,05', minute='05', timezone='Asia/Shanghai')
    scheduler.start()


def setDistanceJob():
    setDistanceAndTmForShort()


def runSetDistanceJob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(setDistanceJob, 'cron', hour='06,07,08', minute='05', timezone='Asia/Shanghai')
    scheduler.start()


# 发货确认
def sendBillConform():
    '''
    提供给前台调用
    :return:
    '''
    sendBillConformByTaskId()


@AirCronScheduler(hour='07', minute='45')
def sendBillConformJob():
    sendBillConformByTaskId()

#测试代码
# def AirCronInfo():
#     log.info('testAirCron被正常执行----' + str(bjtm()))
#
#
# @AirCronScheduler(minute='00,02,05,07,09,15,20,25,35,45,50,55', second='1,2,9,10,15,25,35,45,55')
# def AirCronInfoJob():
#     AirCronInfo()


# 新增KC提货任务
def addKCgetBillJob():
    contractList = getTestConfigValues(taskName='KCgetBillByContract')
    for contractId in contractList:
        addKCgetBillByContractId(contractId)
    airVisitLog("/air/excuteAirJob/")


def runAddKCgetBillJob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(addKCgetBillJob, 'cron', hour='05,08', minute='05', timezone='Asia/Shanghai')
    scheduler.start()


# 新增国际提货任务
def addIAirgetBillJob():
    contractList = getTestConfigValues(taskName='IairGetBillByContract')
    for contractId in contractList:
        addIairBillByContractId(contractId)


def runaddIAirgetBillJob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(addIAirgetBillJob, 'cron', hour='06', minute='05', timezone='Asia/Shanghai')
    scheduler.start()


def addcostResourceJob():
    airVisitLog("/air/excuteAirJob/")
    addcostResource()


def refreshCostResourceJob():
    airVisitLog("/air/excuteAirJob/")
    refreshCostResource()


def runRfreshCostResourceJob():
    scheduler = BackgroundScheduler()
    scheduler.add_job(refreshCostResourceJob, 'cron', hour='06', minute='15', timezone='Asia/Shanghai')
    scheduler.start()


def refreshCostResourceDeletedJob():
    refreshCostResourceDeleted()


@AirIntervalScheduler(seconds=60)
def runRfreshCostResourceDeletedJob():
    refreshCostResourceDeleted()



def sendRequirementTempJob():
    checkRequirementConfig()
    test_sendRequirementTemp()
    airVisitLog("/air/excuteAirJob/")


def jobNone():
    log.info("对应定时任务不存在！")


jobDict = {"sendRequirementJob": sendRequirement, "sendSpaceApply": sendSpaceApplyJob,
           "addAirTask": addTaskJob, "addContractAndCapaByContractId": addContractAndCapaJob,
           "autoReplaySpaceByContractId": setAutoReplaySpaceJob, "addCnSendPriceByContractId": addCnCarrPrice,
           "KCgetBillByContract": addKCgetBillJob, "IairGetBillByContract": addIAirgetBillJob,
           "addcostResourceParams": addcostResourceJob, "sendBillConform": sendBillConform,
           "sendRequirementTempJob": sendRequirementTempJob}


# 提供给前台触发定时任务
def excuteCurrentJob(taskName):
    return jobDict.get(taskName, jobNone)()
