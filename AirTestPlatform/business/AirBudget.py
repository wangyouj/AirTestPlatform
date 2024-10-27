import logging
from threading import currentThread

from common.Tools import export_to_local, airThreadRun, currentTm
from config.DBconfig import db_airOpen
from mapper.AirOpenSql import get_city_info, insert_budget_data, init_budget_data, export_budget_data_sql

log = logging.getLogger('log')


def product_budget_data(areaCode):
    '''
    按责任区生成数据
    :param areaCode: 始发责任区
    :return:
    '''
    print("%s is running " % currentThread().getName())

    # 满足责任区配置、城市配置、网点配置的始发城市列表
    sendCityList = get_city_info(areaCode)
    print(sendCityList)
    codes = set(item['cost_quality_area_code'] for item in sendCityList)
    print(codes)
    print(list(codes))
    # 满足责任区配置、城市配置、网点配置的目的城市列表
    getCityList = get_city_info()

    for sendCity in sendCityList:
        departAreaCode = sendCity['AREA_CODE']
        departArea = sendCity['cost_quality_area_code']
        departCityCode = sendCity['dist_code']
        departCityName = sendCity['dist_name']
        for getCity in getCityList:
            arriveArea = getCity['cost_quality_area_code']
            arriveCityCode = getCity['dist_code']
            arriveCityName = getCity['dist_name']
            # 判断始发目的地是否相同，不相同则生成预算
            if arriveCityCode != departCityCode:
                insert_budget_data(departAreaCode, departArea, departCityCode, departCityName, arriveArea,
                                   arriveCityCode,
                                   arriveCityName)


# TODO 多线程工具封装
# def product_budget_data_theads():
#     # 根据地区分组，每个地区独立一个线程
#     CityList = get_city_info()
#     codes = set(item['cost_quality_area_code'] for item in CityList)
#     areaCodeList = list(codes)
#     print(areaCodeList)
#
#     start = time.time()
#     executor = ThreadPoolExecutor(10)  # 线程池
#
#     res = []
#     for areaCode in areaCodeList:  # 开启10个任务
#         future = executor.submit(product_budget_data, areaCode)  # 异步提交任务
#         res.append(future)
#
#     executor.shutdown()  # 等待所有线程执行完毕
#     print("++++>")
#     for r in res:
#         print(r.result())  # 打印结果
#     end = time.time()
#     print(end - start)


def product_budget_data_theads():
    # 根据地区分组，每个地区独立一个线程
    CityList = get_city_info()
    codes = set(item['cost_quality_area_code'] for item in CityList)
    areaCodeList = list(codes)
    print(areaCodeList)
    threadCount=len(areaCodeList)
    print('threadCount==================='+str(threadCount))
    airThreadRun(product_budget_data, threadCount, areaCodeList)


# 将生成的数据导出为本地excel文件
def export_budget_test_data():
    # 对应数据库
    db = db_airOpen()
    # 导出脚本
    exportBudgetDataSql, data = export_budget_data_sql()
    # 导出路径
    file_path = 'D:/2024版本/预算管理/预算管理数据明细V{0}.xlsx'.format(str(currentTm()))
    # 导出
    export_to_local(db, exportBudgetDataSql, file_path)


def product_and_export_budget_data():
    # 初始化数据表
    init_budget_data()
    # 执行数据生成
    product_budget_data_theads()
    # 执行导出
    export_budget_test_data()
