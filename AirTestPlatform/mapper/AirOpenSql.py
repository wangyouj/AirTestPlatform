
from common.DBUtil import airOpenDB


# 从配置表获取可校验通过的基础数据
def get_city_info(areaCode=''):
    getCityInfoSql = '''SELECT  w.`cost_quality_area_code`,p.`AREA_CODE`,n.`dist_code`,n.`dist_name` FROM  tm_open_department p,tm_open_belong_network m,tm_district n, tm_open_responsibility_area w WHERE 
 p.DELETE_FLG=0 AND  m.del_flg=0 AND  n.valid_flg=1   AND  w.del_flag=0  AND  n.`type_code`=3   AND  m.`city_code`=n.`dist_code` AND  w.`site_belong_network`=m.`belong_network`
 AND   p.`DEPT_CODE`=m.`belong_network`  and  (w.`cost_quality_area_code`='{0}' or '{0}'='')  group by   dist_code  LIMIT 60; '''.format(
        areaCode)
    cityList = airOpenDB(getCityInfoSql)
    return cityList


# 初始化数据
def init_budget_data():
    initBudgetDataSql = '''TRUNCATE TABLE  tt_atms_budget_import_test_data;'''
    airOpenDB(initBudgetDataSql)


# 写入预算测试数据
def insert_budget_data(departAreaCode, departArea, departCityCode, departCityName, arriveArea, arriveCityCode,
                       arriveCityName):
    insertBudgetSql = '''INSERT INTO tt_atms_budget_import_test_data (data_month,depart_area_code,responsibility_depart_area,depart_city_code,depart_city_name,responsibility_arrive_area,arrive_city_code,arrive_city_name,budget_weight,send_kilo_cost_with_tax,get_kilo_cost_with_tax) VALUES
	 ('2024-01','{0}','{1}','{2}','{3}','{4}','{5}','{6}',0,0,0),
	 ('2024-02','{0}','{1}','{2}','{3}','{4}','{5}','{6}',0,ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-03','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-04','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-05','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-06','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-07','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-08','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-09','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-10','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-11','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3)),
	 ('2024-12','{0}','{1}','{2}','{3}','{4}','{5}','{6}',FLOOR(200+RAND()*(1000-200)),ROUND(RAND()*10+0,3),ROUND(RAND()*10+0,3));'''.format(
        departAreaCode, departArea, departCityCode, departCityName, arriveArea, arriveCityCode, arriveCityName)
    print(insertBudgetSql)
    airOpenDB(insertBudgetSql)


# 导出测试数据到本地生成可导入文件
def export_budget_data_sql():
    exportBudgetDataSql = '''SELECT data_month 月份,depart_area_code 始发地区,responsibility_depart_area 始发责任地区,depart_city_name 始发地,responsibility_arrive_area 目的地区,
    arrive_city_name 目的地,budget_weight 预算重量（kg）,send_kilo_cost_with_tax 发货单公斤成本（含税）,get_kilo_cost_with_tax 提货单公斤成本（含税） FROM  tt_atms_budget_import_test_data;'''
    data=airOpenDB(exportBudgetDataSql)
    return exportBudgetDataSql,data
