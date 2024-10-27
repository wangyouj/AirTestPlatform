'''
# @Author  : No.47
# @Time    : 2022/12/15 11:17
# @Function: atms数据操作
'''
import random

from common.DBUtil import do_sql
from config.DBconfig import db_costbase, db_atms
from common.Tools import bjtm


def costbaseDB(sql):
    conf=db_costbase()
    return do_sql(conf,sql)

def atmsDB(sql):
    conf=db_atms()
    return do_sql(conf,sql)

#根据合同ID获取合同信息
def getInfoByContractId(contractId):
    sql='''SELECT * FROM `tm_atms_contract` p WHERE p.`contract_id`='{}' limit 1;'''.format(contractId)
    contractList=costbaseDB(sql)
    if len(contractList)>0:
        return contractList[0]
    else:
        return None
#根据serveCode获取服务主数据
def getServeMainData(serveCode):
    sql='''SELECT * FROM `tm_atms_serve_main_data` p WHERE p.`serve_code`='{}' LIMIT 1;'''.format(serveCode)
    serveCodeList=costbaseDB(sql)
    if len(serveCodeList)>0:
        return serveCodeList[0]
    else:
        return None

#根据合同ID获取合同费用项
def getContractItemById(contractId):
    sql='''SELECT * FROM `tm_atms_contract_fare_item` p WHERE p.`contract_id`={} AND p.`is_delete`=0;'''.format(contractId)
    contractItemList=costbaseDB(sql)
    if len(contractItemList)>0:
        return contractItemList
    else:
        return None

def getCnSendPriceMain(contractId,capacityName,departCityCode, arriveCityCode):
    sql='''SELECT * FROM `tt_atms_air_s_carr_sh_cn` p WHERE p.`contract_id`='{}' AND p.`capacity_name`='{}' AND p.`depart_city_code`='{}' AND p.`arrive_city_code`='{}';'''.format(
        contractId,capacityName,departCityCode,arriveCityCode)
    return costbaseDB(sql)

#删除已有运价
def removeCnSendPriceMain(contractId,capacityName,departCityCode, arriveCityCode):
    sql='''delete FROM `tt_atms_air_s_carr_sh_cn`  WHERE `contract_id`='{}' AND `capacity_name`='{}' AND `depart_city_code`='{}' AND `arrive_city_code`='{}';'''.format(
        contractId,capacityName,departCityCode,arriveCityCode)
    return costbaseDB(sql)


def getContractAndCapacaity(contractId):
    sql='''SELECT * FROM `tm_atms_contract_and_capacity` p WHERE p.`contract_id`='{}' AND p.`is_delete`=0;'''.format(contractId)
    contractAndCapacaityList=costbaseDB(sql)
    if len(contractAndCapacaityList)>0:
        return contractAndCapacaityList
    else:
        return

#国内发货运价主数据
def setCnSendPriceMain(capacityName,departCityCode, arriveCityCode,contractId,departThrLetterCode,arriveThrLetterCode):
    deptId = getInfoByContractId(contractId)['dept_id']
    deptCode= getInfoByContractId(contractId)['dept_code']
    supplierId = getInfoByContractId(contractId)['contract_supplier_id']
    supplierId2 = getInfoByContractId(contractId)['contract_supplier_id_2']
    supplierId3 = getInfoByContractId(contractId)['contract_supplier_id_3']
    supplierCode=getInfoByContractId(contractId)['contract_supplier_code']
    supplierCode2=getInfoByContractId(contractId)['contract_supplier_code_2']
    supplierCode3=getInfoByContractId(contractId)['contract_supplier_code_3']
    cargoTypeList = [1, 2, 3, 5, 6, 19, 20, 21]
    for goodsStowageType in cargoTypeList:
        carrKey='_'.join([deptCode,capacityName,departCityCode,arriveCityCode,str(supplierId), str(supplierId2), str(supplierId3),str(goodsStowageType)])
        createTm=bjtm()
        sql='''INSERT INTO `costbase`.`tt_atms_air_s_carr_sh_cn`(`goods_stowage_type`, `effective_date`, `expiration_date`,
         `supplier_id`, `supplier_id_2`, `supplier_id_3`, `supplier_low_charge`, `supplier_2_low_charge`, `supplier_3_low_charge`, 
         `supplier_charge_logic`, `supplier_2_charge_logic`,`supplier_3_charge_logic`, `settle_type`, `first_wt_able`, `first_wt`, 
         `first_charge`, `extend_wt_price`, `dept_id`, `dept_code`, `capacity_name`, `depart_city_code`, `arrive_city_code`, `carriage_type`,
          `contract_id`, `synchronized_time`, `carr_key`, `reply_Id`, `is_exception`, `supplier_code`, `supplier_code_2`,`supplier_code_3`, 
          `flight_type`, `linked_type`, `linked_type_2`, `linked_type_3`, `short_mode`, `depart_thr_letter_code`,`is_delete`, `version`, 
          `create_tm`, `create_emp_code`, `modified_tm`, `modified_emp_code`, `settlement_org`, `arrive_thr_letter_code`) VALUES('{0}',
           '2022-12-01 00:00:00.0', '2028-12-01 00:00:00.0', '{1}', '{2}', '{3}', '0.0', '0.0', '0.0', NULL, NULL, NULL,'1', NULL, NULL, NULL, 
           NULL, '{4}', '{5}', '{6}', '{7}', '{8}', '1', '{9}', NULL, '{10}',NULL, '2', '{11}','{12}', '{13}', '1', '2', '2', '2', '-1', '{14}',
            '0', '1', '{15}', '47', NULL, NULL, '1', '{16}');'''.format(goodsStowageType,supplierId, supplierId2, supplierId3,
            deptId,deptCode,capacityName,departCityCode, arriveCityCode,contractId,carrKey,supplierCode,supplierCode2,supplierCode3,departThrLetterCode,
            createTm,arriveThrLetterCode)
        costbaseDB(sql)
        print(carrKey+'--维护运价主数据成功！')

