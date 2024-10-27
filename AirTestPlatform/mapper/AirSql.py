import logging
import random
from datetime import date

from common.DBUtil import do_sql
from config.DBconfig import db_airSit, db_airTest, db_report, db_uranus
from common.Tools import bjtm, sysDate, planId, markNum, getModSevenNum

log = logging.getLogger('log')


def airDB(sql):
    conf = db_airSit()
    # print(sql)
    return do_sql(conf, sql)


def airTest(sql):
    conf = db_airTest()
    # print(sql)
    return do_sql(conf, sql)


def airReportDB(sql):
    conf = db_report()
    # print(sql)
    return do_sql(conf, sql)


def airUranusDB(sql):
    conf = db_uranus()
    # print(sql)
    return do_sql(conf, sql)


# 通过运力名获取机场三字码
def getAirPortCode(flightNo, sendDate):
    sql = '''SELECT * FROM  `tm_air_used_daily_capacity` p WHERE p.`capacity_name`='{}' AND p.`effective_dt`='{}' limit 1;'''.format(
        flightNo, sendDate)
    return airDB(sql)


# 通过taskId获取任务信息
def getTaskInfo(taskId):
    sql = '''SELECT * FROM `tt_air_send` p WHERE p.`task_Id`='{}';'''.format(taskId)
    return airDB(sql)


def addBookingLog(flightNo, sendDate, requirementId, state, createdTm):
    sql = '''INSERT INTO test_addbooking_log(flight_no, send_date, requirement_id, state, created_tm) 
    VALUES ('{}', '{}', '{}', {}, '{}');'''.format(flightNo, sendDate, requirementId, state, createdTm)
    print(sql)
    return airTest(sql)


def getBookingLog(flightNo, sendDate, start, pageSize):
    sql1 = '''select * from test_addbooking_log p where (p.`flight_no`='{0}' or '{0}'='') AND (p.`send_date`='{1}' or '{1}'='') 
    order by id desc limit {2},{3};'''.format(flightNo, sendDate, start, pageSize)
    sql2 = '''select count(*) from test_addbooking_log p where (p.`flight_no`='{0}' or '{0}'='') AND (p.`send_date`='{1}' or '{1}'='');'''.format(
        flightNo, sendDate)
    result = airTest(sql1)
    total = airTest(sql2)[0]['count(*)']
    return result, total


def addOneCodeLog(taskId, containerNo, virtualContainerNo, start, endNum, onecode, createdTm=bjtm()):
    sql = '''INSERT INTO test_onecode_log(task_id, container_no, virtual_container_no, start, end_num, onecode, created_tm) VALUES
     ('{}', '{}', '{}', {}, {},'{}', '{}');'''.format(taskId, containerNo, virtualContainerNo, start, endNum, onecode,
                                                      createdTm)
    print(sql)
    return airTest(sql)


def getOneCodeLog(currentPage, pageSize):
    start = (currentPage - 1) * pageSize
    sql1 = '''select * from test_onecode_log  order by id desc limit {0},{1};'''.format(start, pageSize)
    sql2 = '''select count(*) from test_onecode_log;'''
    result = airTest(sql1)
    total = airTest(sql2)[0]['count(*)']
    return result, total


def setRequireMent(idX):
    x = random.randint(500, 7777)
    y = random.randint(500, 8888)
    z = random.randint(100, 9999)
    sumXYZ = x + y + 2 * z
    sql = '''UPDATE `tt_air_booking_plan_requirement` p SET p.`requirement_status`=1,p.`general_weight_plan`={0},p.`alive_weight_plan`={1},
    p.`fresh_weight_plan`={2},p.`other_weight_plan`={2},manual_weight_total={3},general_weight_total={0},alive_weight_total={1},
    fresh_weight_total={2},other_weight_total={2},weight_total={3} WHERE id={4} and requried_id is null;'''.format(x,y,z,sumXYZ,idX)
    print(sql)
    log.info(sql)
    airDB(sql)


# 获取测试网点列表
def getTestConfigValues(taskName='sendRequirementJob'):
    sql = '''SELECT p.`values` FROM `air_scheduler_config` p WHERE p.`task_name`='{}' limit 1;'''.format(taskName)
    return airTest(sql)[0]['values'].split(',')


