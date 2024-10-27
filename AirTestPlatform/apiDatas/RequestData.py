
#获取散航分舱结果url及参数
def getSubdivisionResult():
    url = 'http://shiva-trtms-air-service-gateway.intsit.sfcloud.local:1080/inner/air/subdivision/tdop/findTaskList'
    getSubdivisionJson = {
        "operatorNo": "01386333",
        "siteCode": "755W",
        "flightDt": "2024-07-27",
        "currentPage": "1",
        "pageSize": "1000"
    }
    return url, getSubdivisionJson


def OEapproveInfo():
    url='http://10.206.170.7/air/task/billTaskException/receiveOeDispatchNew'
    headers = {'Content-Type': 'application/json'}
    return url,headers