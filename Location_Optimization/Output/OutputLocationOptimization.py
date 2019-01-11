'''
function : 输出实际通道出货件数，假设全部交换件数，真正去交换件数
'''

import datetime
import time
import dbquery
from Output import WriteResult,DataProcess
import OptimizaAnalyse

if __name__ == '__main__':
    Start = time.clock()
    CurTime = datetime.datetime.now()
    CurTimeFormat = CurTime.strftime("%Y-%m-%d")
    YesTimeFormat = (CurTime - datetime.timedelta(days = 6)).strftime("%Y-%m-%d")
    CurTimeFormat = (CurTime - datetime.timedelta(days = 5)).strftime("%Y-%m-%d")
    #Channelqty = WriteResult.Get_InitExcel(YesTimeFormat, CurTimeFormat)

    ExchangeResultProcess = DataProcess.ExchangeResult_Process('./2019.1.4A区交换方案22.csv')  #得到交换方案
    #WriteResult.Get_HypoExcel(YesTimeFormat, CurTimeFormat, ExchangeResultProcess)
    WriteResult.Get_RealExcel(YesTimeFormat, CurTimeFormat)

    # Init_Data = dbquery.Get_OrderData('2019-01-01 17:00:00.000', YesTimeFormat + ' 8:00:00',
    #                                   YesTimeFormat + ' 12:00:00', CurTimeFormat + ' 1:00:00')  # 得到数据库原始数据(根据订单流入时间)
    # TransData = Data_Processing(Init_Data)  # 数据处理

    print("The Program is successfully %s"%(time.clock() - Start))

    print('111')#https://www.aliyun.com/jiaocheng/124652.html