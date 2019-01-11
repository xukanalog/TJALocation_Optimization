import copy

def Data_Processing(Init_Data):
    '''
    :param Init_Data: list [(productcode,positioncode,qty)]
    :return: TransData: dic   {productcode:Qty}       TransDataReal: dic {productcode:（PositionCode，Qty）}
    '''
    TransData = dict()
    TransDataReal = dict()
    for (ProductCode,PositionCode,Qty) in Init_Data:
        if ProductCode not in TransData:
            TransData[ProductCode] = Qty
        else:                              # 由于A区存在一品多位情况，会导致后者覆盖前者
            TransData[ProductCode] += Qty
        if ProductCode not in TransDataReal:
            TransDataReal[ProductCode] = (PositionCode,Qty)
    return TransData, TransDataReal

def Product_Position(filename):
    '''
    :param csv
    :return: dic {product:positioncode}
    '''
    #with open(filename,'r') as f:
    f = open(filename,encoding = 'utf-8')
    count = 0
    ProductPosition = dict()

    for line in f.readlines():
        count += 1
        line = line.replace('\n','')
        LineSpilt = line.split(',',3)
        if count == 1:
            continue
        ProductPosition[LineSpilt[1]] = LineSpilt[0]
    return ProductPosition

def ExchangeResult_Process(filename):
    '''
    :param filename:
    :return: ExchangeResultProcess
    '''
    f = open(filename,encoding = 'utf-8')
    count = 0
    ExchangeResultProcess = []
    Temp = dict()
    for line in f.readlines():
        count += 1
        line = line.replace('\n','')
        line = line.replace(' ', '')
        LineSpilt = line.split(',',4)
        if count == 1:
            continue
        Temp[LineSpilt[0]] = LineSpilt[1]
        Temp[LineSpilt[2]] = LineSpilt[3]
        ExchangeResultProcess.append(copy.deepcopy(Temp))
        Temp.clear()
    return ExchangeResultProcess