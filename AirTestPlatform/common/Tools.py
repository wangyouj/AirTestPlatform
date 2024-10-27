from concurrent.futures import ThreadPoolExecutor
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import hmac
import re
import random
import pandas as pd
from datetime import timedelta
from hashlib import sha1

import requests, logging
from datetime import date
import pymysql
import time

from sqlalchemy.orm import class_mapper

log = logging.getLogger('log')

# 生成秘钥cipher_key
# CIPHER_KEY = Fernet.generate_key()

CIPHER_KEY = settings.CIPHER_KEY


class AIR_Login:
    def __init__(self):
        self.user = '01386333'
        self.pwd = '123'
        self.code = '1'
        self.service = 'http://shiva-trtms-air-service-web.sit.sf-express.com:80/admin/login'
        # self.service = service

    def air_web_login(self):
        '''
        登录实现
        :return:
        '''
        url = 'https://cas.sit.sf-express.com/cas/login?service=' + self.service
        session = requests.session()
        html = session.post(url=url, allow_redirects=False, verify=False).content.decode()
        # print(html)
        pattern1 = r'name="lt" value="(.+?)" />'
        lt_value = re.findall(pattern1, html)[0]
        pattern2 = r'name="iddds" value="(.+?)"  />'
        iddds_value = re.findall(pattern2, html)[0]

        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                                ' AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/49.0.2623.112 Safari/537.36',
                  'Content-Type': 'application/x-www-form-urlencoded'}
        body_data = dict()
        body_data['lt'] = lt_value
        body_data['_eventId'] = 'submit'
        body_data['qrcodeId'] = ''
        body_data['iddds'] = iddds_value
        body_data['username'] = self.user
        body_data['password'] = self.pwd
        body_data['verifyCode'] = self.code
        # 访问WEB系统应用
        res = session.post(url, headers=header, data=body_data, allow_redirects=False)
        true_url = res.headers['Location']
        res = session.get(url=url, verify=False)
        # 校验登录结果
        pattern = r'<title>(.*?)</title>'
        title_list = re.findall(pattern, res.content.decode())
        print(title_list)
        if not title_list:
            logging.warning('页面访问失败！')
        else:
            logging.info('正在访问：' + str(title_list))

        session.post(true_url, headers=header, data=body_data, allow_redirects=True)
        service_web_cookie = str(session.cookies)
        return session, service_web_cookie


def airSys():
    '''
    获取air系统session
    :return:
    '''
    a = AIR_Login()
    session, cookie = a.air_web_login()
    return session, cookie


def airThreadRun(methodName, threadCount, KeyList):
    '''
    多线程任务处理封装--当前方法适用于I/O密集型任务，其它类型未必适用，使用前建议验证效果
    :param methodName: 需要执行的任务即函数名或方法名
    :param threadCount: 线程数
    :param KeyList: 任务分组维度list
    :return:
    '''
    start = time.time()
    # 线程池
    executor = ThreadPoolExecutor(threadCount)

    res = []
    for key in KeyList:  # 开启指定数量的任务
        future = executor.submit(methodName, key)  # 异步提交任务
        res.append(future)

    executor.shutdown()  # 等待所有线程执行完毕

    for r in res:
        print(r.result())  # 打印结果

    end = time.time()
    print(end - start)


def export_to_local(db, sql, file_path):
    '''
    本地下载-通用方法
    依赖工具包：pip install pandas
    :param db: 指定的数据库实例
    :param sql: 获取下载数据的SQL
    :param file_path: 下载数据的存放路径+文件名
    :return:
    '''
    # 获取数据库配置
    host, user, password, database, port, charset = db
    # 建立连接
    connection = pymysql.connect(host=getOrgStr(host), user=getOrgStr(user), password=getOrgStr(password),
                                 database=getOrgStr(database))
    # 取数脚本
    sql = sql
    # 查询数据
    df = pd.read_sql(sql, connection)
    # 关闭数据库连接
    connection.close()
    # 将查询结果保存到本地的Excel文件：
    # 指定文件位置
    output_file_path = file_path
    # 执行导出
    df.to_excel(output_file_path, index=False)


def currentTm():
    '''
    获取时间格式如：20240801181818
    :return: str
    '''
    currentTm = time.strftime('%Y%m%d%H%M%S')
    return currentTm


def getEncodeStr(text):
    '''
    密码托管
    :param text:
    :return:
    '''
    cipher = Fernet(CIPHER_KEY)
    # 将原文转为字节
    text = text.encode('utf-8')
    # 进行加密
    encrypted_text = cipher.encrypt(text)
    return encrypted_text.decode('utf-8')


def getOrgStr(text):
    cipher = Fernet(CIPHER_KEY)
    # 转为字节
    text = text.encode('utf-8')
    # 进行解密
    decrypted_text = cipher.decrypt(text)
    return decrypted_text.decode('utf-8')


def now():
    t = time.time()
    # print (t)   #原始时间数据
    # print (int(t))   #秒级时间戳
    now = int(round(t * 1000))
    # print (int(round(t * 1000000))) #微秒级时间戳
    return now


# 获取当前时间
def bjtm():
    bjtm = time.strftime('%Y-%m-%d %H:%M:%S')
    return bjtm


# 获取日期
def sysDate(x=0):
    s = date.today()
    modified_date = s + timedelta(days=x)
    modified_date = modified_date.strftime("%Y-%m-%d")
    return modified_date


# 获取随机字符串
def random_str(slen=32):
    seed = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    return ''.join(sa)


# 生成随机车标号
def markNum(slen=12):
    seed = "123456789"
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    return ''.join(sa)


# 生成随机主运单
def mainNum():
    pre = '407-'
    numX = random.randint(1428571, 14285714) * 7
    mainNumber = pre + str(numX)
    return mainNumber


# 获取模7规则主单数字
def getModSevenNum():
    x = random.randint(1000000, 9999999)
    y = x % 7
    return str(x) + str(y)


# 将数据库对象转为字典
def to_dict(obj):
    mapper = class_mapper(obj.__class__)
    columns = [column.key for column in mapper.columns]
    return dict((col, getattr(obj, col)) for col in columns)


# 生成计划需求ID
def planId(slen=5):
    seed = "123456789"
    nowStr = str(now())
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    return int(nowStr + ''.join(sa))


# 生成随机面单号
def getOrderNo(slen=0):
    return "SF" + str(now() + slen)


# 航班管家对DI签名
def sf_signature(app_id, app_secret, uri, timestamp, nonce):
    content = app_id + '|' + uri + '|' + timestamp + '|' + nonce
    hmac_raw = hmac.new(app_secret.encode(), content.encode(), sha1)
    digest = hmac_raw.digest()
    sign = base64.b64encode(digest)
    return sign.decode()


# 输出数据区间内符合模7规则主单号
def getMainNumbers(startNum, endNum):
    mainNumberList = []
    for num in range(startNum, endNum):
        mainNumber = str(num) + str(num % 7)
        mainNumberList.append(mainNumber)
    print("主单号总数=" + str(len(mainNumberList)))
    print(mainNumberList)

# if __name__ == '__main__':
#     airsys=AIR_Login()
#     session, service_web_cookie=airsys.air_web_login()
#     print(session)
#     print(service_web_cookie)
