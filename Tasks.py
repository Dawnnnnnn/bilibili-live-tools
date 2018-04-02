from API import API
from bilibili import bilibili
import hashlib
import datetime
import requests
import time
import asyncio


class Tasks():
    
    def __init__(self, bilibili, configloader,api):
        self.bilibili = bilibili
        self.configloader = configloader
        self.api = api

    # 获取每日包裹奖励
    def Daily_bag(self):
        url = 'http://api.live.bilibili.com/gift/v2/live/receive_daily_bag'
        response = requests.get(url, headers=self.bilibili.pcheaders)
        for i in range(0,len(response.json()['data']['bag_list'])):
            print("# 获得-" + response.json()['data']['bag_list'][i]['bag_name'] + "-成功")


    def CurrentTime(self):
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime

    # 签到功能
    def DoSign(self):
        url = 'https://api.live.bilibili.com/sign/doSign'
        response = requests.get(url, headers=self.bilibili.pcheaders)
        temp = response.json()
        print("# 签到状态:",temp['msg'])

    # 领取每日任务奖励
    def Daily_Task(self):
        url = 'https://api.live.bilibili.com/activity/v1/task/receive_award'
        payload2 = {'task_id': 'double_watch_task'}
        response2 = requests.post(url, data=payload2, headers=self.bilibili.appheaders)
        print("# 双端观看直播:", response2.json()["msg"])

    # 应援团签到
    def link_sign(self):
        url = "https://api.vc.bilibili.com/link_group/v1/member/my_groups"
        pcheaders = self.bilibili.pcheaders.copy()
        pcheaders['Host'] = "api.vc.bilibili.com"
        response = requests.get(url,headers=pcheaders)
        check = len(response.json()['data']['list'])
        group_id_list = []
        owner_uid_list = []
        for i in range(0,check):
            group_id = response.json()['data']['list'][i]['group_id']
            owner_uid = response.json()['data']['list'][i]['owner_uid']
            group_id_list.append(group_id)
            owner_uid_list.append(owner_uid)
        for (i1,i2) in zip(group_id_list,owner_uid_list):
            temp_params = "_device="+self.bilibili.device+"&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key="+self.bilibili.access_key+"&appkey="+self.bilibili.appkey+"&build="+self.bilibili.build+"&group_id="+str(i1)+"&mobi_app="+self.bilibili.mobi_app+"&owner_id="+str(i2)+"&platform="+self.bilibili.platform+"&src=xiaomi&trace_id=20171224024300024&ts="+self.CurrentTime()+"&version=5.20.1.520001"
            params = temp_params + self.bilibili.app_secret
            hash = hashlib.md5()
            hash.update(params.encode('utf-8'))
            url = "https://api.vc.bilibili.com/link_setting/v1/link_setting/sign_in?"+temp_params+"&sign="+str(hash.hexdigest())
            self.bilibili.appheaders['Host'] = "api.vc.bilibili.com"
            response = requests.get(url,headers=self.bilibili.appheaders)
            if response.json()['code'] == 0:
                if (response.json()['data']['status']) == 1:
                    print("# 应援团 %s 已应援过"  %(i1) )
                if (response.json()['data']['status']) == 0:
                    print("# 应援团 %s 应援成功,获得 %s 点亲密度"  %(i1, response.json()['data']['add_num']))
            else:
                print("# 应援团 %s 应援失败" %(i1))

    def send_gift(self):
        if self.configloader.dic_user['gift']['on/off'] == "1":
            try:
                argvs = self.api.get_bag_list()
                for i in range(0,len(argvs)):
                    giftID = argvs[i][0]
                    giftNum = argvs[i][1]
                    bagID = argvs[i][2]
                    roomID = self.configloader.dic_user['gift']['send_to_room']
                    self.api.send_bag_gift_web(roomID,giftID,giftNum,bagID)
            except:
                print("# 没有将要过期的礼物~")

    def sliver2coin(self):
        if self.configloader.dic_user['coin']['on/off'] == "1":
            self.api.silver2coin()

    async def run(self):
        while 1:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "每日任务")
            self.send_gift()
            self.sliver2coin()
            self.DoSign()
            self.Daily_bag()
            self.Daily_Task()
            self.link_sign()
            await asyncio.sleep(21600)