# 查询定时任务配置
def getAirSchedulerConfig(currentPage, pageSize):
    start = (currentPage - 1) * pageSize
    sql1 = '''select * from air_scheduler_config  where config_type=1 order by id limit {0},{1};'''.format(start, pageSize)
    sql2 = '''select count(*) from air_scheduler_config where config_type=1;'''
    result = airTest(sql1)
    total = airTest(sql2)[0]['count(*)']
    return result, total


# 修改定时任务配置
def setAirSchedulerConfig(values, taskName):
    sql = '''update air_scheduler_config p set p.`values`='{}' where p.`task_name`='{}'; '''.format(values, taskName)
    airTest(sql)


# 获取测试网点列表
def getTestConfig(taskName='sendRequirementJob'):
    sql = '''SELECT * FROM `air_scheduler_config` p WHERE p.`task_name`='{}' limit 1;'''.format(taskName)
    return airTest(sql)[0]


# 定时任务开关
def setAirSchedulerSwitch(state, taskName):
    sql = '''update air_scheduler_config p set p.`state`={} where p.`task_name`='{}'; '''.format(state, taskName)
    airTest(sql)


# 判断合同运力是否存在
def getContractAndCapa(capacityName, departCityCode, arriveCityCode, contractId):
    sql = '''SELECT * FROM `tm_air_contract_and_capacity` p WHERE capacity_name='{}' AND p.`depart_city_code`='{}' AND p.`arrive_city_code`='{}' AND p.`contract_id`={};'''.format(
        capacityName, departCityCode, arriveCityCode, contractId
    )
    return airDB(sql)


# 判断是否存在有效舱位舱位
def getAvaiableCabin(contractId, capacityName, departCityCode, arriveCityCode):
    sql = '''SELECT * FROM `tt_air_avaiable_cabin` p WHERE p.`CONTRACT_ID`={} AND  p.`capacity_name`='{}' AND
     p.`depart_city_code`='{}' AND p.`arrive_city_code`='{}' AND is_used=1;'''.format(contractId, capacityName,
                                                                                      departCityCode, arriveCityCode)
    return airDB(sql)


# 清除无效数据
def removeUnAvaiableCabin(contractId, capacityName, departCityCode, arriveCityCode):
    sql = '''DELETE FROM `tt_air_avaiable_cabin` WHERE CONTRACT_ID={} AND  capacity_name='{}' AND
    depart_city_code='{}' AND arrive_city_code='{}' AND is_used!=1;'''.format(contractId, capacityName, departCityCode,
                                                                              arriveCityCode)
    sql2 = '''DELETE FROM tt_air_cabin_cargo_type WHERE cabin_id NOT IN(SELECT cabin_id FROM `tt_air_avaiable_cabin`);'''
    airDB(sql)
    airDB(sql2)


# 判断是否有在用运力
def getUsedCapacity(capacityName, departCityCode, arriveCityCode,versionDt = sysDate()):
    sql = '''SELECT * FROM `tm_air_used_daily_capacity` p WHERE `capacity_name`='{}' AND p.`depart_city_code`='{}' AND
     p.`arrive_city_code`='{}' AND p.`version_dt`>='{}' AND p.`is_sleep`=2 limit 1;'''.format(capacityName,
                                                                                                departCityCode,
                                                                                                arriveCityCode,
                                                                                                versionDt)
    capacitylist = airDB(sql)
    if len(capacitylist) > 0:
        return capacitylist
    else:
        return []


# 获取在用运力优化
def getUsedCapacityList(srcCityCode='', desCityCode='', srcZoneCode='', desZoneCode='', srcBatchCode=''):
    srcBatchDt = sysDate()
    sql = '''SELECT distinct depart_city_code,arrive_city_code,depart_dept_code,arrive_dept_code,send_bill_batch_no,capa_plan_send_batch_dt FROM
     `tm_air_used_daily_capacity` p WHERE (p.`depart_city_code`='{0}' or '{0}'='') AND
     (p.`arrive_city_code`='{1}' or '{1}'='') AND (p.depart_dept_code='{2}' or '{2}'='') AND (p.`arrive_dept_code`='{3}' or '{3}'='') 
     AND (p.send_bill_batch_no='{4}' or '{4}'='') AND p.`capa_plan_send_batch_dt` between '{5}' AND DATE_ADD(DATE(NOW()), INTERVAL 9 DAY) AND p.`is_sleep`=2
     group by depart_city_code,arrive_city_code,depart_dept_code,arrive_dept_code,send_bill_batch_no,capa_plan_send_batch_dt;'''.format(
        srcCityCode, desCityCode, srcZoneCode, desZoneCode, srcBatchCode, srcBatchDt)
    log.info(sql)
    capacitylist = airDB(sql)
    if len(capacitylist) > 0:
        return capacitylist
    else:
        return []


