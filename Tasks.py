from login import Login
import hashlib
import datetime
import requests
import time
import asyncio


class Tasks(Login):

    # 获取每日包裹奖励
    def Daily_bag(self):
        url = 'http://api.live.bilibili.com/gift/v2/live/receive_daily_bag'
        response = requests.get(url, headers=self.pcheaders)
        try:
            print("获得----" + response.json()['data']['bag_list'][0]['bag_name'] + "----成功")
        except:
            pass

    def CurrentTime(self):
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime

    # 签到功能
    def DoSign(self):
        url = 'https://api.live.bilibili.com/sign/doSign'
        response = requests.get(url, headers=self.pcheaders)
        temp = response.json()
        print(temp['msg'])

    # 领取每日任务奖励
    def Daily_Task(self):
        url = 'https://api.live.bilibili.com/activity/v1/task/receive_award'
        payload1 = {'task_id': 'single_watch_task'}
        response1 = requests.post(url, data=payload1, headers=self.appheaders)
        payload2 = {'task_id': 'double_watch_task'}
        response2 = requests.post(url, data=payload2, headers=self.appheaders)
        payload3 = {'task_id': 'share_task'}
        response3 = requests.post(url, data=payload3, headers=self.appheaders)
        print("今日每日任务已完成")

    # 应援团签到
    def link_sign(self):
        url = "https://api.vc.bilibili.com/link_group/v1/member/my_groups"
        response = requests.get(url,headers=self.pcheaders)
        check = len(response.json()['data']['list'])
        group_id_list = []
        owner_uid_list = []
        for i in range(0,check):
            group_id = response.json()['data']['list'][i]['group_id']
            owner_uid = response.json()['data']['list'][i]['owner_uid']
            group_id_list.append(group_id)
            owner_uid_list.append(owner_uid)
        for (i1,i2) in zip(group_id_list,owner_uid_list):
            temp_params = "_device="+self.device+"&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key="+self.access_key+"&appkey="+self.appkey+"&build="+self.build+"&group_id="+str(i1)+"&mobi_app="+self.mobi_app+"&owner_id="+str(i2)+"&platform="+self.platform+"&src=xiaomi&trace_id=20171224024300024&ts="+self.CurrentTime()+"&version=5.20.1.520001"
            params = temp_params + self.app_secret
            hash = hashlib.md5()
            hash.update(params.encode('utf-8'))
            url = "https://api.vc.bilibili.com/link_setting/v1/link_setting/sign_in?"+temp_params+"&sign="+str(hash.hexdigest())
            response = requests.get(url,headers=self.appheaders)
            if (response.json()['data']['status']) == 1:
                print("应援团 %s 已签到过"  %(i1) )
            if (response.json()['data']['status']) == 0:
                print("应援团 %s 签到成功,获得 %s 点亲密度"  %(i1,response.json()['data']['add_num']))

    # 扭蛋币
    def redleaf(self):
        url ="http://live.bilibili.com/redLeaf/kingMoneyGift"
        response = requests.get(url,headers=self.pcheaders)
        print("扭蛋币:",response.json()['msg'])

    async def run(self):
        while 1:
            print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            self.DoSign()
            self.Daily_bag()
            self.Daily_Task()
            self.redleaf()
            self.link_sign()
            await asyncio.sleep(21600)
