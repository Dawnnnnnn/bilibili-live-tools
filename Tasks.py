from bilibili import bilibili
import datetime
import time
import asyncio
import traceback
import os
import configloader
import utils
from printer import Printer


class Tasks():

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        file_user = fileDir + "/conf/user.conf"
        self.dic_user = configloader.load_user(file_user)

    # 获取每日包裹奖励
    async def Daily_bag(self):
        response = await bilibili().get_dailybag()
        json_response = await response.json()
        for i in range(0, len(json_response['data']['bag_list'])):
            Printer().printlist_append(
                ['join_lottery', '', 'user', "获得-" + json_response['data']['bag_list'][i]['bag_name'] + "-成功"], True)

    def CurrentTime(self):
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime

    # 签到功能
    async def DoSign(self):
        response = await bilibili().get_dosign()
        temp = await response.json(content_type=None)
        Printer().printlist_append(['join_lottery', '', 'user', "签到状态:", temp['msg']], True)

    # 领取每日任务奖励
    async def Daily_Task(self):
        response2 = await bilibili().get_dailytask()
        json_response2 = await response2.json()
        Printer().printlist_append(['join_lottery', '', 'user', "双端观看直播:", json_response2["msg"]], True)

    # 应援团签到
    async def link_sign(self):
        response = bilibili().get_grouplist()
        check = len(response.json()['data']['list'])
        group_id_list = []
        owner_uid_list = []
        for i in range(0, check):
            group_id = response.json()['data']['list'][i]['group_id']
            owner_uid = response.json()['data']['list'][i]['owner_uid']
            group_id_list.append(group_id)
            owner_uid_list.append(owner_uid)
        for (i1, i2) in zip(group_id_list, owner_uid_list):
            response = bilibili().assign_group(i1, i2)
            if response.json()['code'] == 0:
                if (response.json()['data']['status']) == 1:
                    Printer().printlist_append(['join_lottery', '', 'user', "# 应援团 %s 已应援过" % (i1)])
                if (response.json()['data']['status']) == 0:
                    Printer().printlist_append(['join_lottery', '', 'user',
                                                "# 应援团 %s 应援成功,获得 %s 点亲密度" % (i1, response.json()['data']['add_num'])])
            else:
                Printer().printlist_append(['join_lottery', '', 'user', "# 应援团 %s 应援失败" % (i1)])

    async def send_gift(self):
        if self.dic_user['gift']['on/off'] == '1':
            argvs, x = await utils.fetch_bag_list(printer=False)
            for i in range(0, len(argvs)):
                giftID = argvs[i][0]
                giftNum = argvs[i][1]
                bagID = argvs[i][2]
                roomID = self.dic_user['gift']['send_to_room']
                await utils.send_gift_web(roomID, giftID, giftNum, bagID)
            if not argvs:
                Printer().printlist_append(['join_lottery', '', 'user', "没有将要过期的礼物~"])

    async def auto_send_gift(self):
        if self.dic_user['auto-gift']['on/off'] == "1":
            a = await utils.fetch_medal(printer=False)
            res = await bilibili().gift_list()
            json_res = await res.json()
            temp_dic = {}
            for j in range(0, len(json_res['data'])):
                price = json_res['data'][j]['price']
                id = json_res['data'][j]['id']
                temp_dic[id] = price
            x, temp = await utils.fetch_bag_list(printer=False)
            roomid = a[0]
            today_feed = a[1]
            day_limit = a[2]
            left_num = int(day_limit) - int(today_feed)
            calculate = 0
            for i in range(0, len(temp)):
                gift_id = int(temp[i][0])
                gift_num = int(temp[i][1])
                bag_id = int(temp[i][2])
                expire = int(temp[i][3])
                if (gift_id != 4 and gift_id != 3 and gift_id != 9 and gift_id != 10) and expire != 0:
                    if (gift_num * (temp_dic[gift_id] / 100) < left_num):
                        calculate = calculate + temp_dic[gift_id] / 100 * gift_num
                        tmp2 = temp_dic[gift_id] / 100 * gift_num
                        await utils.send_gift_web(roomid, gift_id, gift_num, bag_id)
                        left_num = left_num - tmp2
                    elif left_num - temp_dic[gift_id] / 100 >= 0:
                        tmp = (left_num) / (temp_dic[gift_id] / 100)
                        tmp1 = (temp_dic[gift_id] / 100) * int(tmp)
                        calculate = calculate + tmp1
                        await utils.send_gift_web(roomid, gift_id, tmp, bag_id)
                        left_num = left_num - tmp1
            Printer().printlist_append(['join_lottery', '', 'user', "自动送礼共送出亲密度为%s的礼物" % int(calculate)])

    async def doublegain_coin2silver(self):
        if self.dic_user['doublegain_coin2silver']['on/off'] == "1":
            response0 = await bilibili().request_doublegain_coin2silver()
            json_response0 = await response0.json()
            response1 = await bilibili().request_doublegain_coin2silver()
            json_response1 = await response1.json()
            print(json_response0['msg'], json_response1['msg'])

    async def sliver2coin(self):
        if self.dic_user['coin']['on/off'] == '1':
            response1 = await bilibili().silver2coin_app()
            json_response1 = await response1.json()
            Printer().printlist_append(['join_lottery', '', 'user', "", json_response1['msg']])

    async def run(self):
        while 1:
            try:
                Printer().printlist_append(['join_lottery', '', 'user', "执行每日任务"], True)
                await self.DoSign()
                await self.link_sign()
                await self.Daily_bag()
                await self.Daily_Task()
                await self.send_gift()
                await self.sliver2coin()
                await self.doublegain_coin2silver()
                await self.auto_send_gift()
                await asyncio.sleep(21600)
            except:
                await asyncio.sleep(10)
                traceback.print_exc()