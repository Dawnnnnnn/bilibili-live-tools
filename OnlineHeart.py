from login import Login
import requests
import hashlib
import time
import datetime
import asyncio

class OnlineHeart(Login):

    # 发送pc心跳包 //好像有点bug？？？
    def pcpost_heartbeat(self):
        url = 'http://api.live.bilibili.com/User/userOnlineHeart'
        response = requests.post(url, headers=self.pcheaders)
        #print(response.json())

    # 发送app心跳包
    def apppost_heartbeat(self):
        time = self.CurrentTime()
        temp_params = 'access_key=' + self.access_key + '&actionKey=' + self.actionKey + '&appkey=' + self.appkey + '&build=' + self.build + '&device=' + self.device + '&mobi_app=' + self.mobi_app + '&platform=' + self.platform + '&ts=' + time
        params = temp_params + self.app_secret
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        url = 'https://api.live.bilibili.com/mobile/userOnlineHeart?' + temp_params + '&sign=' + str(hash.hexdigest())
        payload = {'roomid': 23058, 'scale': 'xhdpi'}
        response = requests.post(url, data=payload, headers=self.appheaders)
        #print("app端心跳状态：" + response.json()['message'])

    # 心跳礼物   //测试功能
    def heart_gift(self):
        url = "https://api.live.bilibili.com/gift/v2/live/heart_gift_receive?roomid=3&area_v2_id=34"
        response = requests.get(url, headers=self.pcheaders)
        #print(response.json())

    # 获取当前系统时间的unix时间戳
    def CurrentTime(self):
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime

    async def run(self):
        while 1:
            print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            self.apppost_heartbeat()
            self.pcpost_heartbeat()
            self.heart_gift()
            await asyncio.sleep(300)
