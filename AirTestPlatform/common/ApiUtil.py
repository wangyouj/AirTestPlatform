'''
@author: No.47
@file: ApiUtil.py
@time: 2024/8/16 19:00
@desc: API处理通用
'''

import json
import logging
import pandas as pd
import xlsxwriter
from io import BytesIO
from datetime import datetime
from django.http import HttpResponse
from common.DBUtil import DBUtil

log = logging.getLogger('log')


class ComplexEncoder(json.JSONEncoder):
    '''
    python对象json化工具
    '''

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# TODO 字段名标准化部分数据不兼容问题处理
def dataTransformed(content):
    '''
    将数据库字段名统一转为驼峰式
    :param content: 需要转换的数据--为sql查询后的默认数据类型-dict
    :return: 字段名格式化之后的字典
    '''
    df = pd.DataFrame(content)
    # 字段名-转大骆驼格式 如FlightNo
    df = df.rename(columns=lambda x: x.replace('_', ' ').title().replace(' ', '')).reset_index(drop=True)
    return df.to_dict(orient='records')


# TODO 异常处理：当前页超出总页数？
def standardQuery(DB, dataSql, countSql, currentPage, pageSize):
    '''
    通用查询-获取查询结果-数据量-页数等，支持分页
    :param DB: 指定实例-统一配置于DBconfig.py
    :param dataSql: 获取查询结果的SQL，注意：脚本后不可带’;‘,否则分页异常
    :param countSql: 获取数据量的SQL
    :param currentPage: 当前页
    :param pageSize: 单页数据条数
    :return: 数据列表、数据量
    '''
    start = (currentPage - 1) * pageSize
    # 查询数据项sql-处理分页
    dataSql = dataSql + ' limit {0},{1};'.format(start, pageSize)
    countSql = countSql
    result = DBUtil(DB, dataSql)
    total = DBUtil(DB, countSql)[0]['count(*)']
    return result, total

# TODO 自定义响应码规范化 根据业务场景提供响应码及msg
# 定义统一数据返回格式
def standardReponse(code='00', msg='successful!', content=[]):
    '''
    非查询类标准返回，前端依据code定义弹窗样式，并取msg显示
    :param code: 响应码
    :param msg: 响应信息
    :param content: 响应体-自由扩展
    :return: json化的python对象
    '''
    result = {"code": code, "msg": msg, "content": content}
    return json.dumps(result, cls=ComplexEncoder)


# 定义统一查询接口数据返回格式
def queryStandardReponse(code='00', msg='successful!', total=0, pages=0, currentPage=1, content=[]):
    '''
    查询类接口标准返回,前端依据code定义弹窗样式，并取msg显示,取content部分展示在界面
    :param code: 响应码
    :param msg: 响应信息
    :param total: 总数据条数
    :param pages: 总页数
    :param currentPage: 当前页
    :param content: 查询结果
    :return: json化的python对象
    '''
    result = {"code": code, "msg": msg, "total": total, "pages": pages, "currentPage": currentPage, "content": content}
    return json.dumps(result, cls=ComplexEncoder)


def taskManageReponse(code='00',msg='successful!'):
    result={"code":code,"msg":msg}
    return json.dumps(result,cls=ComplexEncoder)

def ApiReponse(airReponse):
    '''
    http请求统一响应
    :param airReponse: 上文定义的standardReponse、taskManageReponse 或者 queryStandardReponse也可根据需要扩展新的格式
    :return:
    '''
    return HttpResponse(airReponse, content_type='application/json', charset='utf-8')


def downloadResponse(data, fileName='DefaultFileName', sheetName='DefaultSheetName', columnMap=None):
    '''
    远程下载-通用方法
    依赖工具包：pip install openpyxl
    :param data: 需要下载的数据，需为list；如 [{'name': 'wyj', 'ID': 1386333},{'name': 'No-47', 'ID': 47}]
    :param fileName: 下载的文件名
    :param sheetName: excel文件的sheet名
    :param columnMap: 字典-data数据如果需要做列名映射，存放在columnMap;列名映射字典,如{'name': '姓名', 'ID': '工号'}
                    若指定columnMap，需确保map中包含导出字段的所有列名，否则对应列名在导出结果中为空
    :return:
    '''
    # 预下载数据
    data = data
    # 列名字典
    column_map = columnMap
    # 创建一个BytesIO对象来存储Excel文件
    buffer = BytesIO()
    # 创建Excel工作簿
    workbook = xlsxwriter.Workbook(buffer)
    # 创建一个工作表
    worksheet = workbook.add_worksheet(sheetName)

    if columnMap == None:
        # 写入列名--当不需要单独定义字段名-列名字典时使用
        for j, col_name in enumerate(data[0].keys(), start=0):
            worksheet.write(0, j, col_name)  # 添加标题行
    else:
        # 写入列名--当需要自定义字段名与列名字典时使用
        for j, col_name in enumerate(column_map.values(), start=0):
            worksheet.write(0, j, col_name)  # 添加标题行

    # 写入数据-需从第2行开始写入，否则会覆盖表头
    for i, row in enumerate(data, start=1):
        # 注意从第1列开始写入，否则会有空列
        for j, col in enumerate(row.keys(), start=0):
            worksheet.write(i, j, row[col])

    # 保存并关闭工作簿
    workbook.close()
    # 设置响应头，告诉浏览器这是一个Excel文件
    response = HttpResponse(buffer.getvalue(),
                            content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = f'attachment; filename={fileName}'
    log.info('headers----------' + str(response.headers))
    log.info('headers----------end')
    log.info(response.getvalue())
    return response
