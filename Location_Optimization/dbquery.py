import config
import pymssql

def Get_LocationOptimization(PlanTime1,PlanTime2):
    conn = pymssql.connect(server = config.server_ip, user = config.user_name, password = config.password, database = config.db_name)
    cursor = conn.cursor()
    PlanTime1 = "'" + PlanTime1 + "'"
    PlanTime2 = "'" + PlanTime2 + "'"
    query = config.queryoptimiza.format(PlanTime1,PlanTime2)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def Get_RealData(PlanTime1,PlanTime2):
    conn = pymssql.connect(server = config.server_ip, user = config.user_name, password = config.password, database = config.db_name)
    cursor = conn.cursor()
    PlanTime1 = "'" + PlanTime1 + "'"
    PlanTime2 = "'" + PlanTime2 + "'"
    query = config.queryrealdata.format(PlanTime1,PlanTime2)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def Get_OrderData(PlanTime1,PlanTime2,PlanOutTime1,PlanOutTime2):
    conn = pymssql.connect(server = config.server_ip, user = config.user_name, password = config.password, database = config.db_name)
    cursor = conn.cursor()
    PlanTime1 = "'" + PlanTime1 + "'"
    PlanTime2 = "'" + PlanTime2 + "'"
    PlanOutTime1 = "'" + PlanOutTime1 + "'"
    PlanOutTime2 = "'" + PlanOutTime2 + "'"
    query = config.queryorderdata.format(PlanTime1,PlanTime2,PlanOutTime1,PlanOutTime2)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result