# 判断是否有在用运力
def getUsedCapacityByName(capacityName,versionDt = sysDate()):
    sql = '''SELECT * FROM `tm_air_used_daily_capacity` p WHERE `capacity_name`='{}' AND p.`version_dt`>='{}' AND p.`is_sleep`=2 limit 1;'''.format(
        capacityName, versionDt)
    capacitylist = airDB(sql)
    if len(capacitylist) > 0:
        return capacitylist[0]
    else:
        return []


def getUsedCapacityByNameAndDate(capacityName, effectiveDate=sysDate()):
    sql = '''SELECT * FROM `tm_air_used_daily_capacity` p WHERE `capacity_name`='{}' AND p.`effective_dt`='{}' AND p.`is_sleep`=2 limit 1;'''.format(
        capacityName, effectiveDate)
    capacitylist = airDB(sql)
    if len(capacitylist) > 0:
        return capacitylist[0]
    else:
        return []

#根据日期-时间输出格式化时间
def getStandardTm(versionDt=sysDate(),planTm='0900'):
    sql='''select STR_TO_DATE(concat(DATE_FORMAT('{0}', '%Y-%m-%d'), ' ', substr(lpad('{1}', 4, '0'),1,2),
     ':', substr(lpad('{1}', 4, '0'),3, 4)),'%Y-%m-%d %H:%i') as standardTm from  dual;'''.format(versionDt,planTm)
    standardTm=airDB(sql)[0]['standardTm']
    return date.strftime(standardTm,'%Y-%m-%d %H:%M')


# 判断是否有在用运力
def getUsedCapacityByDate():
    effectiveDate = sysDate()
    sql = '''SELECT * FROM `tm_air_used_daily_capacity` p WHERE p.`effective_dt`>='{}' AND p.`is_sleep`=2 limit 1;'''.format(
        effectiveDate)
    capacitylist = airDB(sql)
    if len(capacitylist) > 0:
        return capacitylist[0]
    else:
        return []


# 获取网点名称
def getDeptNameBydeptCode(belongNetworkCode):
    sql = '''SELECT * FROM `ts_department` p WHERE p.`DEPT_CODE`='{}' limit 1;'''.format(belongNetworkCode)
    return airDB(sql)[0]['DEPT_NAME']


# 根据ID获取供应商名称
def getSupplierNameById(supplierId):
    sql = '''SELECT * FROM `tm_air_supplier` p WHERE p.`SUPPLIER_ID`='{}' limit 1;'''.format(supplierId)
    if len(airDB(sql)) > 0:
        return airDB(sql)[0]['SUPPLIER_NAME']
    else:
        log.info('''供应商信息不存在，供应商ID='{}'''.format(supplierId))


