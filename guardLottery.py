import traceback
import asyncio

from bilibili import bilibili
from schedule import Schedule
from printer import Printer
import utils
import encrypt
import json
import brotli


class GuardLottery:
    last_guard_room = 0
    had_gotted_guard = []

    async def guard_lottery(self):
        for k in range(1):
            try:
                response = await bilibili().guard_list()
                json_response = response.json()
                break
            except Exception:
                continue
        else:
            Printer().printer("连接舰长服务器失败，尝试从CDN拉取数据", "Error", "red")
            response = await bilibili().guard_list_v2()
            encrypt_content = response.json()['data']['room_info']['description'].replace('b6','').replace('</p>','').replace('<p>','')
            json_response = json.loads(brotli.decompress(encrypt.decrypt(encrypt_content)).decode())
        for i in range(0, len(json_response)):
            GuardId = json_response[i]['Id']
            if GuardId not in GuardLottery.had_gotted_guard and GuardId != 0:
                GuardLottery.had_gotted_guard.append(GuardId)
                OriginRoomId = json_response[i]['RoomId']
                await self.guard_join(OriginRoomId, GuardId)
                await asyncio.sleep(0.2)

    async def guard_join(self, OriginRoomId, GuardId):
        if Schedule().scheduled_sleep:
            Printer().printer(f"定时休眠，跳过房间 {OriginRoomId} 编号 {GuardId} 的上船奖励", "Info", "green")
            return
        if bilibili().black_status:
            Printer().printer(f"黑屋休眠，跳过房间 {OriginRoomId} 编号 {GuardId} 的上船奖励", "Info", "green")
            return
        if not OriginRoomId == GuardLottery.last_guard_room:
            result = await utils.check_room_true(OriginRoomId)
            if True in result:
                Printer().printer(f"检测到房间 {OriginRoomId} 的钓鱼操作", "Warning", "red")
                return
            await bilibili().post_watching_history(OriginRoomId)
            GuardLottery.last_guard_room = OriginRoomId
        # response2 = await bilibili().get_gift_of_captain_v2(OriginRoomId, GuardId)
        # json_response2 = await response2.json(content_type=None)
        # print(json_response2)
        response2 = await bilibili().get_gift_of_captain(OriginRoomId, GuardId)
        json_response2 = await response2.json(content_type=None)
        if json_response2['code'] == 0:
            Printer().printer(f"获取到房间 {OriginRoomId} 编号 {GuardId} 的上船奖励: "
                              f"{json_response2['data']['award_text']}" if json_response2['data']['award_text'] else
                              f"获取到房间 {OriginRoomId} 编号 {GuardId} 的上船奖励: "
                              f"{json_response2['data']['award_name']}X{json_response2['data']['award_num']}",
                              "Lottery", "cyan")
        elif json_response2['code'] == -403 and json_response2['msg'] == "访问被拒绝":
            Printer().printer(f"获取房间 {OriginRoomId} 编号 {GuardId} 的上船奖励: {json_response2['message']}",
                              "Lottery", "cyan")
            print(json_response2)
        elif json_response2['code'] == 400 and json_response2['msg'] == "你已经领取过啦":
            Printer().printer(f"房间 {OriginRoomId} 编号 {GuardId} 的上船奖励已领过",
                              "Info", "green")
        else:
            Printer().printer(f"房间 {OriginRoomId} 编号 {GuardId}  的上船奖励领取出错: {json_response2}",
                              "Error", "red")

    async def run(self):
        while True:
            try:
                await self.guard_lottery()
                await asyncio.sleep(180)
            except Exception:
                await asyncio.sleep(10)
                Printer().printer(traceback.format_exc(), "Error", "red")
