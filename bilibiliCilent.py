from bilibili import bilibili
from statistics import Statistics
from printer import Printer
from rafflehandler import Rafflehandler
import utils
import asyncio
import random
import struct
import json
import re
import sys


async def handle_1_TV_raffle(type, num, real_roomid, raffleid):
    # await asyncio.sleep(random.uniform(0.1, min(1, num * 1)))
    response2 = await bilibili().get_gift_of_TV(type, real_roomid, raffleid)
    # response1 = await bilibili().get_gift_of_events_app(real_roomid,raffleid)
    Printer().printlist_append(['join_lottery', '广播道具', 'user', "参与了房间{:^9}的广播抽奖".format(real_roomid)], True)
    # json_response1 = await response1.json()
    json_response2 = await response2.json()
    # print(json_response1)
    Printer().printlist_append(
        ['join_lottery', '广播道具', 'user', "广播道具抽奖状态: ", json_response2['msg']], True)
    if json_response2['code'] == 0:
        Statistics().append_to_TVlist(raffleid, real_roomid)
    else:
        print(json_response2)


async def handle_1_activity_raffle(num, text1, raffleid):
    # await asyncio.sleep(random.uniform(0.1, min(1, num * 1)))
    response1 = await bilibili().get_gift_of_events_app(text1, raffleid)
    # pc_response = await bilibili().get_gift_of_events_web(text1, raffleid)

    Printer().printlist_append(['join_lottery', '', 'user', "参与了房间{:^9}的活动抽奖".format(text1)], True)

    json_response1 = await response1.json()
    # json_pc_response = await pc_response.json()
    # print(json_pc_response)
    if json_response1['code'] == 0:
        Printer().printlist_append(['join_lottery', '', 'user', "移动端活动抽奖结果: ",
                                    json_response1['data']['gift_desc']], True)
        Statistics().add_to_result(*(json_response1['data']['gift_desc'].split('X')))
    else:
        print(json_response1)
        Printer().printlist_append(['join_lottery', '', 'user', "移动端活动抽奖结果: ", json_response1['message']], True)
    # if json_pc_response['code'] == 0:
    #     Statistics().append_to_activitylist(raffleid, text1)
    # else:
    #     print(json_pc_response)


async def handle_1_room_TV(real_roomid):
    # await asyncio.sleep(random.uniform(0.1, 0.15))
    result = await utils.check_room_true(real_roomid)
    if True in result:
        Printer().printlist_append(['join_lottery', '钓鱼提醒', 'user', "WARNING:检测到房间{:^9}的钓鱼操作".format(real_roomid)],
                                   True)
    else:
        await bilibili().post_watching_history(real_roomid)
        response = await bilibili().get_giftlist_of_TV(real_roomid)
        json_response = await response.json()
        checklen = json_response['data']['list']
        num = len(checklen)
        list_available_raffleid = []
        for j in range(0, num):
            raffleid = json_response['data']['list'][j]['raffleId']
            type = json_response['data']['list'][j]['type']
            if Statistics().check_TVlist(raffleid):
                list_available_raffleid.append([type, raffleid])
        tasklist = []
        num_available = len(list_available_raffleid)
        for k in list_available_raffleid:
            task = asyncio.ensure_future(handle_1_TV_raffle(k[0], num_available, real_roomid, k[1]))
            tasklist.append(task)
        if tasklist:
            await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)


async def handle_1_room_activity(text1):
    # await asyncio.sleep(random.uniform(0.5, 1))
    result = await utils.check_room_true(text1)
    if True in result:
        Printer().printlist_append(['join_lottery', '钓鱼提醒', 'user', "WARNING:检测到房间{:^9}的钓鱼操作".format(text1)], True)
    else:
        # print(True)
        await bilibili().post_watching_history(text1)
        response = await bilibili().get_giftlist_of_events(text1)
        json_response = await response.json()
        checklen = json_response['data']['lotteryInfo']
        num = len(checklen)
        list_available_raffleid = []
        for j in range(0, num):
            # await asyncio.sleep(random.uniform(0.5, 1))
            raffleid = checklen[j]['eventType']
            if Statistics().check_activitylist(raffleid):
                list_available_raffleid.append(raffleid)
        tasklist = []
        num_available = len(list_available_raffleid)
        for raffleid in list_available_raffleid:
            task = asyncio.ensure_future(handle_1_activity_raffle(num_available, text1, raffleid))
            tasklist.append(task)
        if tasklist:
            await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)



