'''
# @Author  : No.47
# @Time    : 2023/1/9 11:05
# @Function: 
'''

#计划需求发起前初始化配置
import json
import logging
import requests
from mapper.AirBaseSql import getAirSysConfig, updateAirSysConfig
from apiDatas.airJson import airVisit
from mapper.AirSql import getTestConfigValues, setAirSchedulerSwitch, getTestConfig

log = logging.getLogger('log')

def checkRequirementConfig():
    sysConfigList = getAirSysConfig(keyCode='V11.7_PILOT_DEPT_AND_SEND_BATCH_DT')
    currentConfigValue=''
    if len(sysConfigList)>0:
        currentConfigValue = sysConfigList['config_value']
    testCityList=getConfigCity()
    airCityTuple=getAirConfigTuple()
    for city in testCityList:
        if airCityTuple.__contains__('001')==False and airCityTuple.__contains__(city)==False:
            appendStr='#'+city+'R:2022-08-31'
            currentConfigValue=currentConfigValue+appendStr
    updateAirSysConfig(configValue=currentConfigValue, keyCode='V11.7_PILOT_DEPT_AND_SEND_BATCH_DT')

def getConfigCity():
    testDeptList=getTestConfigValues(taskName='sendRequirementJob')
    testCityList=[]
    for dept in testDeptList:
        city=dept[:3]
        testCityList.append(city)
    print(testCityList)
    return testCityList

def getAirConfigTuple():
    sysConfigList = getAirSysConfig(keyCode='V11.7_PILOT_DEPT_AND_SEND_BATCH_DT')
    cityTuple=()
    if len(sysConfigList)>0:
        currentConfigValue=sysConfigList['config_value']
        print(currentConfigValue)
        xlist=currentConfigValue.split('#')
        deptList=[]
        for m in xlist:
            n=m.split(':')
            deptList.append(n[0][:3])
        cityTuple=tuple(deptList)
    return cityTuple

#定时任务开关切换
def setAirScheduleSwitch(taskName):
    currentState=getTestConfig(taskName)['state']
    state=1
    if currentState==1:
        state=0
    if currentState==0:
        state=1
    setAirSchedulerSwitch(state, taskName)

def airVisitLog(visiturl):
    headers = {'Content-Type': 'application/json'}
    url, visitLog=airVisit(visiturl)
    res=requests.post(url=url,data=json.dumps(visitLog),headers=headers)
    log.info(res)