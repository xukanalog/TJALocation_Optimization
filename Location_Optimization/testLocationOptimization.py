import datetime
import LocationOptimization
import xlwt
import time
import ExcelScreenShots
import ChatbotInit

def Excel_Write(OptimizaAnalyseBeforeList,OptimizaAnalyseAfterList):
    '''
    :param OptimizaAnalyseBeforeList:  list 库位优化前通道标准差
    :param OptimizaAnalyseAfterList:   list 库位优化后通道标准差
    :return:
    '''

    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('Result')
    for i in range(len(OptimizaAnalyseBeforeList)):
        worksheet.write(i,0,OptimizaAnalyseBeforeList[i])
        worksheet.write(i,1,OptimizaAnalyseAfterList[i])
    workbook.save("./excel/Test.xls")
    return 0


if __name__ == '__main__':
    Start = time.clock()
    CurTime = datetime.datetime.now()
    CurTimeFormat = CurTime.strftime("%Y-%m-%d")
    YesTimeFormat = (CurTime - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
    OptimizaAnalyseBeforeList = []
    OptimizaAnalyseAfterList = []
    for RowsChange in range(20):
        RowsChangePerTime = 20
        OptimizaAnalyseBefore, OptimizaAnalyseAfter = LocationOptimization.Location_Optimization(YesTimeFormat, CurTimeFormat, RowsChange,RowsChangePerTime)
        OptimizaAnalyseBeforeList.append(OptimizaAnalyseBefore)
        OptimizaAnalyseAfterList.append(OptimizaAnalyseAfter)

    Excel_Write(OptimizaAnalyseBeforeList, OptimizaAnalyseAfterList)
    #ImageName = ExcelScreenShots.Excel_CatchScreen(
       # "D:/alog/天津仓/Algorithm/Dingtalk/Location_Optimization/excel/ExchangeResult.xls", "Result", "A1:B10")

    print("The Program is successfully %s"%(time.clock() - Start))

    print('111')#https://www.aliyun.com/jiaocheng/124652.html