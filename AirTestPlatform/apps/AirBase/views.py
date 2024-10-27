import json
import logging
from math import ceil

import requests
from django.http import HttpResponse

from apiDatas.RequestData import OEapproveInfo
from common.ApiUtil import queryStandardReponse, standardReponse, ApiReponse
from mapper.AirTaskSql import getDispatchData
from mapper.TaskConfigSql import getAirSysConfig

# Create your views here.
log = logging.getLogger('log')


def downloadSubdivisionData(request):
    '''
    请求示例
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


'''
@function:查询air测试平台系统配置
请求示例：
{
"currentPage":1,
"pageSize":10
}
'''
def queryAirSysConfig(request):
    '''
    Air测试平台系统配置查询入口
    :param request:
    :return:
    '''
    print(request.body)
    if request.method=='POST':
        req=json.loads(request.body)
        log.info(req)
        currentPage=req['currentPage']
        pageSize=req['pageSize']
        result,total=getAirSysConfig(currentPage,pageSize)
        airReponse=queryStandardReponse(total=total,pages=ceil(total/pageSize),currentPage=currentPage,content=result)
        return ApiReponse(airReponse)
    else:
        return HttpResponse('参数错误')

def queryDispatchData(request):
    '''
    OE调令数据查询入口
    :param request:
    :return:
    '''
    print(request.body)
    if request.method=='POST':
        req=json.loads(request.body)
        log.info(req)
        businessId=req['businessId']
        sendId=req['sendId']
        exceptionId=req['exceptionId']
        currentPage=req['currentPage']
        pageSize=req['pageSize']
        result,total=getDispatchData(businessId, sendId, exceptionId, currentPage, pageSize)
        log.info(type(result))
        airReponse=queryStandardReponse(total=total,pages=ceil(total/pageSize),currentPage=currentPage,content=result)
        return ApiReponse(airReponse)
    else:
        return HttpResponse('参数错误')

def OEApprove(request):
    '''
    OE审核、驳回入口
    :param request:
    :return:
    '''
    print(request.body)
    if request.method == 'POST':
        reqData = json.loads(request.body)
        log.info(reqData)
        url, headers = OEapproveInfo()
        res = requests.post(url=url, data=json.dumps(reqData), headers=headers)
        log.info(res.text)
        airReponse=standardReponse(content=res.text)
        return ApiReponse(airReponse)
    else:
        return HttpResponse('参数错误')
