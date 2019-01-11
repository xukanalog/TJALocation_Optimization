from Monitor import Config
import pymssql

def Get_Monitor(PositionCode):
    conn = pymssql.connect(server = Config.server_ip, user = Config.user_name, password = Config.password, database = Config.db_name)
    cursor = conn.cursor()
    # PlanTime1 = "'" + PlanTime1 + "'"
    # PlanTime2 = "'" + PlanTime2 + "'"
    PositionCode = "'" + PositionCode + "'"
    query = Config.query.format(PositionCode)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if result ==[]:     #防止查的交换库位现在已经没有sku
        return 0
    print('result=%s,PositionCode=%s'%(result,PositionCode))
    return result[0]