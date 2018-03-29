from bilibili import bilibili
import requests
import hashlib
import time
import datetime
import asyncio


class OnlineHeart():

    def __init__(self, bilibili):
        self.bilibili = bilibili
    # 发送pc心跳包 //好像有点bug？？？
    def pcpost_heartbeat(self):
        url = 'http://api.live.bilibili.com/User/userOnlineHeart'
        response = requests.post(url, headers=self.bilibili.pcheaders)
        #print(response.json())

    # 发送app心跳包
    def apppost_heartbeat(self):
        time = self.CurrentTime()
        temp_params = 'access_key=' + self.bilibili.access_key + '&actionKey=' + self.bilibili.actionKey + '&appkey=' + self.bilibili.appkey + '&build=' + self.bilibili.build + '&device=' + self.bilibili.device + '&mobi_app=' + self.bilibili.mobi_app + '&platform=' + self.bilibili.platform + '&ts=' + time
        params = temp_params + self.bilibili.app_secret
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        url = 'https://api.live.bilibili.com/mobile/userOnlineHeart?' + temp_params + '&sign=' + str(hash.hexdigest())
        payload = {'roomid': 23058, 'scale': 'xhdpi'}
        response = requests.post(url, data=payload, headers=self.bilibili.appheaders)
        #print("app端心跳状态：" + response.json()['message'])

    # 心跳礼物   //测试功能
    def heart_gift(self):
        url = "https://api.live.bilibili.com/gift/v2/live/heart_gift_receive?roomid=3&area_v2_id=34"
        response = requests.get(url, headers=self.bilibili.pcheaders)
        #print(response.json())

    # 获取当前系统时间的unix时间戳
    def CurrentTime(self):
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime

    # 因为休眠时间差不多,所以放到这里,此为实验性功能
    def draw_lottery(self):
        for i in range(60,80):
            url = "https://api.live.bilibili.com/lottery/v1/box/getStatus?aid="+str(i)
            response = requests.get(url,headers=self.bilibili.pcheaders)
            res = response.json()
            #print(res)
            if res['code'] == 0:
                temp = response.json()['data']['title']
                if "测试" in temp:
                    print("检测到疑似钓鱼类测试抽奖，默认不参与，请自行判断抽奖可参与性")
                    print(url)
                else:
                    check = len(response.json()['data']['typeB'])
                    for g in range(0, check):
                        join_end_time = response.json()['data']['typeB'][g]['join_end_time']
                        join_start_time = response.json()['data']['typeB'][g]['join_start_time']
                        ts = self.CurrentTime()
                        if int(join_end_time) > int(ts) > int(join_start_time):
                            url1 = 'https://api.live.bilibili.com/lottery/v1/box/draw?aid=' + str(i) + '&number=' + str(
                                g + 1)
                            response1 = requests.get(url1, headers=self.bilibili.pcheaders)
                            print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                            print("参与抽奖回显：",response1.json())
                        else:
                            break
            else:
                break

    async def run(self):
        while 1:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "心跳")
            self.apppost_heartbeat()
            self.pcpost_heartbeat()
            self.heart_gift()
            self.draw_lottery()
            await asyncio.sleep(300)