def setAvaiableCabin(capacityName, departCityCode, arriveCityCode, deptId, sendBelongNetworkCode, avaiableCabinSpace,
                     capacityId, supplierId, supplierId2, supplierId3, getBelongNetworkCode, planeType, contractId,
                     capKey):
    effectiveDate = sysDate()
    supplierName = getSupplierNameById(supplierId)
    if str(supplierId2) == '-1':
        supplierName2 = ''
    else:
        supplierName2 = getSupplierNameById(supplierId2)

    if str(supplierId3) == '-1':
        supplierName3 = ''
    else:
        supplierName3 = getSupplierNameById(supplierId3)
    deptName = getDeptNameBydeptCode(sendBelongNetworkCode)
    operateTime = bjtm()
    sql = '''INSERT INTO `tt_air_avaiable_cabin`(`capacity_name`, `depart_city_code`, `arrive_city_code`, `scheduled_days`, `effective_date`, `expiration_date`,
     `dept_id`, `dept_code`, `dept_name`, `version`,`avaiable_cabin_space`, `resource_info_id`, `supplier_id`, `supplier_name`, `supplier_id_2`, `supplier_name_2`, 
     `supplier_id_3`, `supplier_name_3`, `send_belong_network_code`, `get_belong_network_code`, `cargo_types`, `is_protocol_flight`, `protocol_weight`, `check_day`, 
     `strategy_cabin_space`, `close_tm_len`, `remark`, `schedule_flight_type`, `util_type`, `plane_type`, `cabin_common_id`, `CONTRACT_ID`, `pattern_number`, `packing_number`, 
      `bucket_number`, `is_used`, `warning_flag`, `protocol_distribution_priority`, `created_emp_code`, `created_tm`, `modified_emp_code`, `modified_tm`, 
      `synchronized_time`, `cap_key`, `atp_current_Tm`, `data_source`, `atp_id`, `check_status`, `reject_reason`, `proxy_cabin_space`, `approved_cabin_space`,
       `expansion_status`, `cancel_peak_warning`, `adjust_reason`) VALUES
     ('{0}', '{1}', '{2}','1234567', '{3}', '2028-12-01', {4}, '{5}', '{6}', 0, {7}, {8}, {9}, '{10}', {11}, '{12}', {13}, '{14}',
      '{5}', '{15}', '1,2,3,5,6,19,20,21', 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '{16}', NULL, {17}, NULL, NULL, NULL, 1, 1, NULL,
       '47', '{18}', '47', '{18}', '{18}', '{19}', NULL, 1, NULL, 6, NULL, NULL, NULL, 4, NULL, NULL);'''.format(
        capacityName, departCityCode, arriveCityCode, effectiveDate, deptId, sendBelongNetworkCode, deptName,
        avaiableCabinSpace, capacityId, supplierId, supplierName, supplierId2, supplierName2,
        supplierId3, supplierName3, getBelongNetworkCode, planeType, contractId, operateTime, capKey)
    return airDB(sql)


def setCabinCargoType(cabinId):
    operateTime = bjtm()
    cargoTypeList = [1, 2, 3, 5, 6, 19, 20, 21]
    for cargoType in cargoTypeList:
        sql = '''INSERT INTO `tt_air_cabin_cargo_type`(`cabin_id`, `cargo_type`, `created_emp_code`, `created_tm`) VALUES
         ({}, {}, '47', '{}');'''.format(cabinId, cargoType, operateTime)
        airDB(sql)


def getCabinCargoType(cabinId):
    sql = '''SELECT * FROM tt_air_cabin_cargo_type p WHERE p.`cabin_id`={};'''.format(cabinId)
    return airDB(sql)


def removeCnSendPriceAir(contractId):
    sql1 = '''DELETE FROM `tt_air_s_carr_sh_cn_item` WHERE carriage_id IN(SELECT send_id FROM `tt_air_s_carr_sh_cn`  WHERE contract_id='{}');'''.format(
        contractId)
    sql2 = '''DELETE FROM `tt_air_s_carr_sh_cn`  WHERE contract_id='{}';'''.format(contractId)
    airDB(sql1)
    airDB(sql2)


def updateRequirementMatch():
    sql = 'UPDATE tt_air_plan_requirement_report p SET p.`send_batch_dt`=DATE_ADD(DATE(send_batch_dt), INTERVAL 1 DAY);'
    airReportDB(sql)


def getProxyConfig(deptCode='010R', supplierId=10101000167485):
    sql = '''SELECT * FROM tt_air_aibss_proxy_config p WHERE p.`send_belong_network_code`='{}' AND p.`supplier_id`={};'''.format(
        deptCode, supplierId)
    proxyConfigList = airDB(sql)
    return proxyConfigList


def addProxyConfig(deptCode='010R', supplierId=10101000167485):
    createTm = bjtm()
    supplierName = getSupplierNameById(supplierId)
    sql = '''INSERT INTO `airsit`.`tt_air_aibss_proxy_config`(`id`, `send_belong_network_code`, `depart_city_name`, `depart_city_code`, `supplier_id`, `supplier_name`, `email_addr`, `cc_email_addr`, `CREATED_EMP_CODE`, `CREATED_TM`, `MODIFIED_EMP_CODE`, `MODIFIED_TM`, `interface_type`, `area_name`, `is_range`, `is_range_1`, `is_range_2`, `email_addr_1`, `cc_email_addr_1`, `interface_type_1`, `interface_type_2`, `is_range_3`, `interface_type_3`, `synchronized_time`) VALUES
     (3066, '{0}', '北京', '010', {1}, '{2}', NULL, NULL, '847790', '{3}', '847790', 
     '{3}', '3', '华北分拨区', 1, 1, 1, NULL, NULL, '3', '3', 1, '3', '{3}');'''.format(deptCode, supplierId, supplierName,
                                                                                   createTm)
    airDB(sql)


