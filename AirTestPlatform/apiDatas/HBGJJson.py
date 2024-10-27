'''
# @Author  : No.47
# @Time    : 2023/12/14 10:27
# @Function: 
'''


# 全量动态
import json
import time
import uuid

from common.Tools import now, sf_signature, bjtm


def hbgjCommonParam():
    APP_SECRET = 'appid4hbgjSecret'
    APP_ID = 'appid4hbgj'
    #航班管家向DI推送全量航班动态url
    urlDynamic = 'http://di-api.intsit.sfcloud.local:1080/airais-open-api/flight/fullFlightDynamicInfo'
    # 航班管家向DI推送订阅航班动态url
    urlSubDynamicInfo = "http://di-api.intsit.sfcloud.local:1080/airais-open-api/flight/subFlightDynamicInfo"
    proxies = {"http": None, "https": None}
    return APP_SECRET,APP_ID,urlDynamic,urlSubDynamicInfo,proxies

#航班计划-国内

#航班计划-国际


#全量动态报文
def dynamicInfo(capacityName,sendDate,departThrLetterCode,arriveThrLetterCode,planFlyDepartTm,
                actualFlyTm,planeType,capacityState,planArriveTm,actualArriveTm,depCity,arrCity):
    APP_SECRET, APP_ID, urlDynamic, urlSubDynamicInfo, proxies = hbgjCommonParam()
    timestamp = now()
    createTm=bjtm()
    nonce = str(uuid.uuid4())
    uri = '/airais-open-api/flight/fullFlightDynamicInfo'
    sign = sf_signature(APP_ID, APP_SECRET, uri, timestamp, nonce)
    headers = {
        'appId': APP_ID,
        'timestamp': timestamp,
        'nonce': nonce,
        'sign': sign,
        'Content-Type': 'application/json'
    }
    signStrList=[capacityName,str(sendDate),departThrLetterCode,arriveThrLetterCode,capacityState]
    signStr='-'.join(signStrList)
    dynamicInfo = {
        "data": [
            {
                "capacityName": capacityName,
                "sendDateLocal": sendDate,
                "sendDate": sendDate,
                "departThrLetterCode": departThrLetterCode,
                "arriveThrLetterCode": arriveThrLetterCode,
                "planFlyDepartTm": planFlyDepartTm,
                "actualFlyTm": actualFlyTm,
                "planeType": planeType,
                "capacityState": capacityState,
                "planArriveTm": planArriveTm,
                "actualArriveTm": actualArriveTm,
                "depZone": "GMT+08:00",
                "arrZone": "GMT+08:00",
                "alterInfo": "",
                "airlineInter": "0",
                "depActTime": actualFlyTm,
                "arrActTime": actualArriveTm,
                "passenger": 1,
                "serviceType": "J",
                "gate": "14",
                "boardingSeat": "",
                "depRate": "",
                "arrRate": "",
                "stop": "",
                "boardingRometing": "0",
                "depCity": depCity,
                "arrCity": arrCity,
                "shareFlag": 1,
                "arrStand": "",
                "arrRemotingFlag": "0",
                # "preFlight": {
                #     "date": "2022-12-12",
                #     "flightNo": "CA8144",
                #     "depCode": "TFU",
                #     "arrCode": "HET"
                # },
                # "followFlight": {
                #     "date": "2022-12-14",
                #     "flightNo": "CA8134",
                #     "depCode": "TGO",
                #     "arrCode": "HET"
                # },
                "aobt": createTm,
                "aibt": "",
                "createTm": timestamp,
                "signStr": signStr
            }
        ]
    }
    dataDynamicInfo=json.dumps(dynamicInfo)
    return urlDynamic, headers, dataDynamicInfo, proxies


#订阅动态
def subDynamicInfo(capacityName,sendDate,departThrLetterCode,arriveThrLetterCode,planFlyDepartTm,
                actualFlyTm,planeType,capacityState,planArriveTm,actualArriveTm):
    APP_SECRET, APP_ID, urlDynamic, urlSubDynamicInfo, proxies=hbgjCommonParam()
    timestamp = str(int(round(time.time() * 1000)))
    nonce = str(uuid.uuid4())
    uri = '/airais-open-api/flight/subFlightDynamicInfo'
    sign = sf_signature(APP_ID, APP_SECRET, uri, timestamp, nonce)
    headers = {
        'appId': APP_ID,
        'timestamp': timestamp,
        'nonce': nonce,
        'sign': sign,
        'Content-Type': 'application/json'
    }
    dataSubDynamicInfo = {
        "capacityName": capacityName,
        "sendDateLocal": sendDate,
        "sendDate": sendDate,
        "departThrLetterCode": departThrLetterCode,
        "arriveThrLetterCode": arriveThrLetterCode,
        "planFlyDepartTm": planFlyDepartTm,
        "actualFlyTm": actualFlyTm,
        "planeType": planeType,
        "capacityState": capacityState,
        "planArriveTm": planArriveTm,
        "actualArriveTm": actualArriveTm,
        "depZone": "GMT+08:00",
        "arrZone": "GMT+08:00",
        "alterInfo": "",
        "airlineInter": "0",
        "depActTime": actualFlyTm,
        "arrActTime": actualArriveTm,
        "passenger": "J",
        "createTm": timestamp,
        "msg": ""}
    return urlSubDynamicInfo,headers,dataSubDynamicInfo,proxies

