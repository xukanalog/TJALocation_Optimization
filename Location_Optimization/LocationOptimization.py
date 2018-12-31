import dbquery
import random
import copy
import xlwt
import OptimizaAnalyse
import datetime

def Data_Processing(Init_Data):
    '''
    :param Init_Data: list [(productcode,positioncode,qty)]
    :return: dic {positioncode:(productcode,qty)}
    '''
    TransData = dict()
    for (ProductCode,PositionCode,Qty) in Init_Data:
        if PositionCode not in TransData:
            TransData[PositionCode] = (ProductCode,Qty)
    return TransData

def Channelqty_Average(TransData):  #计算出货量平均值
    '''
    :param TransData: dic {positioncode:(productcode,qty)}
    :return: #ChannelqtyAveragedic: dic {channel:sumqty}
              ChannelqtyAverage : int
              #ChannelList: list
    '''
    ChannelqtyAveragedic = dict()
    ChannelqtyAverage = 0
    for key,value in TransData.items():
        key = key[0:key.index('-')]
        if key not in ChannelqtyAveragedic:
            ChannelqtyAveragedic[key] = 0
        ChannelqtyAveragedic[key] += value[1]
    for key,value in ChannelqtyAveragedic.items():
        ChannelqtyAverage += value
    return int(ChannelqtyAverage/66)

def Channel_Transfor(TransData):      #货位交换
    '''
    :param TransData: dic {positioncode:(productcode,qty)}
    :return: ChannelTransfor: dic {positioncode:(productcode,qty)}
    '''
    #ChannelTransfor = dict()
    #Temp, AdjustBefore1 = tuple(),tuple()
    ChannelTransfor = copy.deepcopy(TransData)
    ChannelList = []
    for key,value in ChannelTransfor.items():
        ChannelList.append(key)
    RandomNum1 = random.randint(0,len(ChannelList)-1)  #包含前后
    RandomNum2 = random.randint(0,len(ChannelList)-1)
    Temp = ChannelTransfor[ChannelList[RandomNum2]]
    AdjustBefore1 = ChannelTransfor[ChannelList[RandomNum1]]
    AdjustBefore2 = ChannelTransfor[ChannelList[RandomNum2]]
    ChannelTransfor[ChannelList[RandomNum2]] = ChannelTransfor[ChannelList[RandomNum1]]
    ChannelTransfor[ChannelList[RandomNum1]] = Temp
    AdjustAfter1 = ChannelTransfor[ChannelList[RandomNum1]]
    AdjustAfter2 = ChannelTransfor[ChannelList[RandomNum2]]
    return ChannelTransfor, AdjustBefore1,AdjustBefore2,AdjustAfter1,AdjustAfter2, ChannelList[RandomNum1], ChannelList[RandomNum2]

def Channel_Qty(RandomNum1, RandomNum2, ChannelTransfor,TransData):     #得到调整前和调整后的货道出货量
    '''
  #  :param AdjustBefore1:  tuple:(ProductCode,Qty)
  #  :param AdjustBefore2:  tuple:(ProductCode,Qty)
    :param RandomNum1:     str '4317-07-07'
    :param RandomNum2:     str '4317-07-07'
    :param ChannelTransfor dict {PositionCode:(ProductCode,Qty)}   交换后
    :param TransData dict {PositionCode:(ProductCode,Qty)}         交换前
    :return AdjustBeforeQty,AdjustAfterQty
    '''
    AdjustBeforeQty1 = 0
    AdjustBeforeQty2 = 0
    AdjustAfterQty1 = 0
    AdjustAfterQty2 = 0
    for key,value in TransData.items():
        key = key[0:key.index('-')]
        if key == RandomNum1[0:RandomNum1.index('-')]:
            AdjustBeforeQty1 += value[1]
        if key == RandomNum2[0:RandomNum2.index('-')]:
            AdjustBeforeQty2 += value[1]
    for key,value in ChannelTransfor.items():
        key = key[0:key.index('-')]
        if key == RandomNum1[0:RandomNum1.index('-')]:
            AdjustAfterQty1 += value[1]
        if key == RandomNum2[0:RandomNum2.index('-')]:
            AdjustAfterQty2 += value[1]
    return AdjustBeforeQty1, AdjustBeforeQty2, AdjustAfterQty1, AdjustAfterQty2

