'''
function : 天津A区库位优化算法上线，需要对算法好坏进行评估

注：由于采用sku去匹配库位，当库位上sku正好卖完，那就会失去匹配信息，故每列和存在一定偏差
'''


import dbquery
from Output import DataProcess
import xlwt

def Get_InitExcel(YesTimeFormat,CurTimeFormat):    #不交换件数的情况
    '''
    :param: YesTimeFormat,CurTimeFormat 年-月-日
    :return: excel 通道：出货件数
    introduce:  读取当天8点的库位上所存储的sku，采用当天出库的件数去匹配库位，得到每条通道的出货件数
    '''
    Init_DataInit = dbquery.Get_RealData(YesTimeFormat + ' 12:00:00', CurTimeFormat + ' 1:00:00')  # 得到数据库原始数据(根据计划出库时间)
    TransDataInit , __ = DataProcess.Data_Processing(Init_DataInit)                # 数据处理  dic productcode:qty
    ProductPosition = DataProcess.Product_Position("./2019.1.4A区库位信息.csv")  # dic productcode:position
    Channelqty = dict()
    for key , value in TransDataInit.items():
        if key in ProductPosition:
            if ProductPosition[key][0:ProductPosition[key].index('-')] not in Channelqty:
                Channelqty[ProductPosition[key][0:ProductPosition[key].index('-')]] = 0
            Channelqty[ProductPosition[key][0:ProductPosition[key].index('-')]] += value
        #else:
            #print("找到错误啦")
    Excel_Write(Channelqty)
    return 0

def Excel_Write(Channelqty):
    '''
    :param Channelqty:  dict 通道：出货件数
    :return:
    '''
    ChannelqtySort= sorted(Channelqty.items(), key=lambda d: d[0])
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Result')
    i = 0
    for channelqtysort in ChannelqtySort:
        worksheet.write(i , 0, channelqtysort[0])
        worksheet.write(i , 1, channelqtysort[1])
        i += 1
    workbook.save("../excel/ChannelqtyInit.xls")
    return 0

def Channel_AfterExchangeResult(TransData,ExchangeResult):  #根据交换结果得到交换后
    '''
    :param   TransData:  dic {positioncode: (productcode, qty)}
              ExchangeResult:  list [{positioncode: (productcode, qty),positioncode: (productcode, qty)}]
    :return: ChannelAfterExchangeResult:  dic {positioncode: (productcode, qty)}
    '''
    for exchangeresult in ExchangeResult:
        count = 0
        for key,value in exchangeresult.items():
            count += 1
            if count == 1:
                Tempkey = key
                Tempvalue = value
            if count == 2:
                TransData[Tempkey] = value
                TransData[key] = Tempvalue
    ChannelAfterExchangeResult  = TransData
    return ChannelAfterExchangeResult

def Get_HypoExcel(YesTimeFormat,CurTimeFormat,ExchangeResult):          #一次性交换全部的件数的情况
    '''
    :param: YesTimeFormat,CurTimeFormat 年-月-日
             ExchangeResult:  list [{positioncode: productcode,positioncode: productcode}]
    :return: excel 通道：出货件数
    introduce: 读取当天8点的库位上所存储的sku，用给现场的交换策略去更新这些库位信息，
               采用当天出库的件数去匹配库位，得到每条通道的出货件数
    '''
    Init_DataInit = dbquery.Get_RealData(YesTimeFormat + ' 12:00:00', CurTimeFormat + ' 1:00:00')  # 得到数据库原始数据(根据计划出库时间)
    TransDataInit, __ = DataProcess.Data_Processing(Init_DataInit)  # 数据处理  dic productcode:qty
    ProductPosition = DataProcess.Product_Position("./2019.1.4A区库位信息.csv") # dic productcode:position
    for exchangeresult in ExchangeResult:
        count = 0
        for key,value in exchangeresult.items():
            count += 1
            if count == 1:
                Tempkey = key         #position
                Tempvalue = value     #productcode
            if count == 2:
                ProductPosition[Tempvalue] = key
                ProductPosition[value] = Tempkey

    Channelqty = dict()
    for key , value in TransDataInit.items():
        if key in ProductPosition:
            if ProductPosition[key][0:ProductPosition[key].index('-')] not in Channelqty:
                Channelqty[ProductPosition[key][0:ProductPosition[key].index('-')]] = 0
            Channelqty[ProductPosition[key][0:ProductPosition[key].index('-')]] += value
    Excel_Write(Channelqty)
    return 0

def Get_RealExcel(YesTimeFormat,CurTimeFormat):          #实际交换全部的件数的情况
    '''
    :param: YesTimeFormat,CurTimeFormat 年-月-日
    :return: excel 通道：出货件数
    introduce: 读取当天出库的件数，根据当天的预占库位进行每条通道出货件数的计算
    '''
    Init_DataInit = dbquery.Get_RealData(YesTimeFormat + ' 12:00:00', CurTimeFormat + ' 1:00:00')  # 得到数据库原始数据(根据计划出库时间)
    TransDataInit, TransDataReal = DataProcess.Data_Processing(Init_DataInit) # 数据处理  dic TransDataInit productcode:qty
                                                                                              # TransDataReal dic {ProductCode:(PositionCode,Qty)}
    #ProductPosition = DataProcess.Product_Position("./2019.1.4A区库位信息.csv") # dic productcode:position
    Channelqty = dict()
    for key ,value in TransDataReal.items():
        if value[0][0:value[0].index('-')] not in Channelqty:
            Channelqty[value[0][0:value[0].index('-')]] = 0
        Channelqty[value[0][0:value[0].index('-')]] += value[1]
    # for key , value in TransDataInit.items():
    #     if key in ProductPosition:
    #         if ProductPosition[key][0:ProductPosition[key].index('-')] not in Channelqty:
    #             Channelqty[ProductPosition[key][0:ProductPosition[key].index('-')]] = 0
    #         Channelqty[ProductPosition[key][0:ProductPosition[key].index('-')]] += value
    #     else:
    #         print("找到错误啦")
    Excel_Write(Channelqty)
    return 0