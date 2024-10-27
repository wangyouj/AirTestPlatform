'''
# @Author  : No.47
# @Time    : 2022/12/5 16:12
# @Function: 
'''
import json
import logging

from business.AirSysConfig import airVisitLog
from business.LogicBase import haveBookingPlan
from apiDatas.airJson import queryRequirements
from mapper.AirSql import setRequireMent, getTestConfigValues, getUsedCapacityList, \
    insertBookingPlan, selectUsedCapacityByAirport, getTestConfig, insertCostResource, updateCostResource, \
    updateCostResourceDeleted, initIsSupplementary
from common.Tools import airSys, markNum

log = logging.getLogger('log')
'''
根据发货网点获取可用需求
'''
def getRequirementIds(n=1):
    TestDeptCodeList=getTestConfigValues()
    if len(TestDeptCodeList)>0:
        url,data = queryRequirements(TestDeptCodeList,n)
        session, cookie = airSys()
        res = session.post(url=url, json=data, verify=False).json()
        requirementList = res['result']['records']
        ids = []
        for requirement in requirementList:
            if requirement['availableSpace'] > 0:
                ids.append(requirement['id'])
        return ids
    else:
        return []

def test_sendRequirement(n=1):
    #获取可用需求
    ids=getRequirementIds(n)
    if len(ids)>0:
        for id in ids:
            #设置计划需求量
            setRequireMent(id)
            #发起需求
            url = 'http://shiva-trtms-air-service-web.sit.sf-express.com/air/requirement/bookingmanger/planRequirement/initiate'
            session, cookie = airSys()
            res=session.put(url=url,json=ids,verify=False)
            log.info(res.json())
            log.info(res.text)
        airVisitLog("/air/excuteAirJob/")
    else:
        log.info("未获取到可用需求数据")


 #临时-计划需求补录
def test_sendRequirementTemp(n=0):
    #初始化补录标识
    initIsSupplementary()
    #补录-发起
    test_sendRequirement(n)



def addBookingPlan():
    capacityList=getUsedCapacityList()
    if len(capacityList)>0:
        for capacity in capacityList:
            srcBatchDt=capacity['capa_plan_send_batch_dt']
            srcCityCode=capacity['depart_city_code']
            desCityCode=capacity['arrive_city_code']
            srcZoneCode=capacity['depart_dept_code']
            desZoneCode=capacity['arrive_dept_code']
            srcBatchCode=capacity['send_bill_batch_no']
            if haveBookingPlan(srcBatchDt,srcCityCode,desCityCode,srcZoneCode,desZoneCode,srcBatchCode)==False:
                insertBookingPlan(srcBatchDt, srcCityCode, desCityCode, srcZoneCode, desZoneCode, srcBatchCode)
                log.info('--'.join([str(srcBatchDt), srcCityCode, desCityCode, srcZoneCode, desZoneCode, srcBatchCode])+'维护需求计划OK!')

def addcostResourcePre(flightDt, departThrLetterCode, arriveThrLetterCode, capacityName, planSendBatchDt,
                           planSendBatch,scheduleFlightType, departDeptCode, arriveDeptCode, departCityCode, arriveCityCode,
                           goodsLeaveDt,planSendDt, planArrDt, lineKey,avaiableSpaceAmount,
                           planGetBatchDt, planGetBatch, batchSeparateDay, planSendSeparateDay, planGetSeparateDay,
                           lineCode, lastestArrStationDt, departCityName, arriveCityName,
                           stationLastestStopDt,lastestArriveDt, getArrStationDt):
    cabinId=markNum(slen=8)
    cargoTypeList = [1, 2, 3, 5]
    for cargoType in cargoTypeList:
        insertCostResource(flightDt, departThrLetterCode, arriveThrLetterCode, capacityName, planSendBatchDt,
                           planSendBatch,scheduleFlightType, departDeptCode, arriveDeptCode, departCityCode, arriveCityCode,
                           goodsLeaveDt,planSendDt, planArrDt, lineKey, cargoType, avaiableSpaceAmount,
                           planGetBatchDt, planGetBatch, batchSeparateDay, planSendSeparateDay, planGetSeparateDay,
                           lineCode, lastestArrStationDt, departCityName, arriveCityName,
                          cabinId, stationLastestStopDt,lastestArriveDt, getArrStationDt)