#国内发货运价费用项
def setCnSendPriceItem(sendId,supplierId,supplierCode,serveCode,taxCode):
    lowCharge=random.randint(1,99)
    price = random.randint(1,999)/100
    createTm=bjtm()
    unitCode=getServeMainData(serveCode)['meter_unit_code']
    sql='''INSERT INTO tt_atms_air_s_carr_sh_cn_item( `carriage_id`, `supplier_id`, `supplier_code`, `serve_code`, `is_range`,
     `carry_logic`, `low_charge`, `price`, `unit_code`, `unit_name`, `tax_code`, `is_delete`, `created_emp`, `created_tm`, `modified_emp`, `modified_tm`, 
     `serve_content`, `electronic_contract_num`, `electronic_contract_version`) VALUES ({0}, 
    '{1}', '{2}', '{3}', '0', '2', '{4}', '{5}', '{6}', NULL, '{7}', '0', '47', 
    '{8}', NULL, NULL, NULL, NULL, NULL);'''.format(sendId,supplierId,supplierCode,serveCode,
     lowCharge,price,unitCode,taxCode,createTm)
    costbaseDB(sql)


def getCnSendPriceItem(sendId):
    sql='''SELECT * FROM tt_atms_air_s_carr_sh_cn_item p WHERE p.`carriage_id`={};'''.format(sendId)
    cnSendPriceItemList=costbaseDB(sql)
    return cnSendPriceItemList

def getSupplierCode(supplierId):
    sql='''SELECT * FROM `tm_atms_vendor` p WHERE id={} LIMIT 1;'''.format(supplierId)
    supplierList=atmsDB(sql)
    if len(supplierList)>0:
        return supplierList[0]['supplier_code']
    else:
        return supplierId

def getSupplierInfo(supplierId):
    sql='''SELECT * FROM `tm_atms_vendor` p WHERE id={} LIMIT 1;'''.format(supplierId)
    supplierList=atmsDB(sql)
    if len(supplierList)>0:
        return supplierList[0]
    else:
        return supplierId

#按合同删除运价
def removeCnSendPriceAtms(contractId):
    sql='''DELETE FROM tt_atms_air_s_carr_sh_cn_item WHERE carriage_id IN(SELECT send_id FROM `tt_atms_air_s_carr_sh_cn`  WHERE contract_id='{}');'''.format(contractId)
    sql1='''DELETE FROM `tt_atms_air_s_carr_sh_cn`  WHERE contract_id='{}';'''.format(contractId)
    costbaseDB(sql)
    costbaseDB(sql1)

def CnSendPricePushToAir(sendId,type='add'):
    createTm=bjtm()
    sql='''INSERT INTO `tl_atms_data_change` (`module`,`data_id`,`operation_type`,`create_tm`) VALUES('2',{},'{}','{}');'''.format(sendId,type,createTm)
    print(sql)
    costbaseDB(sql)
    print('运价'+str(sendId)+'推送OK')


# if __name__ == '__main__':
#     pass


