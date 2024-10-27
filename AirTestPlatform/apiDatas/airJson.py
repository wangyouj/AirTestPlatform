
import json
import random
import string

from common.Tools import bjtm, getOrderNo, sysDate, markNum, mainNum


#专享急件需求
def requirementJson(flightNo, sendDate,srcAirport,desAirport):
    demand={
    "requireId": None,
    "sendBatchDt": "{}".format(sendDate),
    "departThrLetterCode": "{}".format(srcAirport),
    "arriveThrLetterCode": "{}".format(desAirport),
    "serviceMode": "3",
    "serviceOrganization": "1",
    "operatorEmp": "01386333",
    "operatorTime": "{}".format(bjtm()),
    "flightNoList": [flightNo],
    "wayBillList": [
    {
    "waybillNo": "{}".format(getOrderNo()),
    "demandTotalGeneral":"" ,
    "demandTotalAlive": "",
    "demandTotalFresh": "",
    "demandTotalTa": 100,
    "operatorType": "1"
    },
    {
    "waybillNo": "{}".format(getOrderNo(1)),
    "demandTotalGeneral":200 ,
    "demandTotalAlive": "",
    "demandTotalFresh": "",
    "demandTotalTa": "",
    "operatorType": "1"
    },
    {
    "waybillNo": "{}".format(getOrderNo(2)),
    "demandTotalGeneral":"" ,
    "demandTotalAlive": 399,
    "demandTotalFresh": "",
    "demandTotalTa": "",
    "operatorType": "1"
    },
    {
    "waybillNo": "{}".format(getOrderNo(3)),
    "demandTotalGeneral":"" ,
    "demandTotalAlive": "",
    "demandTotalFresh": 277,
    "demandTotalTa": "",
    "operatorType": "1"
    }
    ]
    }
    return json.dumps(demand)

#机场一个码
def OneCodeKafka(taskId,containerNo,virtualContainerNo,oneCode):
    oneCodekafka={
    "taskId":"{}".format(taskId),
    "status":1,
    "operatorNo":"01386333",
    "containerNo":"{}".format(containerNo),
    "virtualContainerNo":"{}".format(virtualContainerNo),
    "createContainerTime":"{}".format(bjtm()),
    "finishContainerTime":"{}".format(bjtm()),
    "goodsInfo":oneCode}
    return json.dumps(oneCodekafka)
#查询需求
def queryRequirements(network,n=1):
    url='http://shiva-trtms-air-service-web.sit.sf-express.com/air/requirement/bookingmanger/planRequirementList'
    sendBatchDt = sysDate(n)
    requirementParm={
    "departDeptCodes":network,
    "sendBatchDtStartStr":"{}".format(sendBatchDt),
    "sendBatchDtEndStr":"{}".format(sendBatchDt),
    "arriveDeptCode":"",
    "temporyRequirementClick":"false",
    "invalidLineClick":"false",
    "planRequirementClick":"false",
    "pageNum":1,
    "pageSize":1000}
    return url,requirementParm

#新增合同运力
def addContAndCapaJson(departCityCode,arriveCityCode,departCityName,arriveCityName,
                       sendBelongNetworkCode,getBelongNetworkCode,capacityName,capacityId,contractId,
                       applicableScheduledDays,countryCodeEnd,countryCodeStart,flightNo,flightNoI18n,
                       flightType,getBillBatchNo,lineCode,planeType,sendBillBatchNo,uniqueCapKey,capKey):
    url = 'http://air-atms-core.sit.sf-express.com/sys/air-atms-core-contract/contract/addContAndCapa'
    addCAndCJson={
    "departCityCode":departCityCode,
    "arriveCityCode":arriveCityCode,
    "departCityName":departCityName,
    "arriveCityName":arriveCityName,
    "sendBelongNetworkCode":sendBelongNetworkCode,
    "getBelongNetworkCode":getBelongNetworkCode,
    "capacityName":capacityName,
    "capacityId":capacityId,
    "contractId":contractId,
    "capacityNames":{
        "applicableScheduledDays":applicableScheduledDays,
        "arriveCityCode":arriveCityCode,
        "arriveCityName":arriveCityName,
        "capKey":capKey,
        "capacityId":capacityId,
        "capacityName":capacityName,
        "capacityType":"2",
        "countryCodeEnd":countryCodeEnd,
        "countryCodeStart":countryCodeStart,
        "departCityCode":departCityCode,
        "departCityName":departCityName,
        "flightNo":flightNo,
        "flightNoI18n":flightNoI18n,
        "flightType":flightType,
        "getBelongNetworkCode":getBelongNetworkCode,
        "getBillBatchNo":getBillBatchNo,
        "lineCode":lineCode,
        "planeType":planeType,
        "sendBelongNetworkCode":sendBelongNetworkCode,
        "sendBillBatchNo":sendBillBatchNo,
        "uniqueCapKey":uniqueCapKey,
        "scheduleFlightType": None,
        "flag": None,
        "deptCode": None,
        "departThrLetterCode": None,
        "contractType": None,
        "capacityNames": None,
        "arriveThrLetterCode": None,
        "utilType": None
    },
    "contrastRate":"",
    "flightType":"1",
    "pullTransportType":1,
    "isNotReturnFloorHandle":"0",
    "isGetReturnServiceFee":"0",
    "shortBarge":"2",
    "scheduledDay1":"",
    "scheduledDay2":"",
    "scheduledDay3":"",
    "scheduledDay4":"",
    "scheduledDay5":"",
    "scheduledDay6":"",
    "scheduledDay7":"",
    "courseRatingStr":"{}".format(random.randint(1,10))
}
    return url,addCAndCJson


