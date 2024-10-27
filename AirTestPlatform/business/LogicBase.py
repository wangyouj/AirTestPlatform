'''
# @Author  : No.47
# @Time    : 2022/12/15 18:37
# @Function: 
'''

from apiDatas.airJson import getCapaList
from mapper.AirSql import getContractAndCapa, getAvaiableCabin, getUsedCapacity, \
    getCabinCargoType, getProxyConfig, getAutoReplay, selectBookingPlan, getUsedCapacityByNameAndDate
from common.Tools import airSys
from mapper.AtmsSql import getCnSendPriceMain, getContractItemById, getCnSendPriceItem, \
    getInfoByContractId


# 获取机型业载
def getMaxLoad(capacityName, departCityCode, arriveCityCode):
    maxLoad = 0
    if int(getUsedCapacity(capacityName, departCityCode, arriveCityCode)[0]['max_load']) != None:
        maxLoad = int(int(getUsedCapacity(capacityName, departCityCode, arriveCityCode)[0]['max_load']) * 0.2)
    return maxLoad


'''
获取运力维度数据
'''
def getMainCapaList(contractId):
    deptCode=getInfoByContractId(contractId)['dept_code']
    contractType=getInfoByContractId(contractId)['contract_type']
    url, getCapaListJson = getCapaList(deptCode,contractType)
    session, cookie = airSys()
    res = session.post(url=url, json=getCapaListJson, verify=False).json()
    mainCapaList = res['result']['records']
    return mainCapaList


'''
判断是否存在可用运力
'''
def haveUsedCapacity(capacityName, departCityCode, arriveCityCode):
    usedCapacityList = getUsedCapacity(capacityName, departCityCode, arriveCityCode)
    if len(usedCapacityList) > 0:
        return True
    else:
        return False


'''
判断合同运力是否存在
'''
def haveContractAndCapa(capacityName, departCityCode, arriveCityCode, contractId):
    CAndCapaList = getContractAndCapa(capacityName, departCityCode, arriveCityCode, contractId)
    if len(CAndCapaList) > 0:
        return True
    else:
        return False


'''
判断是否有无可用舱位
'''
def haveAvaiableCabin(contractId, capacityName, departCityCode, arriveCityCode):
    avaiableCabinList = getAvaiableCabin(contractId, capacityName, departCityCode, arriveCityCode)
    if len(avaiableCabinList) > 0:
        return True
    else:
        return False


# 判断有无舱位货物类型
def haveNoCabinCargoType(cabinId):
    cabinCargoTypeList = getCabinCargoType(cabinId)
    if len(cabinCargoTypeList) == 0:
        return True
    else:
        return False

#判断有无运价
def haveNoCnSendPrice(contractId,capacityName,departCityCode, arriveCityCode):
    cnSendPriceList = getCnSendPriceMain(contractId,capacityName,departCityCode, arriveCityCode)
    if len(cnSendPriceList) > 0:
        return False
    else:
        return True

def haveNoCnSendPriceItem(sendId):
    cnSendPriceItemList=getCnSendPriceItem(sendId)
    if len(cnSendPriceItemList)==0:
        return True
    else:
        return False

#根据合同ID获取服务编码
def getServerCodeListByCOntractId(contractId):
    serverCodeList=[]
    ContractItemList=getContractItemById(contractId)
    for ContractItem in ContractItemList:
        serverCodeList.append(ContractItem['serve_code'])
    return serverCodeList

#根据网点+供应商判断有无采集配置
def haveProxyConfig(deptCode='010R',supplierId='10101000167485'):
    proxyConfigList=getProxyConfig(deptCode,supplierId)
    if len(proxyConfigList)>0:
        return True
    else:
        return False

#当前运力在当天是否存在
def isCapacityExistCurrent(capacityName):
    list=getUsedCapacityByNameAndDate(capacityName)
    if len(list)>0:
        return True
    else:
        return False

def haveNoAutoConfig(supplierId,departThrLetterCode,arriveThrLetterCode):
    configList=getAutoReplay(supplierId,departThrLetterCode,arriveThrLetterCode)
    if len(configList)>0:
        return False
    else:
        return True

def haveBookingPlan(srcBatchDt,srcCityCode,desCityCode,srcZoneCode,desZoneCode,srcBatchCode):
    bookingPlanList=selectBookingPlan(srcBatchDt,srcCityCode,desCityCode,srcZoneCode,desZoneCode,srcBatchCode)
    if len(bookingPlanList)>0:
        return True
    else:
        return False