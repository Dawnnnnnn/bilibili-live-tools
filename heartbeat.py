#!/usr/bin/python
#coding:utf-8
import hashlib
import requests
import time
import datetime


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


# 发送pc心跳包
def pcpost_heartbeat(headers):
    url = 'http://api.live.bilibili.com/User/userOnlineHeart'
    headers['Referer'] = "http://live.bilibili.com/3"
    response = requests.post(url, headers=headers)
    print ("pc端心跳状态：" + response.json()['message'])

# 发送app心跳包
def apppost_heartbeat(headers):
    time = CurrentTime()
    temp_params = 'access_key='+access_key+'&actionKey='+actionKey+'&appkey='+appkey+'&build='+build+'&device='+device+'&mobi_app='+mobi_app+'&platform='+platform+'&ts='+time
    params = temp_params + '560c52ccd288fed045859ed18bffd973'
    hash = hashlib.md5()
    hash.update(params.encode('utf-8'))
    url = 'https://api.live.bilibili.com/mobile/userOnlineHeart?' + temp_params + '&sign=' + str(hash.hexdigest())
    headers['Referer'] = "http://live.bilibili.com/3"
    payload = {'roomid':23058,'scale':'xhdpi'}
    response = requests.post(url,headers=headers,data=payload)
    print ("app端心跳状态：" + response.json()['message'])


# 获取当前系统时间的unix时间戳
def CurrentTime():
    currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
    return currenttime


# 获取用户信息
def GetUserInfo(headers):
    url = 'https://api.live.bilibili.com/User/getUserInfo?ts='+CurrentTime()
    response = requests.get(url, headers=headers)
    temp = response.json()
    name = temp['data']['uname']
    level = temp['data']['user_level']
    silver = temp['data']['silver']
    billCoin = temp['data']['billCoin']
    user_intimacy = temp['data']['user_intimacy']
    user_next_intimacy = temp['data']['user_next_intimacy']
    gold = temp['data']['gold']
    print ("昵称: %s 等级:%d 银瓜子:%d 金瓜子:%d 硬币:%d 经验值:%d/%d"%(name,level,silver,gold,billCoin,user_intimacy,user_next_intimacy))


def main(headers = {}):
    while 1:
        print ("当前时间:",time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        GetUserInfo(headers)
        apppost_heartbeat(headers)
        pcpost_heartbeat(headers)
        time.sleep(300)


main(headers)