def addcostResource():
    addcostResourceParams = json.loads(getTestConfig(taskName='addcostResourceParams')['values'])
    departThrLetterCode = addcostResourceParams['departThrLetterCode']
    arriveThrLetterCode = addcostResourceParams['arriveThrLetterCode']
    capacityList=selectUsedCapacityByAirport(departThrLetterCode,arriveThrLetterCode)
    if len(capacityList)>0:
        for capacity in capacityList:
            print(capacity)
            flightDt=capacity['effective_dt']
            departThrLetterCode = capacity['depart_thr_letter_code']
            arriveThrLetterCode = capacity['arrive_thr_letter_code']
            capacityName = capacity['capacity_name']
            planSendBatchDt = capacity['capa_plan_send_batch_dt']
            planSendBatch = capacity['send_bill_batch_no']
            scheduleFlightType = capacity['schedule_flight_type']
            departDeptCode = capacity['depart_dept_code']
            arriveDeptCode = capacity['arrive_dept_code']
            departCityCode = capacity['depart_city_code']
            arriveCityCode = capacity['arrive_city_code']
            goodsLeaveDt = capacity['goods_leave_dt']
            planSendDt = capacity['plan_send_dt']
            planArrDt = capacity['plan_arr_dt']
            lineKey = capacity['line_key']
            avaiableSpaceAmount = int(capacity['max_load'])*0.5
            planGetBatchDt = capacity['capa_plan_distribute_batch_dt']
            planGetBatch = capacity['get_bill_batch_no']
            batchSeparateDay = capacity['batch_separate_day']
            planSendSeparateDay = capacity['send_batch_separate_day']
            planGetSeparateDay = capacity['plan_arrive_separate_day']
            lineCode = capacity['line_code']
            lastestArrStationDt = capacity['lastest_arr_station_dt']
            departCityName = capacity['depart_city_name']
            arriveCityName = capacity['arrive_city_name']
            stationLastestStopDt = capacity['station_lastest_stop_dt']
            lastestArriveDt = capacity['lastest_arrive_dt']
            getArrStationDt = capacity['get_arr_station_dt']
            addcostResourcePre(flightDt, departThrLetterCode, arriveThrLetterCode, capacityName, planSendBatchDt,
                               planSendBatch, scheduleFlightType, departDeptCode, arriveDeptCode, departCityCode,
                               arriveCityCode,
                               goodsLeaveDt, planSendDt, planArrDt, lineKey, avaiableSpaceAmount,
                               planGetBatchDt, planGetBatch, batchSeparateDay, planSendSeparateDay, planGetSeparateDay,
                               lineCode, lastestArrStationDt, departCityName, arriveCityName,
                               stationLastestStopDt, lastestArriveDt, getArrStationDt)


'''
--air
#FlightResourceTask   每2分钟增量触发AIR推送航班资源实际订舱信息至ARES
#ShCostResourceInfoEntryTask  计算散航成本-资源任务信息任务

为保证鄂枢联调测试数据稳定，临时停止后台任务，如需启动资源成本定时任务，则：
##散航旧定时任务逻辑：
①继承AbstractSingleTask，可以通过tm_single_task_config配置表控制
②继承AbstractBaseTask，在后台代码中无限循环，通过TT_PESSIMISTIC_LOCKING获得到锁以后则开始执行：
#停止任务
UPDATE TT_PESSIMISTIC_LOCKING 
SET NODE_KEY = '停止任务', TM = now(), LOCK_REASON = '停止任务'
WHERE `KEY` = 'shCostResourceInfoEntry'
#重置开始任务
UPDATE TT_PESSIMISTIC_LOCKING 
SET TM = now(), LOCK_REASON = null 
WHERE `KEY` = 'shCostResourceInfoEntry'
'''

def refreshCostResource():
    log.info('开始刷新散航资源数据')
    updateCostResource()
    log.info('散航资源数据刷新OK!')

def refreshCostResourceDeleted():
    log.info('翻转删除状态')
    updateCostResourceDeleted()
    log.info('翻转删除状态OK!')


