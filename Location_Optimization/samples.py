#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# create time: 15/01/2018 17:08
__author__ = 'Devin -- http://zhangchuzhao.site'
import json
import logging
import requests
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    # *************************************这里填写自己钉钉群自定义机器人的token*****************************************
    webhook = 'https://oapi.dingtalk.com/robot/send?access_token=52d9034cc78680bc0d4ba6a65748e77fa7b96ee43d57b96116910606f7863d59'
    # 用户手机号列表
    at_mobiles = ['*************************这里填写需要提醒的用户的手机号码，字符串或数字都可以****************************']
    # 初始化机器人小丁
    xiaoding = DingtalkChatbot(webhook)
    # text
    xiaoding.send_text(msg='我就是小丁，小丁就是我！', is_at_all=True)
    xiaoding.send_text(msg='我就是小丁，小丁就是我！', at_mobiles=at_mobiles)

    # markdown
    # 1、提醒所有人
    xiaoding.send_markdown(title='氧气文字', text='#### 广州天气\n'
                           '> 9度，西北风1级，空气良89，相对温度73%\n\n'
                           '> ![美景](http://www.sinaimg.cn/dy/slidenews/5_img/2013_28/453_28488_469248.jpg)\n'
                           '> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n',
                           is_at_all=True)
    # 2、提醒指定手机用户，需要在text参数中@用户
    xiaoding.send_markdown(title='氧气文字', text='#### 广州天气\n'
                           '> 9度，西北风1级，空气良89，相对温度73%\n\n'
                           '> ![美景](http://www.sinaimg.cn/dy/slidenews/5_img/2013_28/453_28488_469248.jpg)\n'
                           '> ###### 10点20分发布 [天气](http://www.thinkpage.cn/) \n',
                           at_mobiles=at_mobiles)


