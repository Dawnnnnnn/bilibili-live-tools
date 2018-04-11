from bilibili import bilibili
import hashlib
import requests
import datetime
import time
import asyncio
import utils
class Silver():

    # 将time_end时间转换成正常时间
    def DataTime(self):
        datatime = str(datetime.datetime.fromtimestamp(float(self.time_end())))
        return datatime

    # 领瓜子时判断领取周期的参数
    def time_start(self):

        response = bilibili().get_time_about_silver()
        temp = response.json()
        # print (temp['code'])    #宝箱领完返回的code为-10017
        if temp['code'] == -10017:
            print("# 今日宝箱领取完毕")            
        else:
            time_start = temp['data']['time_start']
            return str(time_start)

    # 领瓜子时判断领取周期的参数
    def time_end(self):
        try:
            response = bilibili().get_time_about_silver()
            temp = response.json()
            time_end = temp['data']['time_end']
            return str(time_end)
        except:
            pass

    # 领取银瓜子
    def GetAward(self):
        try:
            timeend = self.time_end()
            timestart = self.time_start()
            response = bilibili().get_silver(timestart, timeend)
            #print(response.json())
            return response.json()['code']
        except:
            pass

    async def run(self):
        while 1:
            print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "检查宝箱状态")
            temp = self.GetAward()
            if temp == None or temp == -10017:
                await asyncio.sleep(utils.seconds_until_tomorrow() + 300)
            elif temp == 0:
                print("# 打开了宝箱")
                self.GetAward()
            else:
                print("# 继续等待宝箱冷却...")
                await asyncio.sleep(181)
