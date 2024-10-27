# WangYJ-01386333-Python中级



## 一、环境搭建
### 1.1python环境安装
```commandline
在官网https://www.python.org/下载python后配置环境变量
```
### 1.2django框架安装
```commandline
 pip install Django
```
### 1.3创建django项目
```commandline
django-admin startproject AirTestPlatform
```
### 1.4创建app
-[ ] 按需在项目根路径按下述命令创建一个或多个app后将app移动至apps包统一管理
-[ ] app下models.py、tests.py、admin.py文件若未实际使用可删除以精简项目
```commandline
 python manage.py startapp AirFullLink
```
### 1.5执行迁移命令-避免启动error
```commandline
python manage.py migrate
```
### 1.6启动django项目
```commandline
 python manage.py runserver 9002
```
### 1.7验证django环境
浏览器访问：http://127.0.0.1:9002,页面正常响应即可

## 二、项目功能介绍
- [ ] 1-基础数据维护自动化
- -[ ] 1.1基于航空合同自动维护合同运力
- -[ ] 1.2基于航空合同自动维护运价
- -[ ] 1.3基于航空合同自动维护舱位
- -[ ] 1.4基于航班自动生成需求
- [ ] 2-散航测试环境业务全链路驱动
- -[ ] 2.1基于网点自动录入、发起需求
- -[ ] 2.2基于网点自动发起、批复订舱
- -[ ] 2.3基于上述订舱自动生成任务
- -[ ] 2.4基于任务控制自动生成短驳
- -[ ] 2.5保证各模块数据类型、状态多样化
- [ ] 3-其它功能
- -[ ] 3.1 专享急件、SHEIN、航班管家、航司、调度、场地等上下游MOCK功能
- -[ ] 3.2 根据城市、网点、责任区配置生成合法预算测试数据并支持前台下载
- -[ ] 3.3 数据爬取并保存至本地EXCEL功能


## 三、主要技术应用
- [ ] Django-API开发框架
- [ ] PyMySQL-持久化工具
- [ ] Pandas-数据分析库
- [ ] apscheduler-定时任务框架
- [ ] cryptography-加解密工具
- [ ] concurrent-多线程工具


## 四、项目结构
- [AirTestPlatform]()————django工程管理目录
- [common]()————项目公共方法如工具类等
  - [Tools.py]()——项目通用工具类
  - [ApiUtil.py]()——对外接口标准封装
  - [DButil.py]()——持久化工具
  - [CustomException.py]()——自定义异常
- [config]()————数据库、建表脚本等
  - [DBConfig.py]()——数据库配置
  - [...]()——其它配置
- [mapper]()————持久化脚本管理
- [apiDatas]()————接口请求模板管理
- [business]()————业务逻辑实现
- [job]()————定时任务管理
- [apps]()————app管理
  - [AirFullLink]()————全链路模块django对外api入口、定时任务入口
  - [AirBase]()————其它模块django对外api入口、定时任务入口



## 五、协作说明

| 步骤      |  协作说明 |
|---------|------------------------------------------------------------------------------------|
| 入口      | 请根据功能类型在对应app下views.py编写访问函数并在urls.py配置访问路径<br/>PS:因apps下app文件仅负责提供访问入口 因此不建议新增app |
| 配置      | 请根据需要将配置放置在config包，根据配置类型选择是否新建配置文件                                                |
| 公共方法    | 请根据需要在common包下编写公共方法,按需新建py文件                                                      |
| API访问模型 | 请将api访问模板放置在apiDatas包下，按需新建文件、参数化                                                  |
| 业务逻辑实现  | 请将业务逻辑处理类文件放置在business包，按需新建py文件                                                   |
| 数据持久化   | 请将持久化脚本、DB访问脚本放置在mapper包，按需新建py文件                                                  |
| 定时任务    | 请将定时任务放置在job包下管理，可按需新建py文件                                                         |


















