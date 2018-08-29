from bilibili import bilibili
from login import login
import time
import traceback
import datetime
import asyncio
from printer import Printer


def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)


class OnlineHeart():

    async def apppost_heartbeat(self):
        await bilibili().apppost_heartbeat()

    async def pcpost_heartbeat(self):
        response = await bilibili().pcpost_heartbeat()
        return response

    async def heart_gift(self):
        await bilibili().heart_gift()

    async def guard_lottery(self):
        response = await bilibili().guard_list()
        json_response = response.json()
        for i in range(0,len(json_response)):
            if json_response[i]['Status'] == True:
                GuardId = json_response[i]['GuardId']
                OriginRoomId = json_response[i]['OriginRoomId']
                response2 = await bilibili().get_gift_of_captain(OriginRoomId, GuardId)
                json_response2 = await response2.json()
                if json_response2['code'] == 0:
                    Printer().printlist_append(['join_lottery', '', 'user', f"获取到房间{OriginRoomId},编号{GuardId}的上船亲密度:{json_response2['data']['message']}"], True)
                elif json_response2['code'] == 400:
                    Printer().printlist_append(['join_lottery', '', 'user',
                                                f"房间{OriginRoomId},编号{GuardId}的上船亲密度已领过"],
                                               True)
                else:
                    Printer().printlist_append(['join_lottery', '', 'user',
                                                f"房间{OriginRoomId},编号{GuardId}的上船亲密度领取出错,{json_response2}"],
                                               True)
            else:
                pass

    # 因为休眠时间差不多,所以放到这里,此为实验性功能
    async def draw_lottery(self):
        black_list = ["测试", "test"]
        for i in range(169, 200):
            response = await bilibili().get_lotterylist(i)
            json_response = await response.json()
            if json_response['code'] == 0:
                temp = json_response['data']['title']
                for k in black_list:
                    if k in temp:
                        print("检测到疑似钓鱼类测试抽奖，默认不参与，请自行判断抽奖可参与性")
                else:
                    check = len(json_response['data']['typeB'])
                    for g in range(0, check):
                        join_end_time = json_response['data']['typeB'][g]['join_end_time']
                        join_start_time = json_response['data']['typeB'][g]['join_start_time']
                        ts = CurrentTime()
                        if int(join_end_time) > int(ts) > int(join_start_time):
                            response1 = await bilibili().get_gift_of_lottery(i, g)
                            json_response1 = await response1.json()
                            print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                            print("参与实物抽奖回显：", json_response1)
                        else:
                            pass
            else:
                break

    async def run(self):
        while 1:
            try:
                Printer().printlist_append(['join_lottery', '', 'user', "心跳"], True)
                response = await self.pcpost_heartbeat()
                json_response = await response.json()
                if json_response['code'] == 3:
                    Printer().printlist_append(['join_lottery', '', 'user', "cookie过期,将重新登录"], True)
                    login().login()
                await self.apppost_heartbeat()
                await self.heart_gift()
                await self.guard_lottery()
                await self.draw_lottery()
                await asyncio.sleep(300)
            except:
                await asyncio.sleep(10)
                traceback.print_exc()