#获取运力维度
def getCapaList(deptCode,contractType):
    url='http://air-atms-core.sit.sf-express.com/sys/air-atms-core-contract/contract/listContractCapacity'
    getCapaListJson={
    "flightNo":"",
    "pageStart":1,
    "pageSize":500,
    "departCityCode":None,
    "arriveCityCode":None,
    "capacityType":2,
    "contractType":contractType,
    "deptCode":deptCode
}
    return url,getCapaListJson


def addAvaiableCabinData(capacityName,arriveCityCode,departCityCode,
                         contractId,supplierId,supplierId2,supplierId3,deptId,sendBelongNetworkCode,
                         getBelongNetworkCode,planeType,avaiableCabinSpace):
    urlX='http://shiva-trtms-air-p.sit.sf-express.com/air/avaiableCabin/save.arz'
    effectiveDate=sysDate()
    addAvaiableCabinJson={
    "avaiableCabin":{
        "effectiveDate":effectiveDate,
        "expirationDate":"2028-12-01",
        "capacityName":capacityName,
        "sDay1":"1",
        "sDay2":"2",
        "sDay3":"3",
        "sDay4":"4",
        "sDay5":"5",
        "sDay6":"6",
        "sDay7":"7",
        "isProtocolFlight":"2",
        "cargoTypes":"1,2,3,5,6,19,20,21",
        "scheduledDays":"1234567",
        "arriveCityCode":arriveCityCode,
        "departCityCode":departCityCode,
        "supplierNames":"",
        "contractId":"{}".format(contractId),
        "supplierId":"{}".format(supplierId),
        "supplierId2":"{}".format(supplierId2),
        "supplierId3":"{}".format(supplierId3),
        "supplierName":"",
        "deptId":"{}".format(deptId),
        "sendBelongNetworkCode":"{}".format(sendBelongNetworkCode),
        "getBelongNetworkCode":"{}".format(getBelongNetworkCode),
        "deptCode":"{}".format(sendBelongNetworkCode),
        "dataSource":1,
        "preCheckSpace":1,
        "avaiableCabinDetailList":[
            {
                "planeType":planeType,
                "avaiableCabinSpace":avaiableCabinSpace,
                "editing": False
            }
        ]
    }
}
    return urlX,addAvaiableCabinJson

#发起订舱-计算结果大于0部分每天自动发起
def sendSpaceApplyData(ids,relationIds):
    url='http://shiva-trtms-air-service-web.sit.sf-express.com/air/book/aibssSpace/sendSpaceApply'
    sendSpaceApplyJson={"id":ids,"relationIds":relationIds,"sureCostWarning":1}
    return url,sendSpaceApplyJson


#生成任务
def addTaskData(ids,relationIds):
    url='http://shiva-trtms-air-service-web.sit.sf-express.com/air/book/aibssSpace/addTask'
    addTaskJson={"id":ids,"relationIds":relationIds}
    return url,addTaskJson

