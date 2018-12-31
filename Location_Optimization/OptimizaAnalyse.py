import dbquery
import xlrd
import numpy

def Channel_Standard(TransData):
    '''
    :param TransData:  dic {positioncode: (productcode, qty)}
    :return: ChannelStandard
    '''
    ChannelQtyDic = dict()
    ChannelStandardArray = []
    for key,value in TransData.items():
        if key[0:key.index('-')] not in ChannelQtyDic:
            ChannelQtyDic[key[0:key.index('-')]] = 0
        ChannelQtyDic[key[0:key.index('-')]] += value[1]
    for key,value in ChannelQtyDic.items():
        ChannelStandardArray.append(value)
    ChannelStandard = numpy.std(ChannelStandardArray, ddof = 1)
    return ChannelStandard

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

