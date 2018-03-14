import asyncio
import random
from struct import *
import json
import datetime
import time
import hashlib
import requests
import socket

access_key = ''    # 示例：5dd42a8149a8799b809b700298483f5e
cookies = ''
# 底下这些都是固定值，一时不会变
appkey = '27eb53fc9058f8c3'
actionKey = 'appkey'
build = '6570'
device = 'phone'
mobi_app = 'iphone'
platform = 'ios'

"/YunYing/roomEvent?access_key=775b10755d81313d249d67dfa096ac6b&actionKey=appkey&appkey=27eb53fc9058f8c3&build=6570&device=phone&event_type=flower_rain-17266&mobi_app=iphone&platform=ios&room_id=479592&sign=8c15e70d03fb43b1fe04ec6230dbbe5d&ts=1521008511"
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
        self._roomId = 3108596
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
        print(dic)
        if cmd == 'SYS_GIFT':
            start = time.time()
            try:
                text1 = dic['real_roomid']
                host = "api.live.bilibili.com"
                tempurl = '/activity/v1/Raffle/check?roomid='+str(text1)
                se = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                se.connect((host, 80))
                se.send(("GET " + tempurl + " HTTP/1.1\r\n").encode())
                se.send(("Accept:text/html,application/xhtml+xml,*/*;q=0.8\r\n").encode())
                se.send(("Accept-Language:zh-CN\r\n").encode())
                se.send(("Connection:keep-alive\r\n").encode())
                se.send(("Host:" + host + "\r\n").encode())
                se.send(("Display-ID:146771405-1521008435\r\n").encode())
                se.send(("User-Agent: bili-universal/6570 CFNetwork/894 Darwin/17.4.0\r\n").encode())
                se.send(("Accept-encoding: gzip\r\n").encode())
                se.send(("Buvid:000ce0b9b9b4e342ad4f421bcae5e0ce\n\n").encode())
                temp = (se.recv(1024))
                temp = temp.decode(encoding="utf-8", errors="strict")
                a = temp.find("{")
                data = temp[a:-1]+"}"
                data = eval(data)
                raffleid = data['data'][0]['raffleId']

                ts = CurrentTime()
                temp_params = 'access_key='+access_key+'&actionKey='+actionKey+'&appkey='+appkey+'&build='+build+'&device='+device+'&event_type=flower_rain-' + str(
                            raffleid) + '&mobi_app='+mobi_app+'&platform='+platform+'&room_id=' + str(
                            text1) + '&ts=' + ts
                params = temp_params + '560c52ccd288fed045859ed18bffd973'
                hash = hashlib.md5()
                hash.update(params.encode('utf-8'))


                host = "api.live.bilibili.com"
                se = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                se.connect((host, 80))
                se.send(("GET " + "/YunYing/roomEvent?" + temp_params + "&sign=" + hash.hexdigest()+ " HTTP/1.1\r\n").encode())
                se.send(("Accept:text/html,application/xhtml+xml,*/*;q=0.8\r\n").encode())
                se.send(("Accept-Language:zh-CN\r\n").encode())
                se.send(("Connection:keep-alive\r\n").encode())
                se.send(("Host:" + host + "\r\n").encode())
                se.send(("Display-ID:146771405-1521008435\r\n").encode())
                se.send(("User-Agent: bili-universal/6570 CFNetwork/894 Darwin/17.4.0\r\n").encode())
                se.send(("Accept-encoding: gzip\r\n").encode())
                se.send(("Buvid:000ce0b9b9b4e342ad4f421bcae5e0ce\n\n").encode())
                se.send(("Cookie:LIVE_BUVID=AUTO6315210085073123; finger=72e500cb; sid=m4iv1ypb").encode())
                end = time.time()
                print(end-start)
                temp = (se.recv(1024).decode("utf-8"))
                print(temp)
                with open("log.txt","a",encoding="utf-8") as f:
                    f.write(temp)
                '''
                headers = {
                            'Accept': 'application/json, text/plain, */*',
                            'User-Agent': 'bili-universal/6570 CFNetwork/894 Darwin/17.4.0',
                            'Accept-Language': 'zh-CN,zh;q=0.9',
                            'accept-encoding': 'gzip',
                            'Host': 'api.live.bilibili.com',
                            "Buvid": "000ce0b9b9b4e342ad4f421bcae5e0ce",
                            "Display-ID": "146771405-1521008435",
                            'cookie': cookies,
                    }
                '''


            except:
                pass

            return