#发起OE
def OE_demand(flight_info, cur_date):
    data = []
    shunt_id = []
    print(flight_info)
    oe_info ={
            "shuntId": "OE-0831{}".format(str(''.join(random.sample(string.digits, 5)))),
            "capacityType": "1",
            "departCityCode": flight_info['departCityCode'],
            "departDeptCode": flight_info['departDeptCode'],
            "capacityName": flight_info['capacity_name'],
            "arriveCityCode": flight_info['arriveCityCode'],
            "arriveDeptCode": flight_info['arriveDeptCode'],
            "scheduleFlightType": flight_info['scheduleFlightType'],
            "sendBatch": flight_info['sendBillBatchNo'],
            "sendBatchDt": cur_date,
            "aliveWeight": "800",
            "freshWeight": "500",
            "generalWeight": "300",
            "otherWeight": "400",
            "weightTotal": "2000",
            "maintainEmpCode": "01386333",
            "maintainTm": cur_date,
            "source": "3",
            "serviceMode": "1",
            "taskId": "2022{}".format(str(''.join(random.sample(string.digits, 5)))),
            "exceptionId": "0831{}".format(str(''.join(random.sample(string.digits, 5))))
            }
    data.append(oe_info)
    shunt_id.append(oe_info['shuntId'])
    url = 'http://shiva-trtms-air-service-gateway.intsit.sfcloud.local:1080/inner/air/requirement/openApi/receive/airTemporaryDispatch'
    return url,data

#新增KC提货
def KC_billData(kcOrderId,capacityName,departThrLetterCode,arriveThrLetterCode):
    markNumber=markNum()
    mainNumber=mainNum()
    sendDate=sysDate()
    url='http://shiva-trtms-air-service-task.intsit.sfcloud.local/air/task/getBillOrder/saveGetBillOrder'
    KcOrderInfo={
    "kcOrderId":int(kcOrderId),
    "capacityName":"{}".format(capacityName),
    "sendDate":"{}".format(sendDate),
    "departThrLetterCode":"{}".format(departThrLetterCode),
    "arriveThrLetterCode":"{}".format(arriveThrLetterCode),
    "mainNumber":"{}".format(mainNumber),
    "sendCount":random.randint(10,66),
    "sendWeight":random.randint(100,999),
    "chargeWeight":random.randint(100,999),
    "goodsStowageType":"2",
    "markNumber":"{}".format(markNumber),
    "actualFlyDate":"",
    "actualArriveDate":"",
    "isSupp":1,
    "remark":"47-AddKcByTest",
    "userName":"KC-47",
    "srcData":1
}
    return url,json.dumps(KcOrderInfo)

def airVisit(visiturl):
    url='http://traffic.sit.sf-express.com/api/visitlog/visitrecord/'
    visitLog={"visiturl": visiturl,"system":"air"}
    return url,visitLog

#Iair-OS→CN提货
def Iair_billData(IAirOrderId,capacityName,departThrLetterCode,arriveThrLetterCode,actualFlyDate,actualArriveDate):
    url='http://10.206.170.7/air/task/iair/sendBill/save'
    headers = {'Content-Type': 'application/json'}
    markNumber = markNum()
    mainNumber = mainNum()
    sendDate = sysDate()
    IairOrderInfo={
      "iAirOrderId": "{}".format(IAirOrderId),
      "capacityName": "{}".format(capacityName),
      "sendDate": "{}".format(sendDate),
      "departThrLetterCode": "{}".format(departThrLetterCode),
      "arriveThrLetterCode": "{}".format(arriveThrLetterCode),
      "mainNumber": "{}".format(mainNumber),
      "sendCount": random.randint(10,66),
      "sendWeight": random.randint(100,199),
      "chargeWeight": random.randint(100,199),
      "goodsStowageType": 2,
      "markNumber": "{}".format(markNumber),
      "actualFlyDate": "{}".format(actualFlyDate),
      "actualArriveDate": "{}".format(actualArriveDate),
      "planSendDt": "{}".format(sendDate),
      "planArrDt": "{}".format(sendDate),
      "isSupp": 0,
      "remark": "IAir提货造数",
      "state": 1,
      "operator": "test",
      "isCheck": 0,
      "auditTm": "",
      "auditor": "",
      "rejectRemark": "",
      "loadingNumber": 10,
      "loadingDelivery": 10
    }
    return url,headers,IairOrderInfo