def Excel_Write(ExchangeResult):
    '''
    :param ExchangeResult: list [{PositionCode:(ProductCode,Qty),PositionCode:(ProductCode,Qty)}]
    :return: excel
    '''
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Result')
    FirstCol = worksheet.col(0) #xlwt中是行和列都是从0开始计算的
    SecCol = worksheet.col(1)
    FirstCol.width = 256 * 45
    SecCol.width = 256 * 45
    count = 0
    for exchangeresult in ExchangeResult:
        column = 0
        for key,value in exchangeresult.items():
            worksheet.write(count,column,str(key) + str(value))
            column += 1
        count = count + 1
    workbook.save('./excel/ExchangeResult.xls')
    return 0

#if __name__ == '__main__':
def Location_Optimization(YesTimeFormat,CurTimeFormat,RowsChange,RowsChangePerTime):
    '''
    :param      YesTimeFormat  昨天时间  '2018-12-20' ;CurTimeFormat:  当前时间  '2018-12-21'
                 RowsChange: 需要换的行数    RowsChangePerTime：换一次需要计算的次数
    :return:    OptimizaAnalyseBefore: 换之前通道标准差   OptimizaAnalyseAfter：换之后通道标准差
    '''
    #Init_Data = dbquery.Get_LocationOptimization('2018-12-20 23:30:00.000','2018-12-21 23:40:00.000')  #得到数据库原始数据
    ##Init_Data1 = dbquery.Get_RealData('2018-12-21 12:00:00.000', '2018-12-22 1:00:00.000')  # 得到数据库原始数据(根据计划出库时间)
    ##TransData1 = Data_Processing(Init_Data1)  # 数据处理
    Init_Data1 = dbquery.Get_RealData(YesTimeFormat + ' 12:00:00', CurTimeFormat + ' 1:00:00')  # 得到数据库原始数据(根据计划出库时间)
    TransData1 = Data_Processing(Init_Data1)  # 数据处理
    Init_Data = dbquery.Get_OrderData('2018-12-25 17:00:00.000',YesTimeFormat + ' 8:00:00',YesTimeFormat + ' 12:00:00', CurTimeFormat + ' 1:00:00')  # 得到数据库原始数据(根据订单流入时间)
    TransData = Data_Processing(Init_Data)  #数据处理
    OptimizaAnalyseBefore = OptimizaAnalyse.Channel_Standard(TransData1)
    ChannelqtyAverage =  Channelqty_Average(TransData)
    ExchangeResult = []                 #最终的交换结果
    ExchangeTemp = dict()               #交换的暂存
    for i in range(RowsChange):
        Max = float('-inf')
        MaxFlag = 0
        for j in range(RowsChangePerTime):
            ChannelTransfor, AdjustBefore1, AdjustBefore2, AdjustAfter1, AdjustAfter2, RandomNum1, RandomNum2 = Channel_Transfor(TransData)
            AdjustBeforeQty1, AdjustBeforeQty2, AdjustAfterQty1, AdjustAfterQty2 = Channel_Qty(RandomNum1, RandomNum2, ChannelTransfor, TransData)
            #EqualValue = abs(AdjustBefore1[1] + AdjustBefore2[1] - 2 * ChannelqtyAverage) - abs(AdjustAfter1[1] + AdjustAfter2[1] - 2 * ChannelqtyAverage)
            EqualValue = abs(AdjustBeforeQty1 - ChannelqtyAverage) + abs(AdjustBeforeQty2 - ChannelqtyAverage) -(abs(AdjustAfterQty1 - ChannelqtyAverage) + abs(AdjustAfterQty2 - ChannelqtyAverage))
            if (EqualValue > Max):
                #TransData = ChannelTransfor    #需要存入中间变量中，防止对下一次结果造成影响
                MaxFlag = 1
                TransDataTemp = ChannelTransfor
                Max = EqualValue
                ExchangeTemp.clear()
                ExchangeTemp[RandomNum1] = AdjustBefore1
                ExchangeTemp[RandomNum2] = AdjustBefore2
        TransData = copy.deepcopy(TransDataTemp)
        TransDataTemp.clear()
        if MaxFlag == 1:
            ExchangeResult.append(copy.deepcopy(ExchangeTemp))
            ExchangeTemp.clear()
    Excel_Write(ExchangeResult)
    #OptimizaAnalyseAfter = OptimizaAnalyse.Channel_Standard(TransData)
    ChannelAfterExchangeResult = OptimizaAnalyse.Channel_AfterExchangeResult(TransData1 ,ExchangeResult)  #采用ExchangeResult交换方案对TransData进行交换的结果
    OptimizaAnalyseAfter = OptimizaAnalyse.Channel_Standard(ChannelAfterExchangeResult)   #标准差计算
    return OptimizaAnalyseBefore, OptimizaAnalyseAfter

