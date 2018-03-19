from login import Login
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
            await asyncio.sleep(3600)
