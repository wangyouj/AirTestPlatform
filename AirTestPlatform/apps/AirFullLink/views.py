import json
import requests
import logging
from datetime import date
from math import ceil
from django.http import  HttpResponse

from common.ApiUtil import downloadResponse, queryStandardReponse, ApiReponse, standardReponse, taskManageReponse
from common.CustomException import ListLengthZeroError
from common.Tools import bjtm
from mapper.AirOpenSql import export_budget_data_sql
from business.AirSysConfig import setAirScheduleSwitch, airVisitLog
from apiDatas.HBGJJson import subDynamicInfo
from apiDatas.airJson import  OneCodeKafka
from mapper.AirSql import getTaskInfo, addOneCodeLog, getOneCodeLog, getAirSchedulerConfig, \
    setAirSchedulerConfig, getUsedCapacityByName, getStandardTm
from common.Tools import random_str, sysDate
from job.AirScheduler import runAddTaskJob, excuteCurrentJob, runSetDistanceJob, sendBillConformJob, \
    runRfreshCostResourceJob, runRfreshCostResourceDeletedJob

from mapper.AirSql import getAirPortCode, getBookingLog, setRequireMent
from common.Tools import airSys
from apiDatas.airJson import requirementJson
from mapper.AirSql import addBookingLog
from job.AirScheduler import sendRequirementJob, addCnCarrPriceJob, runAddContractAndCapaJob, \
    runRefreshRequirementMatchJob, runsendSpaceApplyJob, runSetAutoReplaySpaceJob
from business.AIrRequirement import getRequirementIds
from business.AirTask import AirBase, addCnCarrPrice


# Create your views here.
log = logging.getLogger('log')


def downloadFiles(request):
    '''
    demo
    :param request:
    :return:
    '''
    print(request.body)
    log.info("1---------------------")
    if request.method == 'POST':
        req = json.loads(request.body)
        flowCount = req['flowCount']
        return HttpResponse("开发中...")

    else:
        return HttpResponse("请求方式错误,请使用post方式")


def downloadBudgetData(request):
    '''
    预算下载
    :param request:
    :return:
    '''
    #获取可下载数据
    exportBudgetDataSql, data = export_budget_data_sql()
    #文件名
    fileName = 'ImportableBudgetListV{0}.xlsx'.format(str(bjtm()))
    log.info('下载文件名为：--'+fileName)
    #sheet名
    sheetName = '预算明细'
    if len(data) <= 0:
        raise ListLengthZeroError
    else:
        return downloadResponse(data,fileName=fileName,sheetName=sheetName)


'''
根据taskId生成对应一个码推送数据
请求示例：
{"taskId":"2022112300008",
"containerNo":"90999",
"startNumber":1,
"endNumber":9
}
'''
def getOneCode(request):
    airVisitLog("/air/getOneCode/")
    log.info(request.body)
    if request.method == 'POST':
        req=json.loads(request.body)
        log.info(req)
        taskId = req['taskId']
        virtualContainerNo=random_str()
        containerNo = req['containerNo']
        startNumber= req['startNumber']
        endNumber= req['endNumber']
        mainNumber1=getTaskInfo(taskId)[0]['main_number']
        mainNumber=mainNumber1.replace(mainNumber1[3], "", 1)
        oneCode=[]
        i=startNumber
        while i<=endNumber:
            m=str(i).zfill(5)
            startStr = "{" + '''"mainWayBillNo":"{}"'''.format(mainNumber+m)
            oneCode.append(json.loads(startStr+'''}'''))
            i += 1
        log.info(oneCode)
        result=OneCodeKafka(taskId,containerNo,virtualContainerNo,oneCode)
        addOneCodeLog(taskId, containerNo, virtualContainerNo, startNumber, endNumber, result)
        return HttpResponse(result, content_type='application/json', charset='utf-8')
    else:
        return HttpResponse('参数错误')



'''
@function:查询一个码记录
请求示例：
{
"currentPage":2,
"pageSize":10
}
'''
def queryOneCodeLog(request):
    log.info(request.body)
    if request.method=='POST':
        req=json.loads(request.body)
        log.info(req)
        currentPage=req['currentPage']
        pageSize=req['pageSize']
        result,total=getOneCodeLog(currentPage,pageSize)
        airReponse = queryStandardReponse(total=total, pages=ceil(total / pageSize), currentPage=currentPage,content=result)
        return ApiReponse(airReponse)
    else:
        return HttpResponse('参数错误')