#OptimizaAnalyseBefore, OptimizaAnalyseAfter = Location_Optimization("2018-12-25","2018-12-26")
#print('111')

'''
if __name__ == '__main__':
    #Init_Data = dbquery.Get_LocationOptimization('2018-12-20 23:30:00.000','2018-12-21 23:40:00.000')  #得到数据库原始数据
    Init_Data1 = dbquery.Get_RealData('2018-12-21 12:00:00.000', '2018-12-22 1:00:00.000')  # 得到数据库原始数据(根据计划出库时间)
    TransData1 = Data_Processing(Init_Data1)  # 数据处理
    Init_Data = dbquery.Get_OrderData('2018-12-18 17:00:00.000','2018-12-20 8:00:00.000','2018-12-20 12:00:00.000', '2018-12-21 1:00:00.000')  # 得到数据库原始数据(根据订单流入时间)
    TransData = Data_Processing(Init_Data)  #数据处理
    OptimizaAnalyseBefore = OptimizaAnalyse.Channel_Standard(TransData)
    ChannelqtyAverage =  Channelqty_Average(TransData)
    ExchangeResult = []                 #最终的交换结果
    ExchangeTemp = dict()               #交换的暂存
    for i in range(100):
        Max = float('-inf')
        MaxFlag = 0
        for j in range(20):
            ChannelTransfor, AdjustBefore1, AdjustBefore2, AdjustAfter1, AdjustAfter2, RandomNum1, RandomNum2 = Channel_Transfor(TransData)
            AdjustBeforeQty1, AdjustBeforeQty2, AdjustAfterQty1, AdjustAfterQty2 = Channel_Qty(RandomNum1, RandomNum2, ChannelTransfor, TransData)
            #EqualValue = abs(AdjustBefore1[1] + AdjustBefore2[1] - 2 * ChannelqtyAverage) - abs(AdjustAfter1[1] + AdjustAfter2[1] - 2 * ChannelqtyAverage)
            EqualValue = abs(AdjustBeforeQty1 - ChannelqtyAverage) + abs(AdjustBeforeQty2 - ChannelqtyAverage) -(abs(AdjustAfterQty1 - ChannelqtyAverage) + abs(AdjustAfterQty2 - ChannelqtyAverage))
            if (EqualValue > Max):
                #TransData = ChannelTransfor    #需要存入中间变量中，防止对下一次结果造成影响
                MaxFlag = 1
                TransDataTemp = ChannelTransfor
                Max = EqualValue
                ExchangeTemp.clear()
                ExchangeTemp[RandomNum1] = AdjustBefore1
                ExchangeTemp[RandomNum2] = AdjustBefore2
        TransData = copy.deepcopy(TransDataTemp)
        TransDataTemp.clear()
        if MaxFlag == 1:
            ExchangeResult.append(copy.deepcopy(ExchangeTemp))
            ExchangeTemp.clear()
    Excel_Write(ExchangeResult)
    OptimizaAnalyseAfter = OptimizaAnalyse.Channel_Standard(TransData)
    ChannelAfterExchangeResult = OptimizaAnalyse.Channel_AfterExchangeResult(TransData1 ,ExchangeResult)  #采用ExchangeResult交换方案对TransData进行交换的结果
    OptimizaAnalyseAfter1 = OptimizaAnalyse.Channel_Standard(ChannelAfterExchangeResult)   #标准差计算

    print('111')

'''


#go p1 增加一个线程