import datetime
import LocationOptimization
import ExcelScreenShots
import ChatbotInit

if __name__ == '__main__':
    CurTime = datetime.datetime.now()
    CurTimeFormat = CurTime.strftime("%Y-%m-%d")
    YesTimeFormat = (CurTime - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
    OptimizaAnalyseBefore, OptimizaAnalyseAfter = LocationOptimization.Location_Optimization(YesTimeFormat, CurTimeFormat)
    ImageName = ExcelScreenShots.Excel_CatchScreen(
        "D:/alog/天津仓/Algorithm/Dingtalk/Location_Optimization/excel/ExchangeResult.xls", "Result", "A1:B10")

    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=6661d45e234542fd8bbbce2d0ed37dc27d7e55f4a5c65e176ecf1921c5817f2a'
    at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
    xiaoding = ChatbotInit.DingtalkChatbot(webhook)

    # markdown
    # 1、提醒所有人
    xiaoding.send_markdown(title='A区库位优化表', text='#### A区库位优化\n'
    '> ![测试](http://alogxukan.vaiwan.com:8081/alog/%s)\n'%(ImageName),
    #'> ![测试](http://alogxukan.vaiwan.com:8081/alog/19d9dc0f-5bfa-4b0c-b17b-eec9c130e099.PNG)\n',
                                             # '> 9度，西北风1级，空气良89，相对温度73%\n\n'
                                             # '> ![美景](http://www.sinaimg.cn/dy/slidenews/5_img/2013_28/453_28488_469248.jpg)\n'
                                             # '> ###### 10点20分发布 [天ss气](http://www.thinkpage.cn/) \n',
                           is_at_all=True)

    print('111')#https://www.aliyun.com/jiaocheng/124652.html


