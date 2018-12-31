import time
import datetime

if __name__ == '__main__':
    while(True):
        time.sleep(5)
        print('5秒过去啦')
        pass






    while(True):
        NowTime = datetime.datetime.now()
        if NowTime.minute == 0 and NowTime.second == 0:
            pass