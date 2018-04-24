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
import requests
import sys

async def handle_1_TV_raffle(num, real_roomid, raffleid):
    #print('参与')
    await asyncio.sleep(random.uniform(0.5, min(10, num * 1)))
    response2 = await bilibili().get_gift_of_TV(real_roomid, raffleid)
    Printer().printlist_append(['join_lottery', '小电视', 'user', "参与了房间{:^9}的小电视抽奖".format(real_roomid)], True)
    json_response2 = await response2.json()
    Printer().printlist_append(
        ['join_lottery', '小电视', 'user', "小电视道具抽奖状态: ", json_response2['msg']],True)
    # -400不存在
    if json_response2['code'] == 0:
        Statistics().append_to_TVlist(raffleid, real_roomid)
    else:
        print(json_response2)
                    
async def handle_1_activity_raffle(num, text1, text2, raffleid):
    await asyncio.sleep(random.uniform(0.5, min(10, num * 1)))
    response1 = await bilibili().get_gift_of_events_app(text1, text2, raffleid)
    pc_response = await bilibili().get_gift_of_events_web(text1, text2, raffleid)
    
    Printer().printlist_append(['join_lottery', '', 'user', "参与了房间{:^9}的活动抽奖".format(text1)], True)

    json_response1 = await response1.json()
    json_pc_response = await pc_response.json()
    if json_response1['code'] == 0:
        Printer().printlist_append(['join_lottery', '', 'user', "移动端活动抽奖结果: ",
                                       json_response1['data']['gift_desc']],True)
        Statistics().add_to_result(*(json_response1['data']['gift_desc'].split('X')))
    else:
        print(json_response1)
        Printer().printlist_append(['join_lottery', '', 'user', "移动端活动抽奖结果: ", json_response1['message']],True)
        
    Printer().printlist_append(
            ['join_lottery', '', 'user', "网页端活动抽奖状态: ", json_pc_response['message']],True)
    if json_pc_response['code'] == 0:
        Statistics().append_to_activitylist(raffleid, text1)
    else:
        print(json_pc_response)
        
async def handle_1_room_TV(real_roomid):
    await asyncio.sleep(random.uniform(0.5, 1))
    result = await utils.check_room_true(real_roomid)
    if True in result:
        Printer().printlist_append(['join_lottery', '钓鱼提醒', 'user', "WARNING:检测到房间{:^9}的钓鱼操作".format(real_roomid)], True)
    else:
        # print(True)
        await bilibili().post_watching_history(real_roomid)
        response = await bilibili().get_giftlist_of_TV(real_roomid)
        json_response = await response.json()
        checklen = json_response['data']['unjoin']
        num = len(checklen)
        list_available_raffleid = []
        for j in range(0, num):
            # await asyncio.sleep(random.uniform(0.5, 1))
            resttime = json_response['data']['unjoin'][j]['dtime']
            raffleid = json_response['data']['unjoin'][j]['id']
            if Statistics().check_TVlist(raffleid):
                list_available_raffleid.append(raffleid)
        tasklist = []
        num_available = len(list_available_raffleid)
        for raffleid in list_available_raffleid:
            task = asyncio.ensure_future(handle_1_TV_raffle(num_available, real_roomid, raffleid))
            tasklist.append(task)
        if tasklist:
            await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)

async def handle_1_room_activity(text1, text2):
    await asyncio.sleep(random.uniform(0.5, 1))
    result = await utils.check_room_true(text1)
    if True in result:
        Printer().printlist_append(['join_lottery', '钓鱼提醒', 'user', "WARNING:检测到房间{:^9}的钓鱼操作".format(text1)], True)
    else:
        # print(True)
        await bilibili().post_watching_history(text1)
        response = await bilibili().get_giftlist_of_events(text1)
        json_response = await response.json()
        checklen = json_response['data']
        num = len(checklen)
        list_available_raffleid = []
        for j in range(0, num):
            # await asyncio.sleep(random.uniform(0.5, 1))
            resttime = checklen[j]['time']
            raffleid = checklen[j]['raffleId']
            if Statistics().check_activitylist(raffleid):
                list_available_raffleid.append(raffleid)      
        tasklist = []
        num_available = len(list_available_raffleid)
        for raffleid in list_available_raffleid:
            task = asyncio.ensure_future(handle_1_activity_raffle(num_available, text1, text2, raffleid))
            tasklist.append(task)
        if tasklist:
            await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)
                                                          


