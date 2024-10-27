'''
# @Author  : No.47
# @Time    : 2022/12/09 14:05
# @Function:
'''
import logging
import requests

from business.AirSysConfig import airVisitLog
from business.LogicBase import getMainCapaList, haveUsedCapacity, haveContractAndCapa, haveAvaiableCabin, \
    getMaxLoad, haveNoCabinCargoType, haveNoCnSendPrice, haveNoCnSendPriceItem, \
    isCapacityExistCurrent
from apiDatas.airJson import addContAndCapaJson, KC_billData, Iair_billData, OEapproveInfo
from mapper.AirSql import getAvaiableCabin, getUsedCapacity, \
    removeUnAvaiableCabin, setAvaiableCabin, setCabinCargoType, removeCnSendPriceAir, getUsedCapacityByName, getUsedCapacityByNameAndDate, getSendBillData, sendBillConform, \
    getApprovingExceptionInfobySendId
from common.Tools import airSys, currentTm
from mapper.AtmsSql import getInfoByContractId, setCnSendPriceMain, getContractAndCapacaity, \
    getCnSendPriceMain, getContractItemById, setCnSendPriceItem, getSupplierCode, removeCnSendPriceAtms, \
    CnSendPricePushToAir

log = logging.getLogger('log')

class AirBase():
    def __init__(self):
        self.session, self.cookie = airSys()
        self.headers = {'Cookie': self.cookie, 'Content-Type': 'application/json'}

    '''
    判断运力维度是否存在合同运力，若不存在:
        判断是否有可用运力，若存在有效运力，则自动维护合同运力
    维护合同运力之后：
        判断是否有可用舱位，若无舱位，则自动维护舱位
    '''
    def addBaseDataForAir(self,contractId):
        mainCapaList=getMainCapaList(contractId)
        log.info(mainCapaList)
        for mainCapacity in mainCapaList:
            applicableScheduledDays=mainCapacity['applicableScheduledDays']
            departCityCode=mainCapacity['departCityCode']
            arriveCityCode=mainCapacity['arriveCityCode']
            departCityName=mainCapacity['departCityName']
            arriveCityName=mainCapacity['arriveCityName']
            sendBelongNetworkCode=mainCapacity['sendBelongNetworkCode']
            capacityName=mainCapacity['capacityName']
            capacityId=mainCapacity['capacityId']
            flightNo=mainCapacity['flightNo']
            flightNoI18n=mainCapacity['flightNoI18n']
            flightType=mainCapacity['flightType']
            getBillBatchNo=mainCapacity['getBillBatchNo']
            lineCode=mainCapacity['lineCode']
            planeType=mainCapacity['planeType']
            sendBillBatchNo=mainCapacity['sendBillBatchNo']
            uniqueCapKey=mainCapacity['uniqueCapKey']
            capKey=mainCapacity['capKey']
            countryCodeEnd=mainCapacity['countryCodeEnd']
            countryCodeStart=mainCapacity['countryCodeStart']
            deptId = getInfoByContractId(contractId)['dept_id']
            supplierId = getInfoByContractId(contractId)['contract_supplier_id']
            supplierId2 = getInfoByContractId(contractId)['contract_supplier_id_2']
            supplierId3 = getInfoByContractId(contractId)['contract_supplier_id_3']
            log.info(capacityName)
            log.info(supplierId)
            #维护合同运力
            self.addContractAndCapa(departCityCode, arriveCityCode, departCityName, arriveCityName, sendBelongNetworkCode,capacityName,capacityId, contractId,applicableScheduledDays,
                              countryCodeEnd, countryCodeStart, flightNo,flightNoI18n, flightType,getBillBatchNo, lineCode,planeType,sendBillBatchNo, uniqueCapKey, capKey)
            #维护舱位主数据
            self.addCabin(capacityName, departCityCode, arriveCityCode, deptId, sendBelongNetworkCode,capacityId, supplierId, supplierId2, supplierId3, contractId, capKey)
            #维护舱位货物类型
            self.addCabinCargoType(contractId, capacityName, departCityCode, arriveCityCode)



    #新增合同运力
    def addContractAndCapa(self,departCityCode, arriveCityCode, departCityName, arriveCityName, sendBelongNetworkCode, capacityName,
                          capacityId, contractId, applicableScheduledDays, countryCodeEnd, countryCodeStart, flightNo, flightNoI18n, flightType,
                          getBillBatchNo, lineCode, planeType, sendBillBatchNo, uniqueCapKey, capKey):
        if haveUsedCapacity(capacityName, departCityCode, arriveCityCode) and haveContractAndCapa(capacityName, departCityCode, arriveCityCode, contractId) == False:
            getBelongNetworkCode = getUsedCapacity(capacityName, departCityCode, arriveCityCode)[0]['get_belong_network_code']
            log.info('---'.join([capacityName, departCityCode, arriveCityCode, str(contractId)]) + '--不存在合同运力')
            print(('---'.join([capacityName, departCityCode, arriveCityCode, str(contractId)]) + '--不存在合同运力'))
            url, addCAndCJson = addContAndCapaJson(departCityCode, arriveCityCode, departCityName, arriveCityName,
                                                   sendBelongNetworkCode, getBelongNetworkCode, capacityName,
                                                   capacityId, contractId,applicableScheduledDays, countryCodeEnd,
                                                   countryCodeStart, flightNo,flightNoI18n,flightType, getBillBatchNo,
                                                   lineCode, planeType, sendBillBatchNo,uniqueCapKey, capKey)
            res = self.session.post(url=url, json=addCAndCJson, headers=self.headers, verify=False).json()
            log.info(res)

    # 若未维护舱位，则维护舱位
    def addCabin(self,capacityName, departCityCode, arriveCityCode, deptId, sendBelongNetworkCode,
                 capacityId,supplierId, supplierId2, supplierId3,contractId,capKey):
        contractType = getInfoByContractId(contractId)['contract_type']
        if haveUsedCapacity(capacityName, departCityCode, arriveCityCode) and haveAvaiableCabin(contractId, capacityName, departCityCode, arriveCityCode) == False and contractType==2:
            CurrentPlaneType = getUsedCapacity(capacityName, departCityCode, arriveCityCode)[0]['plane_type']
            getBelongNetworkCode = getUsedCapacity(capacityName, departCityCode, arriveCityCode)[0]['get_belong_network_code']
            log.info('---'.join([capacityName, departCityCode, arriveCityCode, str(contractId)]) + '--无舱位数据')
            removeUnAvaiableCabin(contractId, capacityName, departCityCode, arriveCityCode)
            avaiableCabinSpace = getMaxLoad(capacityName, departCityCode, arriveCityCode)
            setAvaiableCabin(capacityName, departCityCode, arriveCityCode, deptId, sendBelongNetworkCode,
                             avaiableCabinSpace, capacityId,
                             supplierId, supplierId2, supplierId3, getBelongNetworkCode, CurrentPlaneType, contractId,
                             capKey)
            log.info('---'.join([capacityName, departCityCode, arriveCityCode, str(contractId)]) + '--维护舱位主数据ok')


    #维护舱位货物类型
    def addCabinCargoType(self,contractId, capacityName, departCityCode, arriveCityCode):
        contractType = getInfoByContractId(contractId)['contract_type']
        if haveAvaiableCabin(contractId, capacityName, departCityCode, arriveCityCode) and contractType==2:
            avaiableCabinlist = getAvaiableCabin(contractId, capacityName, departCityCode, arriveCityCode)
            cabinId = avaiableCabinlist[0]['cabin_id']
            if haveNoCabinCargoType(cabinId):
                setCabinCargoType(cabinId)
                log.info('---'.join([capacityName, departCityCode, arriveCityCode, str(contractId)]) + '--维护舱位货物类型ok')


