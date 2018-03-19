from login import Login
import hashlib
import requests
import datetime
import time
import asyncio

class Silver(Login):
    # 获取当前系统时间的unix时间戳
    def CurrentTime(self):
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime

    # 将time_end时间转换成正常时间
    def DataTime(self):
        datatime = str(datetime.datetime.fromtimestamp(float(self.time_end())))
        return datatime

    # 领瓜子时判断领取周期的参数
    def time_start(self):
        time = self.CurrentTime()
        temp_params = 'access_key=' + self.access_key + '&actionKey=' + self.actionKey + '&appkey=' + self.appkey + '&build=' + self.build + '&device=' + self.device + '&mobi_app=' + self.mobi_app + '&platform=' + self.platform + '&ts=' + time
        params = temp_params + self.app_secret
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        GetTask_url = 'https://api.live.bilibili.com/mobile/freeSilverCurrentTask?' + temp_params + '&sign=' + str(
            hash.hexdigest())
        response = self.ses.get(GetTask_url)
        temp = response.json()
        # print (temp['code'])    #宝箱领完返回的code为-10017
        if temp['code'] == -10017:
            print("今天的瓜子领完了")
        else:
            time_start = temp['data']['time_start']
            return str(time_start)

    # 领瓜子时判断领取周期的参数
    def time_end(self):
        try:
            time = self.CurrentTime()
            temp_params = 'access_key=' + self.access_key + '&actionKey=' + self.actionKey + '&appkey=' + self.appkey + '&build=' + self.build + '&device=' + self.device + '&mobi_app=' + self.mobi_app + '&platform=' + self.platform + '&ts=' + time
            params = temp_params + self.app_secret
            hash = hashlib.md5()
            hash.update(params.encode('utf-8'))
            GetTask_url = 'https://api.live.bilibili.com/mobile/freeSilverCurrentTask?' + temp_params + '&sign=' + str(
                hash.hexdigest())
            response = requests.get(GetTask_url, headers=self.appheaders)
            temp = response.json()
            time_end = temp['data']['time_end']
            return str(time_end)
        except:
            pass

    # 领取银瓜子
    def GetAward(self):
        try:
            time = self.CurrentTime()
            timeend = self.time_end()
            timestart = self.time_start()
            temp_params = 'access_key=' + self.access_key + '&actionKey=' + self.actionKey + '&appkey=' + self.appkey + '&build=' + self.build + '&device=' + self.device + '&mobi_app=' + self.mobi_app + '&platform=' + self.platform + '&time_end=' + timeend + '&time_start=' + timestart + '&ts=' + time
            params = temp_params + self.app_secret
            hash = hashlib.md5()
            hash.update(params.encode('utf-8'))
            url = 'https://api.live.bilibili.com/mobile/freeSilverAward?' + temp_params + '&sign=' + str(
                hash.hexdigest())
            response = requests.get(url, headers=self.appheaders)
            print(response.json())
            return response.json()['code']
        except:
            pass

    async def run(self):
        while 1:
            temp = self.GetAward()
            if temp == None or temp == -10017:
                print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                print("半小时后检测一次是否到第二天了")
                await asyncio.sleep(1800)
            elif temp == 0:
                print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                self.GetAward()
            else:
                print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                await asyncio.sleep(181)