class bilibiliClient():

    def __init__(self):
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
    def close_connection(self):
        self._writer.close()
        self._connected = False
        

    async def connectServer(self):
        try:
            reader, writer = await asyncio.open_connection(self.bilibili.dic_bilibili['_ChatHost'], self.bilibili.dic_bilibili['_ChatPort'])
        except:
            print("连接无法建立，请检查本地网络状况")
            return
        self._reader = reader
        self._writer = writer
        if (await self.SendJoinChannel(self.bilibili.dic_bilibili['roomid']) == True):
            self.connected = True
            Printer().printlist_append(['join_lottery', '', 'user', '连接弹幕服务器成功'], True)
            await self.ReceiveMessageLoop()

    async def HeartbeatLoop(self):
        while self.connected == False:
            await asyncio.sleep(0.5)

        Printer().printlist_append(['join_lottery', '', 'user', '弹幕模块开始心跳（由于弹幕心跳间隔为30s，所以后续正常心跳不再提示）'], True)

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
            except :
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

        if cmd == 'DANMU_MSG':
            # print(dic)
            Printer().printlist_append(['danmu', '弹幕', 'user', dic])
            return
        if cmd == 'SYS_GIFT':
            try:
                text1 = dic['real_roomid']
                text2 = dic['url']
                Printer().printlist_append(['join_lottery', '', 'user', "检测到房间{:^9}的活动抽奖".format(text1)], True)
                Rafflehandler().append2list_activity(text1,text2)
                Statistics().append2pushed_activitylist()
            except:
                pass
            return
        if cmd == 'SYS_MSG':
            if set(self.dic_bulletin) == set(dic):
                Printer().printlist_append(['join_lottery', '系统公告', 'user', dic['msg']])
            else:
                try:
                    TV_url = dic['url']
                    real_roomid = dic['real_roomid']
                    Printer().printlist_append(['join_lottery', '小电视', 'user', "检测到房间{:^9}的小电视抽奖".format(real_roomid)], True)
                    Rafflehandler().append2list_TV(real_roomid)
                    Statistics().append2pushed_TVlist()
                except:
                    print('SYS_MSG出错，请联系开发者', dic)
        if cmd == 'GUARD_MSG':
            print(dic)
            try:
                a = re.compile(r"(?<=在主播 )\S+(?= 的直播间开通了总督)")
                res = a.findall(str(dic))
                name = res[0]
                roomid = await utils.check_up_name(name)
                if roomid == 0:
                    roomid = await utils.check_up_name(name)
                print(roomid)
                response1 = await bilibili().get_giftlist_of_captain(roomid)
                json_response1 = await response1.json()
                print(json_response1)
                num = len(json_response1['data']['guard'])
                if num == 0:
                    await asyncio.sleep(10)
                    response1 = await bilibili().get_giftlist_of_captain(roomid)
                    json_response1 = await response1.json()
                    print(json_response1)
                    num = len(json_response1['data']['guard'])
                for i in range(0, num):
                    id = json_response1['data']['guard'][i]['id']
                    print(id)
                    response2 = await bilibili().get_gift_of_captain(roomid, id)
                    json_response2 = await response2.json()
                    payload = {"roomid": roomid, "id": id, "type": "guard", "csrf_token": ''}
                    print(payload)
                    print("获取到房间 %s 的总督奖励: " %(roomid),json_response2)
            except:
                Printer().printlist_append(['join_lotter', '', 'user', "没领取到奖励,请联系开发者"])
                pass
            return