def addCnCarrPrice(contractId):
    contractAndCapacaityList=getContractAndCapacaity(contractId)
    contractType = getInfoByContractId(contractId)['contract_type']
    for contractAndCapacaity in contractAndCapacaityList:
        capacityName = contractAndCapacaity['capacity_name']
        departCityCode = contractAndCapacaity['depart_city_code']
        arriveCityCode = contractAndCapacaity['arrive_city_code']
        if haveUsedCapacity(capacityName, departCityCode, arriveCityCode) and contractType==2:
            capacityInfo = getUsedCapacity(capacityName, departCityCode, arriveCityCode)[0]
            departThrLetterCode = capacityInfo['depart_thr_letter_code']
            arriveThrLetterCode = capacityInfo['arrive_thr_letter_code']
            addCnSendPriceMain(capacityName, departCityCode, arriveCityCode, contractId, departThrLetterCode,arriveThrLetterCode)
            addCnCarrPriceItem(contractId, capacityName, departCityCode, arriveCityCode)

def addCnSendPriceMain(capacityName, departCityCode, arriveCityCode, contractId, departThrLetterCode,arriveThrLetterCode):
    if haveNoCnSendPrice(contractId, capacityName, departCityCode, arriveCityCode):
        setCnSendPriceMain(capacityName, departCityCode, arriveCityCode, contractId, departThrLetterCode,arriveThrLetterCode)
        log.info('--'.join([str(capacityName), str(departCityCode), str(arriveCityCode), str(departThrLetterCode), str(arriveThrLetterCode)]) + '主运价维护OK')