class bilibiliClient():

    def __init__(self, roomid,area_name):
        self.bilibili = bilibili()
        self._reader = None
        self._writer = None
        self._uid = None
        self.connected = False
        self._UserCount = 0
        self.dic_bulletin = {
            'cmd': 'str',
            'msg': 'str',
            'rep': 'int',
            'url': 'str'
        }
        self._roomId = roomid
        self.area_name = area_name

    def close_connection(self):
        self._writer.close()
        self._connected = False

    async def connectServer(self):
        try:
            reader, writer = await asyncio.open_connection(self.bilibili.dic_bilibili['_ChatHost'],
                                                           self.bilibili.dic_bilibili['_ChatPort'])
        except:
            print("连接无法建立，请检查本地网络状况")
            return
        self._reader = reader
        self._writer = writer
        if (await self.SendJoinChannel(self._roomId) == True):
            self.connected = True
            Printer().printlist_append(['join_lottery', '', 'user', '连接 {0:^9} [{1}]弹幕服务器成功'.format(self._roomId,self.area_name)], True)
            await self.ReceiveMessageLoop()

    async def HeartbeatLoop(self):
        while self.connected == False:
            await asyncio.sleep(0.5)

        # Printer().printlist_append(['join_lottery', '', 'user', '弹幕模块开始心跳'], True)

        while self.connected == True:
            await self.SendSocketData(0, 16, self.bilibili.dic_bilibili['_protocolversion'], 2, 1, "")
            await asyncio.sleep(30)

    async def SendJoinChannel(self, channelId):
        self._uid = (int)(100000000000000.0 + 200000000000000.0 * random.random())
        body = '{"roomid":%s,"uid":%s}' % (channelId, self._uid)
        await self.SendSocketData(0, 16, self.bilibili.dic_bilibili['_protocolversion'], 7, 1, body)
        return True

    async def SendSocketData(self, packetlength, magic, ver, action, param, body):
        bytearr = body.encode('utf-8')
        if packetlength == 0:
            packetlength = len(bytearr) + 16
        sendbytes = struct.pack('!IHHII', packetlength, magic, ver, action, param)
        if len(bytearr) != 0:
            sendbytes = sendbytes + bytearr
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), sendbytes)
        try:
            self._writer.write(sendbytes)
        except:
            print(sys.exc_info()[0], sys.exc_info()[1])
            self.connected = False

        await self._writer.drain()

    async def ReadSocketData(self, len_wanted):
        bytes_data = b''
        if len_wanted == 0:
            return bytes_data
        len_remain = len_wanted
        while len_remain != 0:
            try:
                tmp = await asyncio.wait_for(self._reader.read(len_remain), timeout=35.0)
            except asyncio.TimeoutError:
                print('由于心跳包30s一次，但是发现35内没有收到任何包，说明已经悄悄失联了，主动断开')
                self._writer.close()
                self.connected = False
                return None
            except ConnectionResetError:
                print('RESET，网络不稳定或者远端不正常断开')
                self._writer.close()
                self.connected = False
                return None
            except asyncio.CancelledError:

                return None
            except:
                print(sys.exc_info()[0], sys.exc_info()[1])
                print('请联系开发者')
                self._writer.close()
                self.connected = False
                return None

            if not tmp:
                print("主动关闭或者远端主动发来FIN")
                self._writer.close()
                self.connected = False
                return None
            else:
                bytes_data = bytes_data + tmp
                len_remain = len_remain - len(tmp)

        return bytes_data

    async def ReceiveMessageLoop(self):
        while self.connected == True:
            tmp = await self.ReadSocketData(16)
            if tmp is None:
                break

            expr, = struct.unpack('!I', tmp[:4])

            num, = struct.unpack('!I', tmp[8:12])

            num2 = expr - 16

            tmp = await self.ReadSocketData(num2)
            if tmp is None:
                break

            if num2 != 0:
                num -= 1
                if num == 0 or num == 1 or num == 2:
                    num3, = struct.unpack('!I', tmp)
                    self._UserCount = num3
                    continue
                elif num == 3 or num == 4:
                    try:
                        messages = tmp.decode('utf-8')
                    except:
                        continue
                    await self.parseDanMu(messages)
                    continue
                elif num == 5 or num == 6 or num == 7:
                    continue
                else:
                    if num != 16:
                        pass
                    else:
                        continue

    async def parseDanMu(self, messages):
        try:
            dic = json.loads(messages)

        except:
            return
        cmd = dic['cmd']

        if cmd == 'PREPARING':

            Printer().printlist_append(['join_lottery', '', 'user', "房间 {:^9} 下播！将切换监听房间".format(self._roomId)], True)
            try:
                await utils.reconnect()
            except:
                print("切换房间失败,休眠5s后再次尝试")
                await asyncio.sleep(5)
                await utils.reconnect()

        elif cmd == 'DANMU_MSG':
            # print(dic)
            Printer().printlist_append(['danmu', '弹幕', 'user', dic])
            return
        elif cmd == 'SYS_GIFT':
            try:
                text1 = dic['real_roomid']
                text2 = dic['url']
                Printer().printlist_append(['join_lottery', '', 'user', "检测到房间{:^9}的活动抽奖".format(text1)], True)
                Rafflehandler().append2list_activity(text1)
                Statistics().append2pushed_activitylist()
            except:
                pass
            return
        elif cmd == 'SYS_MSG':
            if set(self.dic_bulletin) == set(dic):
                Printer().printlist_append(['join_lottery', '系统公告', 'user', dic['msg']])
            else:
                try:
                    TV_url = dic['url']
                    real_roomid = dic['real_roomid']
                    Printer().printlist_append(['join_lottery', '小电视', 'user', "检测到房间{:^9}的广播抽奖".format(real_roomid)],
                                               True)
                    Rafflehandler().append2list_TV(real_roomid)
                    Rafflehandler().append2list_activity(real_roomid)
                    Statistics().append2pushed_TVlist()
                    Statistics().append2pushed_activitylist()
                except:
                    print('SYS_MSG出错，请联系开发者', dic)
            return
        elif cmd == "WELCOME":
            pass
        elif cmd == "SEND_GIFT":
            pass
        elif cmd == "WELCOME_GUARD":
            pass
        elif cmd == "WISH_BOTTLE":
            pass
        elif cmd == "COMBO_END":
            pass
        elif cmd == "ENTRY_EFFECT":
            pass
        elif cmd == "ROOM_RANK":
            pass
        elif cmd == "COMBO_SEND":
            pass
        elif cmd == "ROOM_BLOCK_MSG":
            pass
        elif cmd == "SPECIAL_GIFT":
            pass
        else:
            Printer().printlist_append(['join_lottery', '小电视', 'user', "出现一个未知msg{}".format(dic)],
                                       True)