'''
@function:查询air定时任务配置
请求示例：
{
"currentPage":1,
"pageSize":10
}
'''
def queryAirSchedulerConfig(request):
    print(request.body)
    if request.method=='POST':
        req=json.loads(request.body)
        log.info(req)
        currentPage=req['currentPage']
        pageSize=req['pageSize']
        result,total=getAirSchedulerConfig(currentPage,pageSize)
        airReponse = queryStandardReponse(total=total, pages=ceil(total / pageSize), currentPage=currentPage,content=result)
        return ApiReponse(airReponse)
    else:
        return HttpResponse('参数错误')


'''
@function:修改air定时任务配置
请求示例：
{
"taskName":"sendRequirementJob",
"deptCode":"755R"
}
'''
def updateAirSchedulerConfig(request):
    print(request.body)
    if request.method=='POST':
        req=json.loads(request.body)
        log.info(req)
        values=req['values']
        taskName=req['task_name']
        setAirSchedulerConfig(values,taskName)
        airReponse=standardReponse()
        return ApiReponse(airReponse)
    else:
        return HttpResponse('参数错误')

'''
@function:立即执行指定定时任务
请求示例：
{
"taskName":"addCnSendPriceByContractId",
}
'''
def excuteAirJob(request):
    log.info(request.body)
    if request.method=='POST':
        req=json.loads(request.body)
        log.info(req)
        taskName=req['task_name']
        excuteCurrentJob(taskName)
        airReponse=taskManageReponse(msg='执行成功！')
        return ApiReponse(airReponse)
    else:
        return HttpResponse('参数错误')


'''
@function:定时任务开关
请求示例：
{
"taskName":"addCnSendPriceByContractId"
}
'''
def AirSchedulerSwitch(request):
    print(request.body)
    if request.method=='POST':
        req=json.loads(request.body)
        log.info(req)
        taskName=req['task_name']
        setAirScheduleSwitch(taskName)
        airReponse=taskManageReponse()
        return ApiReponse(airReponse)
    else:
        return HttpResponse('参数错误')



'''
指定航班号及日期发起需求并自动发起订舱
当前仅支持有维护舱位的航班
示例：
{
"flightNo": "ZH9111",
"sendDate": "2022-11-26"
}
'''
def addBookingByFlightNo(request):
    airVisitLog("/air/booking/")
    log.info(request.body)
    if request.method == 'POST':
        req=json.loads(request.body)
        log.info(req)
        flightNo = req['flightNo']
        sendDate = req['sendDate']
        capacityList=getAirPortCode(flightNo,sendDate)
        if len(capacityList)>0:
            srcAirport=getAirPortCode(flightNo,sendDate)[0]['depart_thr_letter_code']
            desAirport=getAirPortCode(flightNo,sendDate)[0]['arrive_thr_letter_code']
            data = requirementJson(flightNo, sendDate,srcAirport,desAirport)
            log.info(data)
            url = 'http://shiva-trtms-air-service-requirement.intsit.sfcloud.local/air/requirement/openApi/receiveExclusiveDemand'
            headers = {'Content-Type': 'application/json'}
            result = requests.post(url,headers=headers,data=data)
            requirementId=json.loads(result.text)['result']['requireId']
            createdTm=bjtm()
            if requirementId!='':
                addBookingLog(flightNo, sendDate, requirementId, 1,createdTm)
            return HttpResponse(result, content_type='application/json', charset='utf-8')
        else:
            return HttpResponse('不存在可用运力信息！')
    else:
        return HttpResponse('参数错误')

'''
@function:查询发起日志
请求示例：
{
"flightNo":"CZ1090",
"sendDate":"2022-12-04",
"currentPage":2,
"pageSize":5
}
'''
def queryBookingLog(request):
    log.info(request.body)
    if request.method=='POST':
        req=json.loads(request.body)
        log.info(req)
        flightNo = req['flightNo']
        sendDate = req['sendDate']
        currentPage=req['currentPage']
        pageSize=req['pageSize']
        start=(currentPage-1)*pageSize
        result,total=getBookingLog(flightNo,sendDate,start,pageSize)
        return HttpResponse(queryStandardReponse(total=total,pages=ceil(total/pageSize),currentPage=currentPage,content=result), content_type='application/json', charset='utf-8')
    else:
        return HttpResponse('参数错误')

