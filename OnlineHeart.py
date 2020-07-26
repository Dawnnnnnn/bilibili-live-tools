from bilibili import bilibili
from login import login
import time
import traceback
import datetime
import asyncio
import queue
from statistics import Statistics
from printer import Printer


def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)


class OnlineHeart:

    async def apppost_heartbeat(self):
        return await bilibili().apppost_heartbeat()

    async def pcpost_heartbeat(self):
        response = await bilibili().pcpost_heartbeat()
        return response

    async def heart_gift(self):
        await bilibili().heart_gift()

    async def check_winner(self, i, g, start_time):
        # 开奖5s后检查是否中奖
        await asyncio.sleep(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')) - time.time() + 5)
        response2 = await bilibili().get_winner_info(i, g)
        json_response2 = await response2.json(content_type=None)
        for winner in json_response2["data"]["winnerList"]:
            if winner["uid"] == bilibili().dic_bilibili['uid']:
                Printer().printer(f'实物抽奖中中奖: {winner["giftTitle"]}', "Lottery", "cyan")
                Statistics().add_to_result(winner["giftTitle"], 1)

    async def draw_lottery(self):
        black_list = ["123", "1111", "测试", "測試", "测一测", "ce-shi", "test", "T-E-S-T", "lala", "我是抽奖标题", "压测",  # 已经出现
                      "測一測", "TEST", "Test", "t-e-s-t"]  # 合理猜想
        former_lottery = queue.Queue(maxsize=4)
        [former_lottery.put(True) for _ in range(4)]
        for i in range(590, 800):
            response = await bilibili().get_lotterylist(i)
            json_response = await response.json()
            former_lottery.get()
            former_lottery.put(not json_response['code'])
            if json_response['code'] == 0:
                title = json_response['data']['title']
                check = len(json_response['data']['typeB'])
                for g in range(check):
                    join_end_time = json_response['data']['typeB'][g]['join_end_time']
                    join_start_time = json_response['data']['typeB'][g]['join_start_time']
                    status = json_response['data']['typeB'][g]['status']
                    ts = CurrentTime()
                    if int(join_end_time) > int(ts) > int(join_start_time) and status == 0:
                        jp_list = '&'.join([jp['jp_name'] for jp in json_response['data']['typeB'][g]['list']])
                        for k in black_list:
                            if k in title or k in jp_list:
                                Printer().printer(f"检测到 {i} 号疑似钓鱼类测试抽奖『{title}>>>{jp_list}』" + \
                                                  "，默认不参与，请自行判断抽奖可参与性", "Warning", "red")
                                break
                        else:
                            if bilibili().black_status:
                                Printer().printer(f"黑屋休眠，跳过『{title}>>>{jp_list}』抽奖", "Info", "green")
                                continue
                            response1 = await bilibili().get_gift_of_lottery(i, g)
                            json_response1 = await response1.json(content_type=None)
                            Printer().printer(f"参与『{title}>>>{jp_list}』抽奖回显: {json_response1}", "Lottery", "cyan")
                            start_time = json_response['data']['typeB'][g]["startTime"]
                            asyncio.ensure_future(self.check_winner(i, g, start_time))
            else:
                if not any(former_lottery.queue):  # 检查最近4个活动id是否都-400
                    break
            await asyncio.sleep(0.2)
        del former_lottery

    async def run(self):
        while 1:
            try:
                Printer().printer("心跳", "Info", "green")
                response = await self.pcpost_heartbeat()
                json_response = await response.json(content_type=None)
                if json_response['code'] in [3, -101]:
                    Printer().printer(f"cookie过期,将重新登录", "Error", "red")
                    login().login()
                response1 = await self.apppost_heartbeat()
                json_response1 = await response1.json(content_type=None)
                if json_response1['code'] == -101:
                    # '{"code":-101,"message":"账号未登录","ttl":1}'
                    Printer().printer(f"token过期，尝试刷新", "Error", "red")
                    login().refresh_token()
                await self.heart_gift()
                await self.draw_lottery()
                await asyncio.sleep(300)
            except:
                await asyncio.sleep(10)
                Printer().printer(traceback.format_exc(), "Error", "red")
