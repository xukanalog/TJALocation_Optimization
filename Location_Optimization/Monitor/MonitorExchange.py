from Monitor import Dbquery
import copy
import xlwt

def ExchangeResult_Process(filename):
    '''
    得到交换后的情况
    :param filename:
    :return: ExchangeResultProcess list [{positioncode:productcode,positioncode：productcode}]
    '''
    f = open(filename,encoding = 'utf-8')
    ExchangeResultProcess = []
    Temp = dict()
    for line in f.readlines():
        line = line.replace('\n','')
        line = line.replace(' ', '')
        LineSpilt = line.split(',',4)
        Temp[LineSpilt[0]] = LineSpilt[3]
        Temp[LineSpilt[2]] = LineSpilt[1]
        ExchangeResultProcess.append(copy.deepcopy(Temp))
        Temp.clear()
    return ExchangeResultProcess

def Get_JudgeExcel(worksheet,ChangePosition1,ChangeProductCode1,ChangePosition2,ChangeProductCode2,Row,JudgeResult):
    '''
    :param ChangePosition1,ChangePosition2:  交换表 的库位
    :param ChangeProductCode1,ChangeProductCode2:  交换表 的sku
    :param Row: excel 行 ，决定写在哪一行
    :param JudgeResult:
    '''

    worksheet.write(Row,0,ChangePosition1)
    worksheet.write(Row,1,ChangeProductCode1)
    worksheet.write(Row,2,ChangePosition2)
    worksheet.write(Row,3,ChangeProductCode2)
    worksheet.write(Row,4,JudgeResult)
    return 0

if __name__ == '__main__':
    ExchangeResultProcess =  ExchangeResult_Process("./ExchangeResult.csv")        #换的记录
    RealData  = Dbquery.Get_Monitor('4201-01-2-3')     #真实情况
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Result')
    Row = 0
    for exchangeresultprocess in ExchangeResultProcess:
        count = 0
        Row += 1
        for key, value in exchangeresultprocess.items():
            count += 1
            if count == 1:
                Tempkey = key
                Tempvalue = value
            if count == 2:
                print(Dbquery.Get_Monitor(Tempkey))
                if Dbquery.Get_Monitor(Tempkey) != 0 and Dbquery.Get_Monitor(key) != 0:   #防止查的交换库位现在已经没有sku
                    if Dbquery.Get_Monitor(Tempkey)[0] == Tempvalue \
                        and Dbquery.Get_Monitor(key)[0] == value:
                        pass
                        Judge = 1 #表示确实换成功
                    else:
                        Judge = 0
                else:
                    Judge = 0
                Get_JudgeExcel(worksheet, Tempkey, Tempvalue, key, value, Row, Judge)
    workbook.save("./MonitorResult.xls")

    print('111')