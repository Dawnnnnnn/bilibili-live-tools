# from bilibili import bilibili
from API import API
import asyncio
import random
from struct import *
import json
import datetime
import time
import hashlib
import re
import requests
# from printer import Printer
import sys

def CurrentTime():
    currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
    return currenttime


class bilibiliClient():
    
        
    def __init__(self, printer, bilibili, api):
        self.printer = printer 
        self.bilibili = bilibili
        self.api = api

    async def connectServer(self):
        try:
            reader, writer =await asyncio.open_connection(self.bilibili._ChatHost, self.bilibili._ChatPort)
        except :
            print("# 连接无法建立，请检查本地网络状况")
            return 
        self.bilibili._reader = reader
        self.bilibili._writer = writer
        #print("writer and reader are ready")
        if (await self.SendJoinChannel(self.bilibili.roomid) == True):
            self.bilibili.connected = True
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '连接弹幕服务器成功')
            await self.ReceiveMessageLoop()

    async def HeartbeatLoop(self):
        while self.bilibili.connected == False:
            await asyncio.sleep(0.5)
            
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),'开始心跳')

        while self.bilibili.connected == True:
            await self.SendSocketData(0, 16, self.bilibili._protocolversion, 2, 1, "")
            await asyncio.sleep(30)
            

    async def SendJoinChannel(self, channelId):
        self.bilibili._uid = (int)(100000000000000.0 + 200000000000000.0 * random.random())
        body = '{"roomid":%s,"uid":%s}' % (channelId, self.bilibili._uid)
        await self.SendSocketData(0, 16, self.bilibili._protocolversion, 7, 1, body)
        return True

    async def SendSocketData(self, packetlength, magic, ver, action, param, body):
        bytearr = body.encode('utf-8')
        if packetlength == 0:
            packetlength = len(bytearr) + 16
        sendbytes = pack('!IHHII', packetlength, magic, ver, action, param)
        if len(bytearr) != 0:
            sendbytes = sendbytes + bytearr
        # print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), sendbytes)
        try:
            self.bilibili._writer.write(sendbytes)
        except:
            print(sys.exc_info()[0], sys.exc_info()[1])
            self.bilibili.connected = False
            
        
        await self.bilibili._writer.drain()

    async def ReceiveMessageLoop(self):
        while self.bilibili.connected == True:
            tmp = await self.bilibili._reader.read(4)
            if not tmp:
                print("# 网络连接中断或服务器主动断开，请检查本地网络状况，稍后将尝试重连")
                self.bilibili.connected = False
                break
            expr, = unpack('!I', tmp)
            # print(expr)
            tmp = await self.bilibili._reader.read(2)
            tmp = await self.bilibili._reader.read(2)
            tmp = await self.bilibili._reader.read(4)
            num, = unpack('!I', tmp)
            tmp = await self.bilibili._reader.read(4)
            num2 = expr - 16

            if num2 != 0:
                num -= 1
                if num == 0 or num == 1 or num == 2:
                    tmp = await self.bilibili._reader.read(4)
                    num3, = unpack('!I', tmp)
                    self.bilibili._UserCount = num3
                    continue
                elif num == 3 or num == 4:
                    tmp = await self.bilibili._reader.read(num2)
                    # strbytes, = unpack('!s', tmp)
                    try:
                        messages = tmp.decode('utf-8')
                    except:
                        continue
                    await self.parseDanMu(messages)
                    continue
                elif num == 5 or num == 6 or num == 7:
                    tmp = await self.bilibili._reader.read(num2)
                    continue
                else:
                    if num != 16:
                        tmp = await self.bilibili._reader.read(num2)
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
            # self.printer.print_danmu_msg(dic)
            pass
        if cmd == 'SYS_GIFT':
            try:
                if dic['giftId'] != 39:
                    headers = {
                        'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'accept-encoding': 'gzip, deflate',
                        'Host': 'api.live.bilibili.com',
                        'cookie': self.bilibili.cookie,
                    }
                    text1 = dic['real_roomid']
                    text2 = dic['url']
                    await asyncio.sleep(random.uniform(3, 5))
                    self.api.post_watching_history(self.bilibili.csrf,text1)
                    url = 'http://api.live.bilibili.com/activity/v1/Raffle/check?roomid=' + str(text1)
                    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "检测到房间", str(text1).center(9), "的活动抽奖")
                    response = requests.get(url, headers=headers)
                    checklen = response.json()['data']
                    num = len(checklen)
                    while num != 0:
                        for j in range(0,num):
                            await asyncio.sleep(random.uniform(0.5, 1))
                            resttime = response.json()['data'][j]['time']
                            raffleid = response.json()['data'][j]['raffleId']
                            if raffleid not in self.bilibili.activity_raffleid_list:
                                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "参与了房间", str(text1).center(9), "的活动抽奖")
                                self.bilibili.activity_raffleid_list.append(raffleid)
                                self.bilibili.activity_roomid_list.append(text1)
                                self.bilibili.activity_time_list.append(resttime)
                                headers = {
                                    'Accept': 'application/json, text/plain, */*',
                                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                                    'cookie': self.bilibili.cookie,
                                    'referer': text2
                                }
                                temp_params = 'access_key='+self.bilibili.access_key+'&actionKey='+self.bilibili.actionKey+'&appkey='+self.bilibili.appkey+'&build='+self.bilibili.build+'&device='+self.bilibili.device+'&event_type=flower_rain-' + str(
                                    raffleid) + '&mobi_app='+self.bilibili.mobi_app+'&platform='+self.bilibili.platform+'&room_id=' + str(
                                    text1) + '&ts=' + CurrentTime()
                                params = temp_params + self.bilibili.app_secret
                                hash = hashlib.md5()
                                hash.update(params.encode('utf-8'))
                                true_url = 'http://api.live.bilibili.com/YunYing/roomEvent?' + temp_params + '&sign=' + str(
                                    hash.hexdigest())
                                pc_url = 'http://api.live.bilibili.com/activity/v1/Raffle/join?roomid=' + str(
                                    text1) + '&raffleId=' + str(raffleid)
                                response1 = requests.get(true_url,params=params, headers=headers)
                                pc_response = requests.get(pc_url, headers=headers)
                                try:
                                    print("# 移动端活动抽奖结果:", response1.json()['data']['gift_desc'])
                                except:
                                    pass
                                try:
                                    print("# 网页端活动抽奖状态:", pc_response.json()['message'])
                                except:
                                    pass
                        break
                else:
                    try:
                        roomid = dic['roomid']
                        get_url = "http://api.live.bilibili.com/lottery/v1/Storm/check?roomid="+str(roomid)
                        response = requests.get(get_url, headers=self.bilibili.pcheaders)
                        temp = response.json()
                        check = len(temp['data'])
                        if check != 0 and temp['data']['hasJoin'] != 1:
                            id = temp['data']['id']
                            storm_url = 'http://api.live.bilibili.com/lottery/v1/Storm/join'
                            payload = {"id": id, "color": "16777215", "captcha_token": "", "captcha_phrase": "", "token": "",
                                   "csrf_token": self.bilibili.csrf}
                            response1 = requests.post(storm_url, data=payload, headers=self.bilibili.pcheaders, timeout=2)
                            print(response1.json())
                    except:
                        pass


            except:
                pass
            return

        if cmd == 'SYS_MSG':

            try:
                TV_url = dic['url']
                real_roomid = dic['real_roomid']
                #url = "https://api.live.bilibili.com/AppSmallTV/index?access_key=&actionKey=appkey&appkey=1d8b6e7d45233436&build=5230003&device=android&mobi_app=android&platform=android&roomid=939654&ts=1521734039&sign=4f85e1d3ce0e1a3acd46fcf9ca3cbeed"
                temp_params = 'access_key=' + self.bilibili.access_key + '&actionKey=' + self.bilibili.actionKey + '&appkey=' + self.bilibili.appkey + '&build=' + self.bilibili.build + '&device=' + self.bilibili.device +\
                              '&mobi_app=' + self.bilibili.mobi_app + '&platform=' + self.bilibili.platform + '&roomid=' + str(
                    real_roomid) + '&ts=' + CurrentTime()
                params = temp_params + self.bilibili.app_secret
                hash = hashlib.md5()
                hash.update(params.encode('utf-8'))
                await asyncio.sleep(random.uniform(3, 5))
                self.api.post_watching_history(self.bilibili.csrf,real_roomid)
                check_url = 'https://api.live.bilibili.com/AppSmallTV/index?' + temp_params + '&sign=' + str(hash.hexdigest())
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "监测到房间", str(real_roomid).center(9), "的小电视抽奖")
                # headers = {
                #     'Accept': 'application/json, text/plain, */*',
                #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                #     'Accept-Language': 'zh-CN,zh;q=0.9',
                #     'accept-encoding': 'gzip, deflate',
                #     'Host': 'api.live.bilibili.com',
                #     'cookie': self.cookie,
                # }
                response = requests.get(check_url, headers=self.bilibili.appheaders)
                checklen = response.json()['data']['unjoin']
                num = len(checklen)
                while num != 0:
                    for j in range(0,num):
                        await asyncio.sleep(random.uniform(0.5, 1))
                        resttime = response.json()['data']['unjoin'][j]['dtime']
                        raffleid = response.json()['data']['unjoin'][j]['id']
                        if raffleid not in self.bilibili.TV_raffleid_list:
                            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "参与了房间", str(real_roomid).center(9), "的小电视抽奖")
                            self.bilibili.TV_raffleid_list.append(raffleid)
                            self.bilibili.TV_roomid_list.append(real_roomid)
                            self.bilibili.TV_time_list.append(resttime)
                            #url = "https://api.live.bilibili.com/AppSmallTV/join?access_key=&actionKey=appkey&appkey=1d8b6e7d45233436&build=5230003&device=android&id=41581&mobi_app=android&platform=android&roomid=3566261&ts=1521731305&sign=ae3d61f496c66069bcfd299fe7ce1792"
                            temp_params = 'access_key='+self.bilibili.access_key+'&actionKey='+self.bilibili.actionKey+'&appkey='+self.bilibili.appkey+'&build='+self.bilibili.build+'&device='+self.bilibili.device+'&id=' + str(
                                raffleid) + '&mobi_app='+self.bilibili.mobi_app+'&platform='+self.bilibili.platform+'&roomid=' + str(
                                real_roomid) + '&ts=' + CurrentTime()
                            params = temp_params + self.bilibili.app_secret
                            hash = hashlib.md5()
                            hash.update(params.encode('utf-8'))
                            true_url = 'http://api.live.bilibili.com/AppSmallTV/join?' + temp_params + '&sign=' + str(
                                hash.hexdigest())
                            # headers = {
                            #     'Accept': 'application/json, text/plain, */*',
                            #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                            #     'Accept-Language': 'zh-CN,zh;q=0.9',
                            #     'accept-encoding': 'gzip, deflate',
                            #     'Host': 'api.live.bilibili.com',
                            #     'cookie': self.cookie,
                            #     'referer': TV_url
                            # }
                            # url1 = 'http://api.live.bilibili.com/gift/v2/smalltv/join?roomid=' + str(
                            #     real_roomid) + '&raffleId=' + str(raffleid)
                            # #response1 = requests.get(url1, headers=headers)
                            response2 = requests.get(true_url,headers=self.bilibili.appheaders)
                            print("# 小电视道具抽奖状态:",response2.json()['msg'])
                    break

            except:
                pass
        if cmd == 'GUARD_MSG':
            try:
                a = re.compile(r"(?<=在主播 )\S+(?= 的直播间开通了总督)")
                res = a.findall(dic)
                search_url = "https://search.bilibili.com/api/search?search_type=live&keyword=" + str(res[0])
                response = requests.get(search_url)
                roomid = response.json()['result']['live_user'][0]['roomid']
                temp_params = 'access_key=' + self.bilibili.access_key + '&actionKey=' + self.bilibili.actionKey + '&appkey=' + self.bilibili.appkey + '&build=' + self.bilibili.build + '&device=' + self.bilibili.device +\
                              '&mobi_app=' + self.bilibili.mobi_app + '&platform=' + self.bilibili.platform + '&roomid=' + str(
                    roomid) + '&ts=' + CurrentTime()+"&type=guard"
                params = temp_params + self.bilibili.app_secret
                hash = hashlib.md5()
                hash.update(params.encode('utf-8'))
                true_url = 'https://api.live.bilibili.com/lottery/v1/lottery/check?' + temp_params + '&sign=' + str(
                    hash.hexdigest())
                response1 = requests.get(true_url,headers=self.bilibili.appheaders)
                num = len(response1.json()['data']['guard'])
                for i in range(0,num):
                    ts = CurrentTime()
                    id = response1.json()['data']['guard'][i]['id']
                    temp_params = 'access_key=' + self.bilibili.access_key + '&actionKey=' + self.bilibili.actionKey + '&appkey=' + self.bilibili.appkey + '&build=' + self.bilibili.build + '&device=' + self.bilibili.device + '&id='+str(id)+'&mobi_app=' + self.bilibili.mobi_app + '&platform=' + self.bilibili.platform + '&roomid=' + str(
                        roomid) + '&ts=' + ts + "&type=guard"
                    params = temp_params + self.bilibili.app_secret
                    hash = hashlib.md5()
                    hash.update(params.encode('utf-8'))
                    join_url = "https://api.live.bilibili.com/lottery/v1/lottery/join"
                    payload = {"access_key": self.bilibili.access_key, "actionKey": self.bilibili.actionKey,
                                   "appkey": self.bilibili.appkey, "build": self.bilibili.build, "device": self.bilibili.device,
                                   "id": id, "mobi_app": self.bilibili.mobi_app, "platform": self.bilibili.platform, "roomid":roomid,
                                   "ts": ts, "type": "guard", "sign": hash.hexdigest()}
                    response2 = requests.post(join_url,data=payload,headers=self.bilibili.appheaders)
                    print("# 获取到某个总督的奖励:",response2.json()['data']['message'])

            except:
                print("# 没领取到奖励,请联系开发者")
            return
