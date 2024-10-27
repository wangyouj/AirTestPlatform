'''
平台环境切换相关
'''
from common.DBUtil import do_sql
from config.DBconfig import db_airSit, db_requirement, db_aviation, db_airResource, db_atms, db_airOpen

def airDB(sql):
    conf = db_airSit()
    # print(sql)
    return do_sql(conf, sql)

def airopenDB(sql):
    conf = db_airOpen()
    # print(sql)
    return do_sql(conf, sql)

def requirementDB(sql):
    conf = db_requirement()
    # print(sql)
    return do_sql(conf, sql)


def aviationDB(sql):
    conf = db_aviation()
    # print(sql)
    return do_sql(conf, sql)


def airResourceDB(sql):
    conf = db_airResource()
    # print(sql)
    return do_sql(conf, sql)

def atmsDB(sql):
    conf = db_atms()
    # print(sql)
    return do_sql(conf, sql)

'''SIT→PRO'''
'''SIT→PRO备份SIT'''
def sitBackup():
#air
    sql1='''RENAME TABLE tm_air_airstation TO tm_air_airstation_sitbackup2023;'''
    sql2 ='''RENAME TABLE tm_open_resource_pool TO tm_open_resource_pool_sitbackup2023;'''
    sql3 = '''RENAME TABLE tm_air_airstation TO tm_air_airstation_sitbackup2023;'''

    airDB(sql1)
    airDB(sql2)
    airDB(sql3)
#atms
    sql5 = '''RENAME TABLE tm_air_intention_default_duration TO tm_atms_vendor_intl_sitbackup2023;'''
    sql6 = '''RENAME TABLE tm_air_intention_port_capacity TO tm_atms_vendor_intl_server_cabin_sitbackup2023;'''
    sql7 = '''RENAME TABLE tm_air_intention_port_capacity_batch TO tm_atms_vendor_intl_server_cabin_agent_sitbackup2023;'''
    sql8 = '''RENAME TABLE tm_air_intention_port_cost TO tm_atms_vendor_intl_server_cabin_price_sitbackup2023;'''
    sql9 = '''RENAME TABLE tm_atms_vendor_intl_server_connect TO tm_atms_vendor_intl_server_connect_sitbackup2023;'''
    sql10 = '''RENAME TABLE tm_atms_vendor_intl_server_customs TO tm_atms_vendor_intl_server_customs_sitbackup2023;'''
    sql11 = '''RENAME TABLE tm_atms_vendor_intl_server_ground TO tm_atms_vendor_intl_server_ground_sitbackup2023;'''
    sql12 = '''RENAME TABLE tm_atms_vendor_intl_server_special TO tm_atms_vendor_intl_server_special_sitbackup2023;'''
    sql13 = '''RENAME TABLE tm_atms_vendor_intl_server_special_cargo TO tm_atms_vendor_intl_server_special_cargo_sitbackup2023;'''
    sql14 = '''RENAME TABLE tm_atms_vendor_intl_server_storage TO tm_atms_vendor_intl_server_storage_sitbackup2023;'''
    sql15 = '''RENAME TABLE tm_atms_vendor_intl_thr_letter_code TO tm_atms_vendor_intl_thr_letter_code_sitbackup2023;'''

    atmsDB(sql5)
    atmsDB(sql6)
    atmsDB(sql7)
    atmsDB(sql8)
    atmsDB(sql9)
    atmsDB(sql10)
    atmsDB(sql11)
    atmsDB(sql12)
    atmsDB(sql13)
    atmsDB(sql14)
    atmsDB(sql15)

#airopen
    sql16 = '''RENAME TABLE tm_air_airstation_airline_relation TO tm_air_airstation_airline_relation_sitbackup2023;'''
    sql17='''RENAME TABLE tm_open_airlines_information TO tm_open_airlines_information_sitbackup2023;'''
    sql18='''RENAME TABLE tm_open_resource_pool TO tm_open_resource_pool_sitbackup2023;'''
    sql19='''RENAME TABLE tm_air_airstation_cfg TO tm_air_airstation_cfg_sitbackup2023;'''
    sql20='''RENAME TABLE tm_open_flight_airport TO tm_open_flight_airport_sitbackup2023;'''

    airopenDB(sql16)
    airopenDB(sql17)
    airopenDB(sql18)
    airopenDB(sql19)
    airopenDB(sql20)

#requirement
    sql21 = '''RENAME TABLE tm_air_intention_port_cost TO tm_air_intention_port_cost_sitbackup2023;'''
    sql22 = '''RENAME TABLE tm_air_intention_port_capacity_batch TO tm_air_intention_port_capacity_batch_sitbackup2023;'''
    sql23 = '''RENAME TABLE tm_air_intention_port_capacity TO tm_air_intention_port_capacity_sitbackup2023;'''
    sql24 = '''RENAME TABLE tm_air_intention_default_duration TO tm_air_intention_default_duration_sitbackup2023;'''
    requirementDB(sql21)
    requirementDB(sql22)
    requirementDB(sql23)
    requirementDB(sql24)