def updateProxyConfig(deptCode='010R', supplierId=10101000167485):
    sql = '''UPDATE tt_air_aibss_proxy_config p SET p.`interface_type`='3',p.`interface_type_1`='3',p.`interface_type_2`='3',p.`interface_type_3`='3',
p.`is_range`=1,p.`is_range_1`=1,p.`is_range_2`=1,p.`is_range_3`=1 WHERE p.`send_belong_network_code`='{}' AND p.`supplier_id`={};'''.format(
        deptCode, supplierId)
    airDB(sql)


# 获取可申请订舱交互数据
def getSendApplyID():
    sendDate = sysDate()
    sql = '''SELECT m.`id` id ,n.id relationId FROM tt_air_aibss_space m RIGHT JOIN tt_space_requirement_relation n ON n.`key_space`=m.`key_space` WHERE
     n.`plan_send_batch_dt`='{}' AND n.`plan_space_amount`>0 AND n.`send_space_state`!=2;'''.format(sendDate)
    SendApplyIdList = airDB(sql)
    return SendApplyIdList


# 获取需求计划
def selectBookingPlan(srcBatchDt, srcCityCode, desCityCode, srcZoneCode, desZoneCode, srcBatchCode):
    sql = ''' SELECT * FROM tt_air_booking_plan p WHERE p.`src_batch_dt`='{0}' AND p.`src_city_code`='{1}' AND p.`des_city_code`='{2}'
            AND p.`src_zone_code`='{3}' AND p.`des_zone_code`='{4}' AND p.`src_batch_code`='{5}' AND p.`capacity_type`=2;'''.format(
        srcBatchDt, srcCityCode, desCityCode, srcZoneCode, desZoneCode, srcBatchCode)
    bookingPlanList = airDB(sql)
    if len(bookingPlanList) > 0:
        return bookingPlanList
    else:
        return []


# 维护需求计划
def insertBookingPlan(srcBatchDt, srcCityCode, desCityCode, srcZoneCode, desZoneCode, srcBatchCode):
    Id = planId()
    currentTm = bjtm()
    sql = '''INSERT INTO tt_air_booking_plan(`id`, `src_batch_dt`, `src_city_code`, `src_zone_code`, `src_batch_code`, `des_city_code`, `des_zone_code`,
     `line_status`, `creator`, `create_tm`, `modifier`, `modify_tm`, `new_src_batch_code`, `plan_flg`, `source`, `capacity_type`, `plan_forecast2d`, `plan_forecast`,
      `plan_forecast_quantity`, `plan_forecast_quantity2d`) VALUES
       ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', 1, '01386333', '{7}', '01386333', 
       '{7}', '{6}', 1, 'Test', 2, 0.00, 0.00, 0, 0);'''.format(Id, srcBatchDt, srcCityCode, srcZoneCode, srcBatchCode,
                                                                desCityCode, desZoneCode, currentTm)
    airDB(sql)


# 获取自动批复
def getAutoReplay(supplierId, departThrLetterCode, arriveThrLetterCode):
    sql = '''SELECT * FROM airsit.tt_air_automatic_stowage t WHERE supplier_id = {} AND depart_thr_letter_code = '{}' AND arrive_thr_letter_code = '{}';'''.format(
        supplierId, departThrLetterCode, arriveThrLetterCode)
    configList = airDB(sql)
    return configList


# 设置自动批复
def setAutoReplay(supplierId, departThrLetterCode, arriveThrLetterCode, pmCode):
    effectiveDate = sysDate()
    currentTm = bjtm()
    sql = '''INSERT INTO `tt_air_automatic_stowage`(`effective_date`, `expiration_date`, `supplier_id`, `depart_thr_letter_code`, `arrive_thr_letter_code`,
     `flight_no`, `space_type`, `approval_rules`, `approval_amount`, `pm_code`, `created_tm`, `created_emp_code`, `modified_emp_code`, `modifeid_tm`) VALUES
     ('{0}', '2028-12-31', {1}, '{2}', '{3}', NULL, NULL, 1, NULL, '{4}', '{5}', 'wyj', 'wyj', '{5}');'''.format(
        effectiveDate, supplierId, departThrLetterCode, arriveThrLetterCode, pmCode, currentTm)
    print(sql)
    airDB(sql)