#手动触发发起t+1计划需求
def startSentRequirement(request):
    if request.method == 'GET':
        # 获取可用需求
        ids = getRequirementIds()
        # 设置计划需求量
        setRequireMent(ids)
        # 发起需求
        url = 'http://shiva-trtms-air-service-web.sit.sf-express.com/air/requirement/bookingmanger/planRequirement/initiate'
        session, cookie = airSys()
        result = session.put(url=url, json=ids, verify=False)
        return HttpResponse(result,content_type='application/json', charset='utf-8')
    else:
        return HttpResponse('参数错误')

'''
手动触发维护运价
请求示例：
{
"contractId":"5022262036"
}
'''

def startAddCnSendPrice(request):
    airBase = AirBase()
    log.info(request.body)
    if request.method == 'POST':
        req = json.loads(request.body)
        log.info(req)
        contractId = req['contractId']
        airBase.addBaseDataForAir(contractId)
        addCnCarrPrice(contractId)
        return HttpResponse('发起成功！')
    else:
        return HttpResponse('参数错误')



'''
请求示例：
{
"capacityName":"CK291",
"versionDt":"2023-11-16"
}
'''
#推送航班订阅动态
def pushSubDynamicInfo(request):
    print(request.body)
    if request.method == 'POST':
        req = json.loads(request.body)
        log.info(req)
        capacityName = req['capacityName']
        versionDt= req['versionDt']
        if versionDt=='':
            versionDt=sysDate()
        departThrLetterCode=getUsedCapacityByName(capacityName,versionDt)['depart_thr_letter_code']
        arriveThrLetterCode=getUsedCapacityByName(capacityName,versionDt)['arrive_thr_letter_code']
        planFlyDepartTm=getUsedCapacityByName(capacityName,versionDt)['plan_depart_tm']
        planArriveTm=getUsedCapacityByName(capacityName,versionDt)['plan_arrive_tm']
        planSendDt=getUsedCapacityByName(capacityName,versionDt)['plan_send_dt']
        planArrDt=getUsedCapacityByName(capacityName,versionDt)['plan_arr_dt']
        planFlyTm=getStandardTm(versionDt,planFlyDepartTm)
        planArrTm=getStandardTm(versionDt,planArriveTm)
        actualFlyTm=date.strftime(planSendDt, '%Y-%m-%d %H:%M')
        actualArriveTm=date.strftime(planArrDt, '%Y-%m-%d %H:%M')
        planeType=getUsedCapacityByName(capacityName,versionDt)['plane_type']
        capacityState='到达'
        urlSubDynamicInfo, headers, dataSubDynamicInfo, proxies=subDynamicInfo(capacityName, versionDt, departThrLetterCode, arriveThrLetterCode, planFlyTm,
                           actualFlyTm, planeType, capacityState, planArrTm, actualArriveTm)
        log.info(headers)
        log.info(dataSubDynamicInfo)
        res = requests.post(urlSubDynamicInfo, headers=headers, data=json.dumps(dataSubDynamicInfo,ensure_ascii=False).encode('utf-8'), proxies=proxies)
        print(res.text)
        result=res.text
        return HttpResponse(result)
    else:
        return HttpResponse('参数错误')




'''
需求、订舱定时任务部分
'''
#发起t+1计划需求定时任务
sendRequirementJob()
#根据合同维护合同运力+舱位
runAddContractAndCapaJob()
#根据配置表合同ID生成运价
addCnCarrPriceJob()
#维护需求订舱吻合度数据
runRefreshRequirementMatchJob()
#自动发起订舱申请
runsendSpaceApplyJob()
#维护自动批复
runSetAutoReplaySpaceJob()

'''
任务、短驳定时任务部分
'''
#生成任务
runAddTaskJob()
#短驳运输距离配置
runSetDistanceJob()
#发货确认
sendBillConformJob()


'''
其它模块定时任务
'''
# runAddBookingPlanJob()
#每天更新资源数据供ARES使用
runRfreshCostResourceJob()
runRfreshCostResourceDeletedJob()






