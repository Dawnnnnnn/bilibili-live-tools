#!/usr/bin/python
#coding:utf-8
import hashlib
import requests
import datetime
import time


access_key = ''    # 示例：5dd42a8149a8799b809b700298483f5e
cookies = ''    #示例：DedeUserID=229771359;DedeUserID__ckMd5=8147bbdcf5335b47;LIVE_LOGIN_DATA=;LIVE_LOGIN_DATA__ckMd5=;SESSDATA=92bc4295%2C1514638540%2C496dc054;sid=6rrncwlc;bili_jct=c9ea8a9d0d2a3c1c80509e5f4ce1fcae;

# 底下这些都是固定值，一时不会变
appkey = '1d8b6e7d45233436'
actionKey = 'appkey'
build = '520001'
device = 'android'
mobi_app = 'android'
platform = 'android'

headers = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Accept-Language' : 'zh-CN,zh;q=0.9',
    'accept-encoding':'gzip, deflate',
    'authority': 'live.bilibili.com',
    'cookie': cookies,
}


# 获取当前系统时间的unix时间戳
def CurrentTime():
    currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
    return currenttime


# 将time_end时间转换成正常时间
def DataTime():
    datatime = str(datetime.datetime.fromtimestamp(float(time_end(headers))))
    return datatime


# 领瓜子时判断领取周期的参数
def time_start(headers):
        time = CurrentTime()
        temp_params = 'access_key='+access_key+'&actionKey='+actionKey+'&appkey='+appkey+'&build='+build+'&device='+device+'&mobi_app='+mobi_app+'&platform='+platform+'&ts='+time
        params = temp_params + '560c52ccd288fed045859ed18bffd973'
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        GetTask_url = 'https://api.live.bilibili.com/mobile/freeSilverCurrentTask?'+temp_params+'&sign='+str(hash.hexdigest())
        response = requests.get(GetTask_url,headers=headers)
        temp = response.json()
        # print (temp['code'])    #宝箱领完返回的code为-10017
        if temp['code'] == -10017:
            print ("今天的瓜子领完了")
        else:
            time_start = temp['data']['time_start']
            print (time_start)
            return str(time_start)


# 领瓜子时判断领取周期的参数
def time_end(headers):
    try:
        time = CurrentTime()
        temp_params = 'access_key='+access_key+'&actionKey='+actionKey+'&appkey='+appkey+'&build='+build+'&device='+device+'&mobi_app='+mobi_app+'&platform='+platform+'&ts='+time
        params = temp_params + '560c52ccd288fed045859ed18bffd973'
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        GetTask_url = 'https://api.live.bilibili.com/mobile/freeSilverCurrentTask?'+temp_params+'&sign='+str(hash.hexdigest())
        response = requests.get(GetTask_url,headers=headers)
        temp = response.json()
        time_end = temp['data']['time_end']
        return str(time_end)
    except:
        pass


# 领取银瓜子
def GetAward(headers):
    try:
        time = CurrentTime()
        timeend = time_end(headers)
        timestart = time_start(headers)
        temp_params = 'access_key='+access_key+'&actionKey='+actionKey+'&appkey='+appkey+'&build='+build+'&device='+device+'&mobi_app='+mobi_app+'&platform='+platform+'&time_end='+timeend+'&time_start='+timestart+'&ts='+time
        params = temp_params + '560c52ccd288fed045859ed18bffd973'
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        url = 'https://api.live.bilibili.com/mobile/freeSilverAward?'+temp_params+'&sign='+str(hash.hexdigest())
        response = requests.get(url, headers=headers)
        print(response.json())
        return response.json()['code']
    except:
        pass


while 1:
    temp = GetAward(headers)
    if temp == None or temp == -10017:
        print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        print("十分钟后检测一次是否到第二天了")
        time.sleep(600)
    elif temp == 0:
        print ("当前时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        GetAward(headers)
    else:
        print ("当前时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        time.sleep(181)