# 获取已批复数据
def getAddTaskID():
    sendDate = sysDate()
    sql = '''SELECT m.`id` id ,n.id relationId FROM tt_air_aibss_space m RIGHT JOIN tt_space_requirement_relation n ON n.`key_space`=m.`key_space` WHERE
     n.`plan_send_batch_dt`='{}' AND n.task_status='1' AND n.approval_state='3' AND n.ACTUAL_SPACE_AMOUNT>0;'''.format(
        sendDate)
    addTaskIdList = airDB(sql)
    return addTaskIdList


# 配置运力信息中运输距离和时长-确保满足生成短驳条件
def setDistanceAndTm():
    currentDate = sysDate()
    sqlAir = '''UPDATE tm_air_used_daily_capacity k SET shipment_transport_distance=99,shipment_transport_time=15,takegoods_transport_distance=25,takegoods_transport_time=10
        WHERE k.capa_plan_send_batch_dt BETWEEN '{}' AND DATE_ADD(DATE(NOW()), INTERVAL 7 DAY) AND (k.depart_city_code IN('010','021','020','755') or arrive_city_code='027');'''.format(
        currentDate)
    sqlUranus = '''UPDATE tt_air_flight_manage_resource p SET p.send_transport_distance=99,p.send_transport_tm=15,p.get_transport_distance=25,p.get_transport_tm=10 WHERE 
        p.plan_send_batch_dt BETWEEN '{}' AND  DATE_ADD(DATE(NOW()), INTERVAL 7 DAY) and (p.src_city IN('010','021','020','755') or des_city='027');'''.format(
        currentDate)
    # 无短驳测试场景设置
    sqlAirFor8981 = '''UPDATE tm_air_used_daily_capacity k SET shipment_transport_distance=0,shipment_transport_time=0,takegoods_transport_distance=0,takegoods_transport_time=0
           WHERE k.capa_plan_send_batch_dt BETWEEN '{}' AND DATE_ADD(DATE(NOW()), INTERVAL 7 DAY) AND k.depart_city_code='8981';'''.format(
        currentDate)
    sqlUranusFor8981 = '''UPDATE tt_air_flight_manage_resource p SET p.send_transport_distance=0,p.send_transport_tm=0,p.get_transport_distance=0,p.get_transport_tm=0 WHERE 
           p.plan_send_batch_dt BETWEEN '{}' AND  DATE_ADD(DATE(NOW()), INTERVAL 7 DAY) and p.src_city='8981';'''.format(
        currentDate)
    airDB(sqlAir)
    airUranusDB(sqlUranus)
    airDB(sqlAirFor8981)
    airUranusDB(sqlUranusFor8981)


def selectUsedCapacityByAirport(departThrLetterCode,arriveThrLetterCode):
    sendBatchDt=sysDate(-2)
    selectUsedCapacityByAirportSql='''SELECT * FROM tm_air_used_daily_capacity p where p.`depart_thr_letter_code`='{}' 
    and p.`arrive_thr_letter_code`='{}' and p.`capa_plan_send_batch_dt`>='{}' and capacity_type=2;'''.format(departThrLetterCode,arriveThrLetterCode,sendBatchDt)
    capacitylist = airDB(selectUsedCapacityByAirportSql)
    if len(capacitylist) > 0:
        return capacitylist
    else:
        return []