#avation
    sql25 = '''RENAME TABLE tt_aof_flight_schedule TO tt_aof_flight_schedule_sitbackup2023;'''
    aviationDB(sql25)

#openresource
    sql26 = '''RENAME TABLE tt_open_eagle_security_check_capability TO tt_open_eagle_security_check_capability_sitbackup2023;'''
    airResourceDB(sql26)

#TODO
'''SIT→PRO启用PRO'''
def usePro():
    # air
    sql1 = '''RENAME TABLE tm_air_airstation TO tm_air_airstation_sitbackup2023;'''
    sql2 = '''RENAME TABLE tm_open_resource_pool TO tm_open_resource_pool_sitbackup2023;'''
    sql3 = '''RENAME TABLE tm_air_airstation TO tm_air_airstation_sitbackup2023;'''
    sql4 = '''RENAME TABLE ts_air_sysconfig TO ts_air_sysconfig_sitbackup2023;'''

    airDB(sql1)
    airDB(sql2)
    airDB(sql3)
    airDB(sql4)
    # atms
    sql5 = '''RENAME TABLE tm_air_intention_default_duration TO tm_atms_vendor_intl_sitbackup2023;'''
    sql6 = '''RENAME TABLE tm_air_intention_port_capacity TO tm_atms_vendor_intl_server_cabin_sitbackup2023;'''
    sql7 = '''RENAME TABLE tm_air_intention_port_capacity_batch TO tm_atms_vendor_intl_server_cabin_agent_sitbackup2023;'''
    sql8 = '''RENAME TABLE tm_air_intention_port_cost TO tm_atms_vendor_intl_server_cabin_price_sitbackup2023;'''
    sql9 = '''RENAME TABLE tm_atms_vendor_intl_server_connect TO tm_atms_vendor_intl_server_connect_sitbackup2023;'''
    sql10 = '''RENAME TABLE tm_atms_vendor_intl_server_customs TO tm_atms_vendor_intl_server_customs_sitbackup2023;'''
    sql11 = '''RENAME TABLE tm_atms_vendor_intl_server_ground TO tm_atms_vendor_intl_server_ground_sitbackup2023;'''
    sql12 = '''RENAME TABLE tm_atms_vendor_intl_server_special TO tm_atms_vendor_intl_server_special_sitbackup2023;'''
    sql13 = '''RENAME TABLE tm_atms_vendor_intl_server_special_cargo TO tm_atms_vendor_intl_server_special_cargo_sitbackup2023;'''
    sql14 = '''RENAME TABLE tm_atms_vendor_intl_server_storage TO tm_atms_vendor_intl_server_storage_sitbackup2023;'''
    sql15 = '''RENAME TABLE tm_atms_vendor_intl_thr_letter_code TO tm_atms_vendor_intl_thr_letter_code_sitbackup2023;'''

    atmsDB(sql5)
    atmsDB(sql6)
    atmsDB(sql7)
    atmsDB(sql8)
    atmsDB(sql9)
    atmsDB(sql10)
    atmsDB(sql11)
    atmsDB(sql12)
    atmsDB(sql13)
    atmsDB(sql14)
    atmsDB(sql15)

    # airopen
    sql16 = '''RENAME TABLE tm_air_airstation_airline_relation TO tm_air_airstation_airline_relation_sitbackup2023;'''
    airopenDB(sql16)

    # requirement
    sql17 = '''RENAME TABLE tm_air_intention_port_cost TO tm_air_intention_port_cost_sitbackup2023;'''
    sql18 = '''RENAME TABLE tm_air_intention_port_capacity_batch TO tm_air_intention_port_capacity_batch_sitbackup2023;'''
    sql19 = '''RENAME TABLE tm_air_intention_port_capacity TO tm_air_intention_port_capacity_sitbackup2023;'''
    sql20 = '''RENAME TABLE tm_air_intention_default_duration TO tm_air_intention_default_duration_sitbackup2023;'''
    requirementDB(sql17)
    requirementDB(sql18)
    requirementDB(sql19)
    requirementDB(sql20)

    # avation
    sql21 = '''RENAME TABLE tt_aof_flight_schedule TO tt_aof_flight_schedule_sitbackup2023;'''
    aviationDB(sql21)

    # openresource
    sql22 = '''RENAME TABLE tt_open_eagle_security_check_capability TO tt_open_eagle_security_check_capability_sitbackup2023;'''
    airResourceDB(sql22)




'''PRO→SIT'''
'''PRO→SIT备份PRO'''
def proBackup():
    pass

'''PRO→SIT启用SIT'''
def useSit():
    pass






















