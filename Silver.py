from bilibili import bilibili
import datetime
import asyncio
import utils
from printer import Printer


class Silver:

    # 将time_end时间转换成正常时间
    async def DataTime(self):
        datatime = str(datetime.datetime.fromtimestamp(float(await self.time_end())))
        return datatime

    # 领瓜子时判断领取周期的参数
    async def time_start(self):

        response = await bilibili().get_time_about_silver()
        temp = await response.json()
        if temp['code'] == -10017:
            Printer().printer(f"今日宝箱领取完毕", "Info", "green")
        else:
            time_start = temp['data']['time_start']
            return str(time_start)

    # 领瓜子时判断领取周期的参数
    async def time_end(self):
        try:
            response = await bilibili().get_time_about_silver()
            temp = await response.json()
            time_end = temp['data']['time_end']
            return str(time_end)
        except:
            pass

    # 领取银瓜子
    async def GetAward(self):
        try:
            timeend = await self.time_end()
            timestart = await self.time_start()
            response = await bilibili().get_silver(timestart, timeend)
            json_response = await response.json()
            return json_response['code']
        except:
            pass

    async def run(self):
        while 1:
            Printer().printer(f"检查宝箱状态", "Info", "green")
            temp = await self.GetAward()
            if temp == None or temp == -10017:
                await asyncio.sleep(utils.seconds_until_tomorrow() + 300)
            elif temp == 0:
                Printer().printer(f"打开了宝箱", "Info", "green")
                await self.GetAward()
            else:
                Printer().printer(f"继续等待宝箱冷却...", "Info", "green")
                await asyncio.sleep(181)