def insertCostResource(flightDt, departThrLetterCode, arriveThrLetterCode, capacityName, planSendBatchDt, planSendBatch,
                       scheduleFlightType, departDeptCode, arriveDeptCode, departCityCode, arriveCityCode, goodsLeaveDt,
                       planSendDt,planArrDt, lineKey, cargoType, avaiableSpaceAmount,
                       planGetBatchDt, planGetBatch, batchSeparateDay, planSendSeparateDay, planGetSeparateDay,
                       lineCode, lastestArrStationDt, departCityName, arriveCityName,cabin_id, stationLastestStopDt,
                       lastestArriveDt, getArrStationDt):
    approvalSpaceAmount=random.randint(20, 50)*10
    surplusSpaceAmount=random.randint(100, 300)*10
    actualSpaceAmount=random.randint(20, 50)*10
    avgSpaceAmount=random.randint(20, 50)*10
    insertCostResourceSql = ''' insert into `tt_air_sh_cost_resource_info` (`flight_dt`, `depart_thr_letter_code`, `arrive_thr_letter_code`, `capacity_name`,
     `plan_send_batch_dt`, `plan_send_batch`, `schedule_flight_type`, `depart_dept_code`, `arrive_dept_code`, `depart_city_code`, `arrive_city_code`, 
     `goods_leave_dt`, `plan_send_dt`, `plan_arr_dt`, `line_key`, `cargo_type`, `avaiable_space_amount`, `is_delete`, 
     `created_emp_code`, `created_tm`, `modified_emp_code`, `modified_tm`, 
     `plan_get_batch_dt`, `plan_get_batch`, `batch_separate_day`, `plan_send_separate_day`, `plan_get_separate_day`, `line_code`, `lastest_arr_station_dt`,
      `depart_city_name`, `arrive_city_name`, `plan_space_amount`, `approval_space_amount`, `surplus_space_amount`, `actual_space_amount`, `avg_space_amount`,
       `cabin_common_id`, `cabin_id`, `station_lastest_stop_dt`, `lastest_arrive_dt`, `get_arr_station_dt`)
        values('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}','{16}',
       '0','test47',now(),'test47',now(),'{17}','{18}','{19}','{20}','{21}','{22}',
       '{23}','{24}','{25}','{26}',NULL,'{27}','{28}','{29}',NULL,'{30}',
        '{31}','{32}','{33}');'''.format(flightDt, departThrLetterCode, arriveThrLetterCode, capacityName, planSendBatchDt, planSendBatch,
                       scheduleFlightType, departDeptCode, arriveDeptCode, departCityCode, arriveCityCode, goodsLeaveDt,
                       planSendDt,planArrDt, lineKey, cargoType, avaiableSpaceAmount,planGetBatchDt, planGetBatch, batchSeparateDay,
                       planSendSeparateDay, planGetSeparateDay,lineCode, lastestArrStationDt, departCityName, arriveCityName,
                       approvalSpaceAmount, surplusSpaceAmount,actualSpaceAmount, avgSpaceAmount, cabin_id,
                       stationLastestStopDt,lastestArriveDt, getArrStationDt)
    airDB(insertCostResourceSql)


#维护资源成本
def updateCostResource():
    updateCostResourceSql ='''update tt_air_sh_cost_resource_info p set 
                            flight_dt=DATE_ADD(p.`flight_dt`, INTERVAL 1 DAY),
                            plan_send_batch_dt=DATE_ADD(p.`plan_send_batch_dt`, INTERVAL 1 DAY),
                            goods_leave_dt=DATE_ADD(p.`goods_leave_dt`, INTERVAL 1 DAY),
                            plan_send_dt=DATE_ADD(p.`plan_send_dt`, INTERVAL 1 DAY),
                            plan_arr_dt=DATE_ADD(p.`plan_arr_dt`, INTERVAL 1 DAY),
                            created_tm=now(),
                            modified_tm=now(),
                            plan_get_batch_dt=DATE_ADD(p.`plan_get_batch_dt`, INTERVAL 1 DAY),
                            lastest_arr_station_dt=DATE_ADD(p.`lastest_arr_station_dt`, INTERVAL 1 DAY),
                            station_lastest_stop_dt=DATE_ADD(p.`station_lastest_stop_dt`, INTERVAL 1 DAY),
                            lastest_arrive_dt=DATE_ADD(p.`lastest_arrive_dt`, INTERVAL 1 DAY),
                            get_arr_station_dt=DATE_ADD(p.`get_arr_station_dt`, INTERVAL 1 DAY);'''
    airDB(updateCostResourceSql)

def updateCostResourceDeleted():
    # 还原定时任务删除数据
    updateCostResourceDeleted = '''UPDATE tt_air_sh_cost_resource_info p SET p.`is_delete`=0,p.`modified_tm`=NOW() WHERE p.`is_delete`=1;'''
    airDB(updateCostResourceDeleted)



