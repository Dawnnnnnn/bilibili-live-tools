# !/usr/bin/python
# coding:utf-8
import datetime
import hashlib
import requests
import time

access_key = ''    # 示例：5dd42a8149a8799b809b700298483f5e
cookies = ''    #示例：DedeUserID=229771359;DedeUserID__ckMd5=8147bbdcf5335b47;LIVE_LOGIN_DATA=;LIVE_LOGIN_DATA__ckMd5=;SESSDATA=92bc4295%2C1514638540%2C496dc054;sid=6rrncwlc;bili_jct=c9ea8a9d0d2a3c1c80509e5f4ce1fcae;

roomid = '23058'    # 需要分享的直播间号(23058默认音乐台)
uid = ''   # 你自己的uid 示例：229771359

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
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'accept-encoding': 'gzip, deflate',
    'authority': 'live.bilibili.com',
    'cookie': cookies,
}


# 获取每日包裹奖励
def Daily_bag(headers):
    url = 'http://api.live.bilibili.com/gift/v2/live/receive_daily_bag'
    response = requests.get(url, headers=headers)
    try:
        print("获得----" + response.json()['data']['bag_list'][0]['bag_name'] + "----成功")
    except:
        pass


def CurrentTime():
    currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
    return currenttime


# 签到功能
def DoSign(headers):
    url = 'https://api.live.bilibili.com/sign/doSign'
    response = requests.get(url, headers=headers)
    temp = response.json()
    print(temp['msg'])


def share_sign():
    temp= uid + roomid + 'bilibili'
    hash = hashlib.md5()
    hash.update(temp.encode('utf-8'))
    fk_md5 = str(hash.hexdigest())
    temp_fk_md5 = fk_md5 + 'bilibili'
    hash = hashlib.sha1()
    hash.update(temp_fk_md5.encode('utf-8'))
    share_sign = (hash.hexdigest())
    return share_sign

# 分享直播间任务
def ShareRoom(headers):
    time = CurrentTime()
    temp_params = 'access_key='+access_key+'&actionKey='+actionKey+'&appkey='+appkey+'&build='+build+'&device='+device+'&mobi_app='+mobi_app+'&platform='+platform+'&roomid='+roomid+'&share_sign='+str(share_sign())+'&sharing_plat=qq'+'&ts='+time
    params = temp_params + '560c52ccd288fed045859ed18bffd973'
    hash = hashlib.md5()
    hash.update(params.encode('utf-8'))
    sign = hash.hexdigest()
    true_url = 'https://api.live.bilibili.com/activity/v1/Common/shareCallback?' + temp_params + '&sign=' + str(hash.hexdigest())
    response = requests.get(true_url,headers=headers)
    print(response.json()['msg'])


# 领取每日任务奖励
def Daily_Task(headers):
    url = 'https://api.live.bilibili.com/activity/v1/task/receive_award'
    payload1 = {'task_id':'single_watch_task'}
    response1 =requests.post(url,data=payload1,headers=headers)
    payload2 = {'task_id':'double_watch_task'}
    response2 = requests.post(url,data=payload2,headers=headers)
    payload3 = {'task_id':'share_task'}
    response3 = requests.post(url,data=payload3,headers=headers)
    print("今日每日任务已完成")


while 1:
    print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    DoSign(headers)
    ShareRoom(headers)
    Daily_bag(headers)
    Daily_Task(headers)
    time.sleep(3600)
