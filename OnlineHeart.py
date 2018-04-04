from bilibili import bilibili
import requests
import hashlib
import time
import datetime
import asyncio

def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)


class OnlineHeart():


    def apppost_heartbeat(self):
        bilibili().apppost_heartbeat()

    def pcpost_heartbeat(self):
        bilibili().pcpost_heartbeat()

    def heart_gift(self):
        bilibili().heart_gift()


    # 因为休眠时间差不多,所以放到这里,此为实验性功能
    def draw_lottery(self):
        for i in range(60,80):
            response  = bilibili().get_lotterylist(i)
            res = response.json()
            if res['code'] == 0:
                temp = response.json()['data']['title']
                if "测试" in temp:
                    print("检测到疑似钓鱼类测试抽奖，默认不参与，请自行判断抽奖可参与性")
                    # print(url)
                else:
                    check = len(response.json()['data']['typeB'])
                    for g in range(0, check):
                        join_end_time = response.json()['data']['typeB'][g]['join_end_time']
                        join_start_time = response.json()['data']['typeB'][g]['join_start_time']
                        ts = CurrentTime()
                        if int(join_end_time) > int(ts) > int(join_start_time):
                            response1 = bilibili().get_gift_of_lottery(i, g)
                            print("当前时间:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                            print("参与实物抽奖回显：",response1.json())
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
            # print('OnlineHeart is over')
            await asyncio.sleep(300)