def addCnCarrPriceItem(contractId,capacityName,departCityCode, arriveCityCode):
    cnSendPriceMainList=getCnSendPriceMain(contractId,capacityName,departCityCode, arriveCityCode)
    contractItemList = getContractItemById(contractId)
    for cnSendPriceMain in cnSendPriceMainList:
        sendId=cnSendPriceMain['send_id']
        if haveNoCnSendPriceItem(sendId):
            CnSendPricePushToAir(sendId)
            for contractItem in contractItemList:
                supplierId=contractItem['supplier_id']
                serveCode = contractItem['serve_code']
                taxCode = contractItem['tax_code']
                supplierCode=getSupplierCode(supplierId)
                setCnSendPriceItem(sendId, supplierId, supplierCode, serveCode, taxCode)
                log.info('--'.join([str(sendId), str(supplierId), str(supplierCode), str(serveCode), taxCode])+'运价明细维护OK')


def removeCnSendPrice(contractId):
    removeCnSendPriceAtms(contractId)
    removeCnSendPriceAir(contractId)


def addKCgetBillByContractId(contractId):
    headers = {'Content-Type': 'application/json'}
    contractAndCapacaityList=getContractAndCapacaity(contractId)
    log.info(contractAndCapacaityList)
    startNum=1
    for contractAndCapacaity in contractAndCapacaityList:
        capacityName=contractAndCapacaity['capacity_name']
        if isCapacityExistCurrent(capacityName) == True:
            departThrLetterCode=getUsedCapacityByName(capacityName)['depart_thr_letter_code']
            arriveThrLetterCode=getUsedCapacityByName(capacityName)['arrive_thr_letter_code']
            kcOrderId = str(currentTm())[:8] + str(startNum).zfill(4)
            startNum += 1
            url, KcOrderInfo=KC_billData(kcOrderId,capacityName,departThrLetterCode,arriveThrLetterCode)
            log.info('新增KC提货url='+url)
            log.info('新增KC提货入参为---'+KcOrderInfo)
            res=requests.post(url=url,data=KcOrderInfo,headers=headers)
            log.info('新增KC之响应为---'+res.text)

#新增OS-CN国际提货任务
def addIairBillByContractId(contractId):
    contractAndCapacaityList = getContractAndCapacaity(contractId)
    log.info(contractAndCapacaityList)
    startNum = 1
    for contractAndCapacaity in contractAndCapacaityList:
        capacityName = contractAndCapacaity['capacity_name']
        if isCapacityExistCurrent(capacityName) == True:
            departThrLetterCode = getUsedCapacityByNameAndDate(capacityName)['depart_thr_letter_code']
            arriveThrLetterCode = getUsedCapacityByNameAndDate(capacityName)['arrive_thr_letter_code']
            actualFlyDate=getUsedCapacityByNameAndDate(capacityName)['lastest_arr_station_dt']
            actualArriveDate=getUsedCapacityByNameAndDate(capacityName)['plan_send_dt']
            IAirOrderId = str(currentTm())[:8] + str(startNum).zfill(4)
            startNum += 1
            url, headers, IairOrderInfo = Iair_billData(IAirOrderId,capacityName,departThrLetterCode,arriveThrLetterCode,actualFlyDate,actualArriveDate)
            log.info('新增Iair提货url=' + url)
            log.info('新增Iair提货入参为---' + IairOrderInfo)
            res = requests.post(url=url, data=IairOrderInfo, headers=headers)
            log.info('新增Iair之响应为---' + res.text)


def sendBillConformByTaskId():
    taskList=getSendBillData()
    for task in taskList:
        taskId=task['task_Id']
        sendBillConform(taskId)
    airVisitLog("/air/excuteAirJob/")


'''
isAgree=1---同意改配
isAgree=0---不同意改配
'''
def OEapproveBySendId(sendId,isAgree=1):
    businessId=getApprovingExceptionInfobySendId(sendId,'business_id')
    url,headers, OEapproveBody=OEapproveInfo(businessId,isAgree)
    log.info('发货ID='+str(sendId)+'调度审核信息='+OEapproveBody)
    res=requests.post(url=url, data=OEapproveBody, headers=headers)
    log.info('发货ID='+str(sendId)+'接收调度Air处理结果'+res.text)
