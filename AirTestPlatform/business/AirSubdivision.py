'''
散航分舱
本项完成作业内容为：
1-实现接口调用
2-解析返回结果
3-将返回结果写入本地excel
'''
import pandas as pd
import requests

from apiDatas.RequestData import getSubdivisionResult
from common.Tools import bjtm


# 获取分舱结果
def getSubdivisionData():
    url, getSubdivisionJson = getSubdivisionResult()
    res = requests.post(url=url, json=getSubdivisionJson, verify=False).json()
    return res


# TODO 爬虫工具封装
# 解析分舱结果并将结果写入excel
def putSubdivisionDataToLocal():
    '''
    解析http响应数据并存储至本地文件
    :return:
    '''
    result = getSubdivisionData()
    # 解析返回结果-获取业务数据列表
    dataList = result['result']['records']
    # 预导出列名转化
    column_names = {
        "id": "主键ID",
        "spaceId": "舱位ID",
        "siteCode": "场地代码",
        "planSendBatchDt": "班次日期",
        "planSendBatch": "计划发出班次",
        "departDeptCode": "始发网点",
        "departCityCode": "始发城市代码",
        "arriveDeptCode": "目的网点",
        "arriveCityCode": "目的城市代码",
        "departThrLetterCode": "始发机场",
        "arriveThrLetterCode": "目的机场",
        "capacityName": "航班号",
        "scheduleFlightType": "时效类型",
        "planSendDt": "计飞",
        "planArriveDt": "计达",
        "flightDate": "航班日期",
        "supplierIds": "供应商ID组合",
        "routeCode": "路由码",
        "cargoCityCode": "配载代码",
        "cargoTransitDepotCode": "",
        "subdivisionSpaceAmount": "分舱量",
        "waybillWeightTotal": "",
        "createdEmpCode": "操作人工号",
        "createdTm": "创建时间",
        "modifiedEmpCode": "",
        "modifiedTm": "修改时间",
        "controlType": "限量类型",
        "effectiveDate": "生效日期",
        "uniqueKey": "舱位-场地",
        "supplierNames": "供应商组合",
        "goodsType": "获取类型"
    }
    # 将JSON数据转换为DataFrame
    df = pd.DataFrame(dataList, columns=column_names.keys())  # 初始时列名是英文
    # 现在，你可以使用字典来替换列名
    df.columns = column_names.values()

    # 将JSON数据转换为DataFrame
    # df = pd.DataFrame(dataList)
    file_path = 'D:/2024版本/预算管理/分舱明细V{0}.xlsx'.format(str(bjtm()))
    # 将DataFrame写入Excel文件
    df.to_excel(file_path, index=False)

# print(getSubdivisionData())
