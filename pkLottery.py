import traceback
import asyncio

from bilibili import bilibili
from printer import Printer
import utils


class PKLottery:
    last_pk_room = 0
    had_gotten_pk = []

    async def pk_lottery(self):
        for _ in range(3):
            try:
                response = await bilibili().pk_list()
                json_response = response.json()
                # print(json_response)
                break
            except Exception:
                continue
        else:
            Printer().printer("连接大乱斗服务器失败", "Error", "red")
            return
        for i in range(0, len(json_response)):
            PKId = json_response[i]['Id']
            if PKId not in PKLottery.had_gotten_pk and PKId != 0:
                PKLottery.had_gotten_pk.append(PKId)
                OriginRoomId = json_response[i]['RoomId']
                if not OriginRoomId == PKLottery.last_pk_room:
                    result = await utils.check_room_true(OriginRoomId)
                    if True in result:
                        Printer().printer(f"检测到房间 {OriginRoomId} 的钓鱼操作", "Warning", "red")
                        continue
                    await bilibili().post_watching_history(OriginRoomId)
                    PKLottery.last_pk_room = OriginRoomId
                response2 = await bilibili().get_gift_of_pk(OriginRoomId, PKId)
                json_response2 = await response2.json(content_type=None)
                # print(json_response2)
                # {'code': 0, 'message': '0', 'ttl': 1, 'data': {'id': 343560, 'gift_type': 0, 'award_id': '1', 'award_text': '辣条X1', 'award_image': 'https://i0.hdslb.com/bfs/live/da6656add2b14a93ed9eb55de55d0fd19f0fc7f6.png', 'award_num': 0, 'title': '大乱斗获胜抽奖'}}
                # {'code': -1, 'message': '抽奖已结束', 'ttl': 1}
                # {'code': -2, 'message': '您已参加过抽奖', 'ttl': 1}
                # {"code":-403,"data":null,"message":"访问被拒绝","msg":"访问被拒绝"}
                if json_response2['code'] == 0:
                    Printer().printer(f"参与房间 {OriginRoomId} 编号 {PKId} 的大乱斗获胜抽奖: {json_response2['data']['award_text']}",
                                      "Lottery", "cyan")
                elif json_response2['code'] == -2 and json_response2['message'] == "您已参加过抽奖":
                    Printer().printer(
                        f"房间 {OriginRoomId} 编号 {PKId} 的大乱斗获胜抽奖已参与过",
                        "Info", "green")
                elif json_response2['code'] == -403 and json_response2['message'] == "访问被拒绝":
                    Printer().printer(f"参与房间 {OriginRoomId} 编号 {PKId} 的大乱斗获胜抽奖: {json_response2['message']}",
                                      "Lottery", "cyan")
                    print(json_response2)
                else:
                    Printer().printer(
                        f"房间 {OriginRoomId} 编号 {PKId} 的大乱斗获胜抽奖参与出错: {json_response2}",
                        "Error", "red")


    async def run(self):
        while True:
            try:
                await self.pk_lottery()
                await asyncio.sleep(30)
            except Exception:
                await asyncio.sleep(10)
                Printer().printer(traceback.format_exc(), "Error", "red")
