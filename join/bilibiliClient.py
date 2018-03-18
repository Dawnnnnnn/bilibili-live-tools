import asyncio
import random
from struct import *
import json
import datetime
import time
import hashlib
import requests

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


def CurrentTime():
    currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
    return currenttime


class bilibiliClient():
    def __init__(self):
        self._CIDInfoUrl = 'http://live.bilibili.com/api/player?id=cid:'
        self._roomId = 0
        self._ChatPort = 2243
        self._protocolversion = 1
        self._reader = 0
        self._writer = 0
        self.connected = False
        self._UserCount = 0
        self._ChatHost = 'livecmt-2.bilibili.com'
        self._roomId = 3108569
        self._roomId = int(self._roomId)

    async def connectServer(self):

        reader, writer = await asyncio.open_connection(self._ChatHost, self._ChatPort)
        self._reader = reader
        self._writer = writer
        if (await self.SendJoinChannel(self._roomId) == True):
            self.connected = True
            print('连接弹幕服务器成功!')
            await self.ReceiveMessageLoop()

    async def HeartbeatLoop(self):
        while self.connected == False:
            await asyncio.sleep(0.5)

        while self.connected == True:
            await self.SendSocketData(0, 16, self._protocolversion, 2, 1, "")
            await asyncio.sleep(30)

    async def SendJoinChannel(self, channelId):
        self._uid = (int)(100000000000000.0 + 200000000000000.0 * random.random())
        body = '{"roomid":%s,"uid":%s}' % (channelId, self._uid)
        await self.SendSocketData(0, 16, self._protocolversion, 7, 1, body)
        return True

    async def SendSocketData(self, packetlength, magic, ver, action, param, body):
        bytearr = body.encode('utf-8')
        if packetlength == 0:
            packetlength = len(bytearr) + 16
        sendbytes = pack('!IHHII', packetlength, magic, ver, action, param)
        if len(bytearr) != 0:
            sendbytes = sendbytes + bytearr
        self._writer.write(sendbytes)
        await self._writer.drain()

    async def ReceiveMessageLoop(self):
        while self.connected == True:
            tmp = await self._reader.read(4)
            expr, = unpack('!I', tmp)
            tmp = await self._reader.read(2)
            tmp = await self._reader.read(2)
            tmp = await self._reader.read(4)
            num, = unpack('!I', tmp)
            tmp = await self._reader.read(4)
            num2 = expr - 16

            if num2 != 0:
                num -= 1
                if num == 0 or num == 1 or num == 2:
                    tmp = await self._reader.read(4)
                    num3, = unpack('!I', tmp)
                    self._UserCount = num3
                    continue
                elif num == 3 or num == 4:
                    tmp = await self._reader.read(num2)
                    # strbytes, = unpack('!s', tmp)
                    try:  # 为什么还会出现 utf-8 decode error??????
                        messages = tmp.decode('utf-8')
                    except:
                        continue
                    self.parseDanMu(messages)
                    continue
                elif num == 5 or num == 6 or num == 7:
                    tmp = await self._reader.read(num2)
                    continue
                else:
                    if num != 16:
                        tmp = await self._reader.read(num2)
                    else:
                        continue

    def parseDanMu(self, messages, headers=headers):

        try:
            dic = json.loads(messages)
        except:  # 有些情况会 jsondecode 失败，未细究，可能平台导致
            return
        cmd = dic['cmd']

        if cmd == 'SYS_GIFT':

            try:
                text1 = dic['real_roomid']
                text2 = dic['url']
                url = 'http://api.live.bilibili.com/activity/v1/Raffle/check?roomid=' + str(text1)
                print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                print("检测到房间", str(text1), "的活动抽奖")
                response = requests.get(url, headers=headers)
                checklen = response.json()['data']
                num = len(checklen)
                if num == 1:
                    raffleid = response.json()['data'][0]['raffleId']
                while num != 0 and num != 1:
                    for j in range(0,num):
                        raffleid = response.json()['data'][j]['raffleId']
                        headers = {
                            'Accept': 'application/json, text/plain, */*',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            'accept-encoding': 'gzip, deflate',
                            'Host': 'api.live.bilibili.com',
                            'cookie': cookies,
                            'referer': text2
                        }
                        temp_params = 'access_key='+access_key+'&actionKey='+actionKey+'&appkey='+appkey+'&build='+build+'&device='+device+'&event_type=flower_rain-' + str(
                            raffleid) + '&mobi_app='+mobi_app+'&platform='+platform+'&room_id=' + str(
                            text1) + '&ts=' + CurrentTime()
                        params = temp_params + '560c52ccd288fed045859ed18bffd973'
                        hash = hashlib.md5()
                        hash.update(params.encode('utf-8'))
                        true_url = 'http://api.live.bilibili.com/YunYing/roomEvent?' + temp_params + '&sign=' + str(
                            hash.hexdigest())
                        pc_url = 'http://api.live.bilibili.com/activity/v1/Raffle/join?roomid=' + str(
                            text1) + '&raffleId=' + str(raffleid)
                        params ={'access_key' : access_key,
                            'actionKey' : actionKey ,
                            'appkey' : appkey ,
                            'build' :build ,
                            'device':device,
                            'event_type':'flower_rain-%s' %(str(raffleid)) ,
                            'mobi_app': mobi_app ,
                            'platform' :platform ,
                            'room_id' : str(text1) ,
                            'ts' : CurrentTime(),
                            'sign':hash.hexdigest(),#md5加密后数据
                        }
                        true_url = 'http://api.live.bilibili.com/YunYing/roomEvent'#加入相关的数据并且加入sign
                        response1 = requests.get(true_url,params=params, headers=headers)
                        pc_response = requests.get(pc_url, headers=headers)
                        try:
                            print("app端活动抽奖状态：", response1.json()['message'])
                            print("app端活动抽奖结果：", response1.json()['data']['gift_desc'])
                        except:
                            pass
                        try:
                            print("pc端活动抽奖状态：", pc_response.json()['message'])
                        except:
                            pass
                    break
                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'accept-encoding': 'gzip, deflate',
                    'Host': 'api.live.bilibili.com',
                    'cookie': cookies,
                    'referer': text2
                }
                temp_params = 'access_key=' + access_key + '&actionKey=' + actionKey + '&appkey=' + appkey + '&build=' + build + '&device=' + device + '&event_type=flower_rain-' + str(
                    raffleid) + '&mobi_app=' + mobi_app + '&platform=' + platform + '&room_id=' + str(
                    text1) + '&ts=' + CurrentTime()
                params = temp_params + '560c52ccd288fed045859ed18bffd973'
                hash = hashlib.md5()
                hash.update(params.encode('utf-8'))
                true_url = 'http://api.live.bilibili.com/YunYing/roomEvent?' + temp_params + '&sign=' + str(
                    hash.hexdigest())
                pc_url = 'http://api.live.bilibili.com/activity/v1/Raffle/join?roomid=' + str(
                    text1) + '&raffleId=' + str(raffleid)
                response1 = requests.get(true_url, headers=headers)
                pc_response = requests.get(pc_url, headers=headers)
                try:
                    print("app端活动抽奖状态：", response1.json()['message'])
                    print("app端活动抽奖结果：", response1.json()['data']['gift_desc'])
                except:
                    pass
                try:
                    print("pc端活动抽奖状态：", pc_response.json()['message'])
                except:
                    pass



            except:
                pass
            return

        if cmd == 'SYS_MSG':

            try:
                TV_url = dic['url']
                real_roomid = dic['real_roomid']
                url = 'http://api.live.bilibili.com/gift/v2/smalltv/check?roomid=' + str(real_roomid)
                print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                print("检测到房间", str(real_roomid), "的小电视抽奖")
                response = requests.get(url, headers=headers)
                checklen = response.json()['data']
                num = len(checklen)
                if num == 1:
                    raffleid = response.json()['data'][0]['raffleId']
                while num != 0 and num != 1:
                    for j in range(0,num):
                        raffleid = response.json()['data'][j]['raffleId']
                        headers = {
                            'Accept': 'application/json, text/plain, */*',
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            'accept-encoding': 'gzip, deflate',
                            'Host': 'api.live.bilibili.com',
                            'cookie': cookies,
                            'referer': TV_url
                        }
                        url1 = 'http://api.live.bilibili.com/gift/v2/smalltv/join?roomid=' + str(
                            real_roomid) + '&raffleId=' + str(raffleid)
                        response1 = requests.get(url1, headers=headers)
                        print(response1.json()['msg'])
                    break
                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'accept-encoding': 'gzip, deflate',
                    'Host': 'api.live.bilibili.com',
                    'cookie': cookies,
                    'referer': TV_url
                }
                url1 = 'http://api.live.bilibili.com/gift/v2/smalltv/join?roomid=' + str(
                    real_roomid) + '&raffleId=' + str(raffleid)
                response1 = requests.get(url1, headers=headers)
                print("小电视抽奖状态:",response1.json()['msg'])


            except:
                pass
            return
