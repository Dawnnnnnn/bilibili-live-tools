from bilibili import bilibili
import hashlib
import datetime
import requests
import time
import asyncio
import os
import configloader
import utils

class Tasks():

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        file_user = fileDir + "/conf/user.conf"
        self.dic_user = configloader.load_user(file_user)
    
    # 获取每日包裹奖励
    def Daily_bag(self):
        response = bilibili().get_dailybag()
        for i in range(0,len(response.json()['data']['bag_list'])):
            print("# 获得-" + response.json()['data']['bag_list'][i]['bag_name'] + "-成功")


    def CurrentTime(self):
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime

    # 签到功能
    def DoSign(self):
        response = bilibili().get_dosign()
        temp = response.json()
        print("# 签到状态:",temp['msg'])

    # 领取每日任务奖励
    def Daily_Task(self):
        response2 = bilibili().get_dailytask()
        # print(response2.json())
        print("# 双端观看直播:", response2.json()["msg"])

    # 应援团签到
    def link_sign(self):
        response = bilibili().get_grouplist()
        check = len(response.json()['data']['list'])
        group_id_list = []
        owner_uid_list = []
        for i in range(0,check):
            group_id = response.json()['data']['list'][i]['group_id']
            owner_uid = response.json()['data']['list'][i]['owner_uid']
            group_id_list.append(group_id)
            owner_uid_list.append(owner_uid)
        for (i1,i2) in zip(group_id_list,owner_uid_list):
            response = bilibili().assign_group(i1, i2)
            if response.json()['code'] == 0:
                if (response.json()['data']['status']) == 1:
                    print("# 应援团 %s 已应援过"  %(i1) )
                if (response.json()['data']['status']) == 0:
                    print("# 应援团 %s 应援成功,获得 %s 点亲密度"  %(i1, response.json()['data']['add_num']))
            else:
                print("# 应援团 %s 应援失败" %(i1))

    def send_gift(self):
        if self.dic_user['gift']['on/off'] == '1':
            try:
                argvs = utils.fetch_bag_list()
                for i in range(0,len(argvs)):
                    giftID = argvs[i][0]
                    giftNum = argvs[i][1]
                    bagID = argvs[i][2]
                    roomID = self.dic_user['gift']['send_to_room']
                    utils.send_gift_web(roomID,giftID,giftNum,bagID)
            except:
                print("# 没有将要过期的礼物~")

    def sliver2coin(self):
        if self.dic_user['coin']['on/off'] == '1':
            bilibili().silver2coin()

    async def run(self):
        while 1:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "每日任务")
            self.sliver2coin()
            self.DoSign()
            self.Daily_bag()
            self.Daily_Task()
            self.link_sign()
            self.send_gift()
            # print('Tasks over.')
            await asyncio.sleep(21600)
