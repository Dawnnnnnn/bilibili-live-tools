from bilibili import bilibili
from login import login
import utils
import time
import traceback
import datetime
import asyncio
from printer import Printer


had_gotted_guard = []

def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)


class OnlineHeart:
    last_guard_room = 0

    async def apppost_heartbeat(self):
        await bilibili().apppost_heartbeat()

    async def pcpost_heartbeat(self):
        response = await bilibili().pcpost_heartbeat()
        return response

    async def heart_gift(self):
        await bilibili().heart_gift()

    async def guard_lottery(self):
        for k in range(3):
            try:
                response = await bilibili().guard_list()
                json_response = response.json()
                break
            except Exception:
                continue
        else:
            Printer().printer("连接舰长服务器失败", "Error", "red")
            return
        for i in range(0, len(json_response)):
            if json_response[i]['Status']:
                GuardId = json_response[i]['GuardId']
                if GuardId not in had_gotted_guard and GuardId != 0:
                    had_gotted_guard.append(GuardId)
                    OriginRoomId = json_response[i]['OriginRoomId']
                    if not OriginRoomId == OnlineHeart.last_guard_room:
                        result = await utils.check_room_true(OriginRoomId)
                        if True in result:
                            Printer().printer(f"检测到房间 {OriginRoomId} 的钓鱼操作", "Warning", "red")
                            continue
                        await bilibili().post_watching_history(OriginRoomId)
                        OnlineHeart.last_guard_room = OriginRoomId
                    response2 = await bilibili().get_gift_of_captain(OriginRoomId, GuardId)
                    json_response2 = await response2.json(content_type=None)
                    if json_response2['code'] == 0:
                        Printer().printer(f"获取到房间 {OriginRoomId} 编号 {GuardId} 的上船亲密度: {json_response2['data']['message']}",
                                          "Lottery", "cyan")
                    elif json_response2['code'] == 400 and json_response2['msg'] == "你已经领取过啦":
                        Printer().printer(
                            f"房间 {OriginRoomId} 编号 {GuardId} 的上船亲密度已领过",
                            "Info", "green")
                    elif json_response2['code'] == 400 and json_response2['msg'] == "访问被拒绝":
                        Printer().printer(f"获取房间 {OriginRoomId} 编号 {GuardId} 的上船亲密度: {json_response2['message']}",
                                          "Lottery", "cyan")
                        print(json_response2)
                    else:
                        Printer().printer(
                            f"房间 {OriginRoomId} 编号 {GuardId}  的上船亲密度领取出错: {json_response2}",
                            "Error", "red")
            else:
                pass


    async def draw_lottery(self):
        black_list = ["123", "1111", "测试", "測試", "测一测", "ce-shi", "test", "T-E-S-T", "lala",  # 已经出现
                      "測一測", "TEST", "Test", "t-e-s-t"]  # 合理猜想
        last_lottery = 0
        for i in range(295, 400):
            response = await bilibili().get_lotterylist(i)
            json_response = await response.json()
            if json_response['code'] == 0:
                last_lottery = 0
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
                                                   "，默认不参与，请自行判断抽奖可参与性","Warning","red")
                                break
                        else:
                            response1 = await bilibili().get_gift_of_lottery(i, g)
                            json_response1 = await response1.json(content_type=None)
                            Printer().printer(f"参与『{title}>>>{jp_list}』抽奖回显: {json_response1}", "Lottery", "cyan")
            else:
                if not last_lottery == 0:  # 因为有中途暂时空一个-400的情况
                    break
                else:
                    last_lottery = json_response['code']

    async def run(self):
        while 1:
            try:
                Printer().printer("心跳", "Info","green")
                response = await self.pcpost_heartbeat()
                json_response = await response.json(content_type=None)
                if json_response['code'] == 3:
                    Printer().printer(f"cookie过期,将重新登录","Error","red")
                    login().login()
                await self.apppost_heartbeat()
                await self.heart_gift()
                await self.guard_lottery()
                await self.draw_lottery()
                await asyncio.sleep(300)
            except:
                await asyncio.sleep(10)
                Printer().printer(traceback.format_exc(), "Error", "red")