#发货确认操作 ：
def sendBillConform(taskId):
    mainNumber=getMainNumber(taskId)
    markNumber=markNum()
    weight = random.randint(200, 1500)
    count=random.randint(10,199 )
    sendDt=sysDate(-3)
    sendBillConformSql='''update tt_air_send set main_number='{0}',mark_number='{1}',transfer_weight={2},send_weight={2},charge_weight={2},send_count={3},
                        loading_number={3},send_deliverly={3},
                        comfirm_send_tm=now(),modified_emp_code='autoTest',mark=mark+1,is_by_main_number=1,
                        synchronized_time=now(),is_virtual_main_number=0,is_surrogate=0,is_virtual_mark_number=0,
                        short_distance_weight={2},short_distance_count={2},takegoods_transport_distance=25,shipment_transport_distance=99,original_send_count={3},original_charge_weight={2},
                        original_send_weight={2}  where send_date>'{4}' and  task_Id={5} and comfirm_send_tm is null;'''.format(mainNumber,markNumber,weight,
                                                                                                                                                     count,sendDt,taskId)
    airDB(sendBillConformSql)
#获取发货确认数据列表
def getSendBillData():
    sendDt = sysDate(-3)
    selectSendBillSql = '''select task_Id from tt_air_send where send_date >'{0}' and (arrive_city_code in('010','027','451','028','8981') or depart_city_code='755') and comfirm_send_tm is null;'''.format(sendDt)
    print(selectSendBillSql)
    taskIdList = airDB(selectSendBillSql)
    if len(taskIdList) > 0:
        x =len(taskIdList)
        log.info('可确认任务为:'+str(taskIdList))
        return taskIdList
    else:
        return []


def initIsSupplementary():
    setIsSupplementarySql='''UPDATE tt_air_booking_plan_requirement p  SET p.is_supplementary=1 WHERE p.send_batch_dt=date(now()) AND p.requirement_status IN(0,1);'''
    airDB(setIsSupplementarySql)
    log.info('初始化是否补录OK！')


#新增主单前缀配置
def  addWaybillPrefixConfig(flightType,airlineCode,departAirportCode):
    addWaybillPrefixConfigSql='''INSERT INTO tm_air_waybill_prefix_config (flight_type,depart_airport_code,airline_code,waybill_prefix,is_enable,created_emp_code,created_tm,is_default) VALUES(
    {0},'{2}','{1}','407',1,'AutoTest',now(),0);'''.format(flightType,airlineCode,departAirportCode)



#根据taskId获取发货任务信息
def getSendInfoByTaskId(taskId,keyStr):
    getSendInfoByTaskIdSql='''select * from  tt_air_send p where p.`task_Id`='{}';'''.format(taskId)
    sendBillList=airDB(getSendInfoByTaskIdSql)
    if len(sendBillList)>0:
        return sendBillList[0][keyStr]
    else:
        return None



def getMainNumber(taskId):
    modSevenNum=getModSevenNum()
    flightType=getSendInfoByTaskId(taskId,'flight_type')
    capacityName=getSendInfoByTaskId(taskId,'capacity_name')
    airlineCode=capacityName[0:2]
    departAirportCode=getSendInfoByTaskId(taskId,'depart_thr_letter_code')
    getPreSql='''SELECT waybill_prefix FROM  tm_air_waybill_prefix_config  p WHERE p.`flight_type`='{0}' AND p.`airline_code`='{1}' AND
     (p.`depart_airport_code`='{2}' or depart_airport_code is null or depart_airport_code='') AND  is_enable=1 limit 1;'''.format(flightType,airlineCode,departAirportCode)
    mainNumberPreList=airDB(getPreSql)
    mainNumberPre='407'
    if len(mainNumberPreList)>0:
        mainNumberPre= mainNumberPreList[0]['waybill_prefix']
    else:
        mainNumberPre= '407'
        addWaybillPrefixConfig(flightType, airlineCode, departAirportCode)
    return mainNumberPre+'-'+modSevenNum


#获取待审核异常信息
def  getApprovingExceptionInfobySendId(sendId,keyStr):
    getApprovingExceptionInfobySendIdSql ='''SELECT * FROM  tl_send_exception_dispatch p,tt_air_bill_exception   m WHERE  p.`exception_id`= m.`exception_id` 
    AND m.`state`=2  AND  p.process_result=1   AND  p.`send_id`={} ORDER BY id  DESC  LIMIT 1;'''.format(sendId)
    approvingExceptionList = airDB(getApprovingExceptionInfobySendIdSql)
    if len(approvingExceptionList) > 0:
        return approvingExceptionList[0][keyStr]
    else:
        return None








#模拟运力信息变更场景
def capacityModify():
    capacityModifySql='''''';






