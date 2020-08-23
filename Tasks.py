from bilibili import bilibili
import datetime
import time
import asyncio
import traceback
import os
import configloader
import utils
import ast
from printer import Printer


class Tasks:

    def __init__(self):
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        file_user = fileDir + "/conf/user.conf"
        self.dic_user = configloader.load_user(file_user)

    # 获取每日包裹奖励
    async def Daily_bag(self):
        response = await bilibili().get_dailybag()
        json_response = await response.json()
        for i in range(0, len(json_response['data']['bag_list'])):
            Printer().printer(f"获得-{json_response['data']['bag_list'][i]['bag_name']}-成功", "Info", "green")

    def CurrentTime(self):
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime

    # 签到功能
    async def DoSign(self):
        response = await bilibili().get_dosign()
        temp = await response.json(content_type=None)
        Printer().printer(f"签到状态:{temp['message']}", "Info", "green")

    # 应援团签到
    async def link_sign(self):
        response = await bilibili().get_grouplist()
        json_response = await response.json(content_type=None)
        check = len(json_response['data']['list'])
        group_id_list = []
        owner_uid_list = []
        for i in range(0, check):
            group_id = json_response['data']['list'][i]['group_id']
            owner_uid = json_response['data']['list'][i]['owner_uid']
            group_id_list.append(group_id)
            owner_uid_list.append(owner_uid)
        for (i1, i2) in zip(group_id_list, owner_uid_list):
            response = await bilibili().assign_group(i1, i2)
            json_response = await response.json(content_type=None)
            if json_response['code'] == 0:
                if (json_response['data']['status']) == 1:
                    Printer().printer(f"应援团{i1}已应援过", "Info", "green")
                if (json_response['data']['status']) == 0:
                    Printer().printer(f"应援团{i1}应援成功,获得{json_response['data']['add_num']}点亲密度", "Info", "green")
            else:
                Printer().printer(f"应援团{i1}应援失败,{json_response}", "Error", "red")

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
                Printer().printer(f"没有将要过期的礼物~", "Info", "green")

    async def auto_send_gift(self):
        if self.dic_user['auto-gift']['on/off'] == "1":
            a = await utils.fetch_medal(printer=False)
            # res = await bilibili().gift_list()
            # json_res = await res.json()
            # temp_dic = {}
            # for j in range(0, len(json_res['data'])):
            #     price = json_res['data'][j]['price']
            #     id = json_res['data'][j]['id']
            #     temp_dic[id] = price
            temp_dic = {1: 100, 6: 1000}
            if self.dic_user['send_exheart']['on/off'] == "1":
                temp_dic = {1: 100, 6: 1000, 30607: 5000}
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
                if gift_id in [1, 6] and expire != 0:
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
            Printer().printer(f"自动送礼共送出亲密度为{int(calculate)}的礼物", "Info", "green")

    async def doublegain_coin2silver(self):
        if self.dic_user['doublegain_coin2silver']['on/off'] == "1":
            response0 = await bilibili().request_doublegain_coin2silver()
            json_response0 = await response0.json()
            response1 = await bilibili().request_doublegain_coin2silver()
            json_response1 = await response1.json()
            print(json_response0['msg'], json_response1['msg'])

    async def coin2silver(self):
        if self.dic_user['coin2silver']['on/off'] == '1' and int(self.dic_user['coin2silver']['num']) > 0:
            response = await bilibili().coin2silver_web(self.dic_user['coin2silver']['num'])
            json_response = await response.json()
            Printer().printer(f"硬币兑换银瓜子状态:{json_response['msg']}", "Info", "green")

    async def sliver2coin(self):
        if self.dic_user['coin']['on/off'] == '1':
            response1 = await bilibili().silver2coin_app()
            json_response1 = await response1.json()
            Printer().printer(f"银瓜子兑换硬币状态:{json_response1['msg']}", "Info", "green")

    async def refresh_medals(self):
        if self.dic_user['refresh_medals']['on/off'] == '1':
            await utils.refresh_all_gray_medals()

    async def refresh_medals_by_roomid(self):
        if self.dic_user['refresh_medals_by_roomid']['on/off'] == "1":
            roomids = ast.literal_eval(self.dic_user['refresh_medals_by_roomid']['room_ids'])
            await utils.refresh_medals_by_roomids(roomids)

    async def get_rooms(self):
        room_ids = []
        for _ in range(3):
            response = await bilibili().request_fetchmedal()
            json_response = await response.json(content_type=None)
            if json_response['code']:
                continue
            # 有时候dict获取不完整，包括最后一项"roomid"的后半部分缺失
            elif all(["roomid" not in medal for medal in json_response['data']['fansMedalList']]):
                continue
            else:
                break

        for i in range(0, len(json_response['data']['fansMedalList'])):
            short_room_id = json_response['data']['fansMedalList'][i].get('roomid', None)
            if short_room_id is None:
                continue
            response1 = await bilibili().get_room_info(short_room_id)
            json_response1 = await response1.json(content_type=None)
            long_room_id = json_response1['data']['room_info']['room_id']
            room_ids.append(long_room_id)
        return room_ids

    async def XE_heartbeat(self, room_ids, room_id):
        index_num = 24 // len(room_ids)
        index_num += 1 if 24 % len(room_ids) else 0
        data = await bilibili().heart_beat_e(room_id)
        for index in range(1, index_num + 1):
            try:
                # print(f"房间{room_id}休眠{data['heartbeat_interval']}s后开始第 {index} 次")
                await asyncio.sleep(data['heartbeat_interval'])
                response = await bilibili().heart_beat_x(index, data, room_id)
                response = await response.json(content_type=None)
                data['ets'] = response['data']['timestamp']
                data['secret_key'] = response['data']['secret_key']
                data['heartbeat_interval'] = response['data']['heartbeat_interval']
            except:
                pass

    async def run(self):
        while 1:
            try:
                Printer().printer(f"开始执行每日任务", "Info", "green")
                await self.DoSign()
                room_ids = await self.get_rooms()
                coroutine_list = []
                for room_id in room_ids:
                    coroutine_list.append(self.XE_heartbeat(room_ids, room_id))
                if coroutine_list:
                    await asyncio.wait(coroutine_list)
                await self.refresh_medals_by_roomid()
                await self.refresh_medals()
                await self.Daily_bag()
                await self.link_sign()
                await self.send_gift()
                await self.sliver2coin()
                await self.coin2silver()
                await self.auto_send_gift()
                await utils.reconnect()
                await asyncio.sleep(21600)
            except:
                await asyncio.sleep(10)
                Printer().printer(traceback.format_exc(), "Error", "red")