def initProxyConfig():
    sysTm=bjtm()
    url='http://10.206.169.1/air/base/proxyConfig/update'
    initProxyConfigJson={
    "aibssProxyConfigInfoList":[
        {
            "cargoTypePriority":1,
            "createdEmpCode":"847790",
            "createdTm":"2023-05-22 14:23:22",
            "id":4811,
            "modifiedEmpCode":"847790",
            "modifiedTm":"{}".format(sysTm),
            "proxyKey":"010R_10101000167485_1",
            "sendBelongNetworkCode":"010R",
            "settleCargoType":"1",
            "spaceType":"F",
            "supplierId":10101000167485
        },
        {
            "cargoTypePriority":2,
            "createdEmpCode":"847790",
            "createdTm":"2023-05-22 14:23:22",
            "id":4812,
            "modifiedEmpCode":"847790",
            "modifiedTm":"{}".format(sysTm),
            "proxyKey":"010R_10101000167485_2",
            "sendBelongNetworkCode":"010R",
            "settleCargoType":"2",
            "spaceType":"F",
            "supplierId":10101000167485
        },
        {
            "cargoTypePriority":3,
            "createdEmpCode":"847790",
            "createdTm":"2023-05-22 14:23:22",
            "id":4813,
            "modifiedEmpCode":"847790",
            "modifiedTm":"{}".format(sysTm),
            "proxyKey":"010R_10101000167485_3",
            "sendBelongNetworkCode":"010R",
            "settleCargoType":"3",
            "spaceType":"F",
            "supplierId":10101000167485
        },
        {
            "cargoTypePriority":4,
            "createdEmpCode":"847790",
            "createdTm":"2023-05-22 14:23:22",
            "id":4814,
            "modifiedEmpCode":"847790",
            "modifiedTm":"{}".format(sysTm),
            "proxyKey":"010R_10101000167485_5",
            "sendBelongNetworkCode":"010R",
            "settleCargoType":"5",
            "spaceType":"F",
            "supplierId":10101000167485
        },
        {
            "cargoTypePriority":5,
            "createdEmpCode":"847790",
            "createdTm":"2023-05-22 14:23:22",
            "id":4815,
            "modifiedEmpCode":"847790",
            "modifiedTm":"{}".format(sysTm),
            "proxyKey":"010R_10101000167485_19",
            "sendBelongNetworkCode":"010R",
            "settleCargoType":"19",
            "spaceType":"F",
            "supplierId":10101000167485
        },
        {
            "cargoTypePriority":6,
            "createdEmpCode":"847790",
            "createdTm":"2023-05-22 14:23:22",
            "id":4816,
            "modifiedEmpCode":"847790",
            "modifiedTm":"{}".format(sysTm),
            "proxyKey":"010R_10101000167485_20",
            "sendBelongNetworkCode":"010R",
            "settleCargoType":"20",
            "spaceType":"F",
            "supplierId":10101000167485
        },
        {
            "cargoTypePriority":7,
            "createdEmpCode":"847790",
            "createdTm":"2023-05-22 14:23:22",
            "id":4817,
            "modifiedEmpCode":"847790",
            "modifiedTm":"{}".format(sysTm),
            "proxyKey":"010R_10101000167485_21",
            "sendBelongNetworkCode":"010R",
            "settleCargoType":"21",
            "spaceType":"F",
            "supplierId":10101000167485
        }
    ],
    "areaName":"华北分拨区",
    "cargoTypePriority":None,
    "ccEmailAddr":"",
    "ccEmailAddr1":"",
    "createdEmpCode":"847790",
    "createdTm":"2023-05-12 15:21:54",
    "createdTmString":"2023-05-12 15:21:54",
    "departCityCode":"010",
    "departCityName":"北京",
    "emailAddr":"",
    "emailAddr1":"",
    "id":3072,
    "interfaceType":"3",
    "interfaceType1":"3",
    "interfaceType1Str":"ACP",
    "interfaceType2":"3",
    "interfaceType2Str":"ACP",
    "interfaceType3":"3",
    "interfaceType3Str":"ACP",
    "interfaceTypeStr":"ACP",
    "isRange":1,
    "isRange1":1,
    "isRange1S":"",
    "isRange1Str":"是",
    "isRange2":1,
    "isRange2S":"",
    "isRange2Str":"是",
    "isRange3":1,
    "isRange3S":"",
    "isRange3Str":"是",
    "isRangeS":"",
    "isRangeStr":"是",
    "modifiedEmpCode":"Test",
    "modifiedTm":"{}".format(sysTm),
    "modifiedTmString":"{}".format(sysTm),
    "sendBelongNetworkCode":"010R",
    "settleCargoType":"",
    "settleCargoTypeImportStr":"",
    "settleCargoTypeStr":"",
    "settleCargoTypeString":"",
    "spaceType":"",
    "supplierId":10101000167485,
    "supplierName":"西班牙军工集团",
    "synchronizedTime":"{}".format(sysTm),
}
    return url,initProxyConfigJson


def OEapproveInfo(businessId,isAgree=1):
    url='http://10.206.170.7/air/task/billTaskException/receiveOeDispatchNew'
    headers = {'Content-Type': 'application/json'}
    OEapproveBody={
    "businessId": "{}".format(businessId),
    "isAgree": isAgree,
    "dispatchId": None}
    return url,headers,OEapproveBody


def hbgjPushSubDynamicInfo():
    url='http://traffic.sit.sf-express.com/api/air/pushSubDynamicInfo/'