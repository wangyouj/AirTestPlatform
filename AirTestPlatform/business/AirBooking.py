'''
# @Author  : No.47
# @Time    : 2022/12/28 10:54
# @Function: 
'''

import logging
from business.LogicBase import haveProxyConfig, haveNoAutoConfig
from common.Tools import airSys
from apiDatas.airJson import sendSpaceApplyData, addTaskData, initProxyConfig
from mapper.AirSql import updateRequirementMatch, updateProxyConfig, addProxyConfig, \
    getSendApplyID, getUsedCapacityByName, setAutoReplay, getAddTaskID
from mapper.AtmsSql import getInfoByContractId, getSupplierInfo, getContractAndCapacaity

log = logging.getLogger('log')

class AirBooking():
    def __init__(self):
        self.session, self.cookie = airSys()
        self.headers = {'Content-Type': 'application/json'}

    def sendSpaceApply(self):
        '''
        发送订舱申请
        :return:
        '''
        idLists = getSendApplyID()
        idsList, relationIdlist=getPostIdList(idLists)
        for ids,relationIds in zip(idsList,relationIdlist):
            url, sendSpaceApplyJson = sendSpaceApplyData(ids, relationIds)
            res=self.session.post(url=url, json=sendSpaceApplyJson, headers=self.headers, verify=False)
            log.info(res)

    def addTask(self):
        '''
        生成任务
        :return:
        '''
        idLists = getAddTaskID()
        log.info('生成任务对应订舱ID为---'+str(idLists))
        idsList, relationIdlist = getPostIdList(idLists)
        for ids, relationIds in zip(idsList, relationIdlist):
            url,addTaskJson = addTaskData(ids, relationIds)
            res = self.session.post(url=url, json=addTaskJson, headers=self.headers, verify=False)
            log.info(res)

    def setProxyConfig(self):
        '''
        初始化采集配置
        :return:
        '''
        url, initProxyConfigJson = initProxyConfig()
        log.info("初始化采集配置开始...")
        print("还能使用否？")
        res = self.session.post(url=url, json=initProxyConfigJson, headers=self.headers, verify=False)
        log.info(res.text)
        print(res.text)

def refreshRequirementMatch():
    '''
    刷新需求吻合度数据
    :return:
    '''
    updateRequirementMatch()

#初始化采集配置
def setProxyConfig(deptCode,supplierId):
    if haveProxyConfig(deptCode, supplierId):
        updateProxyConfig(deptCode, supplierId)
    else:
        addProxyConfig(deptCode, supplierId)


def getPostIdList(idLists):
    idsList=[]
    relationIdlist=[]
    if len(idLists)>0:
        for sendApplyId in idLists:
            idsList.append(sendApplyId['id'])
            relationIdlist.append(sendApplyId['relationId'])
    n = 5  # 每5条数据单独一次申请
    idsList=[idsList[i:i + n] for i in range(0, len(idsList), n)]
    relationIdlist=[relationIdlist[i:i + n] for i in range(0, len(relationIdlist), n)]
    return idsList,relationIdlist



#获取运力列表
def getFlightList(contractId):
    flightList = []
    capacityAndContractList = getContractAndCapacaity(contractId)
    for capacityAndContract in capacityAndContractList[:200]:
        capacityName=capacityAndContract['capacity_name']
        flightList.append(capacityName)
    return flightList

#获取机场列表
def getThrLetterList(flightList):
    departList=[]
    arriveList=[]
    for flightNo in flightList:
        departAirPort=getUsedCapacityByName(flightNo)['depart_thr_letter_code']
        arriveAirPort=getUsedCapacityByName(flightNo)['arrive_thr_letter_code']
        departList.append(departAirPort)
        arriveList.append(arriveAirPort)
    return departList,arriveList


def setAutoReplaySpace(contractId):
    #获取订舱供应商
    spaceSupplierCode=getInfoByContractId(contractId)['space_supplier_code']
    print(spaceSupplierCode)
    if '1'==spaceSupplierCode:
        supplierId=getInfoByContractId(contractId)['contract_supplier_id']
    if '2'==spaceSupplierCode:
        supplierId=getInfoByContractId(contractId)['contract_supplier_id_2']
    if '3'==spaceSupplierCode:
        supplierId=getInfoByContractId(contractId)['contract_supplier_id_3']
    print('supplierId='+str(supplierId))
    pmCode=getSupplierInfo(supplierId)['supplier_one_id']
    flightList=getFlightList(contractId)
    departList, arriveList = getThrLetterList(flightList)
    for departThrLetterCode,arriveThrLetterCode in zip(departList, arriveList):
        if haveNoAutoConfig(supplierId,departThrLetterCode,arriveThrLetterCode):
            setAutoReplay(supplierId, departThrLetterCode, arriveThrLetterCode, pmCode)

