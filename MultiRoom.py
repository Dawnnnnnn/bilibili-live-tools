import random
import asyncio
from bilibili import bilibili
from printer import Printer


class MultiRoom:

    async def asmr_area(self):
        while True:
            try:
                url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
                response = await bilibili().bili_section_get(url)
                json_response = await response.json(content_type=None)
                checklen = len(json_response['data'])
                asmr_area_room = json_response['data'][random.randint(0, checklen-1)]['roomid']
                state = await bilibili().check_room_state(asmr_area_room)
                if state == 1:
                    return [asmr_area_room, "娱乐分区"]
                else:
                    Printer().printer("检测到房间未开播，立即尝试重新获取", "Error", "red")
            except Exception as e:
                Printer().printer(f"获取 [娱乐分区] 房间列表失败，5s后进行下次尝试 {repr(e)}", "Error", "red")
                await asyncio.sleep(5)

    async def game_area(self):
        while True:
            try:
                url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=2&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
                response = await bilibili().bili_section_get(url)
                json_response = await response.json(content_type=None)
                checklen = len(json_response['data'])
                game_area_room = json_response['data'][random.randint(0, checklen-1)]['roomid']
                state = await bilibili().check_room_state(game_area_room)
                if state == 1:
                    return [game_area_room, "游戏分区"]
                else:
                    Printer().printer("检测到房间未开播，立即尝试重新获取", "Error", "red")
            except Exception as e:
                Printer().printer(f"获取 [游戏分区] 房间列表失败，5s后进行下次尝试 {repr(e)}", "Error", "red")
                await asyncio.sleep(5)

    async def mobile_area(self):
        while True:
            try:
                url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=3&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
                response = await bilibili().bili_section_get(url)
                json_response = await response.json(content_type=None)
                checklen = len(json_response['data'])
                mobile_area_room = json_response['data'][random.randint(0, checklen-1)]['roomid']
                state = await bilibili().check_room_state(mobile_area_room)
                if state == 1:
                    return [mobile_area_room, "手游分区"]
                else:
                    Printer().printer("检测到房间未开播，立即尝试重新获取", "Error", "red")
            except Exception as e:
                Printer().printer(f"获取 [手游分区] 房间列表失败，5s后进行下次尝试 {repr(e)}", "Error", "red")
                await asyncio.sleep(5)

    async def draw_area(self):
        while True:
            try:
                url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=4&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
                response = await bilibili().bili_section_get(url)
                json_response = await response.json(content_type=None)
                checklen = len(json_response['data'])
                draw_area_room = json_response['data'][random.randint(0, checklen-1)]['roomid']
                state = await bilibili().check_room_state(draw_area_room)
                if state == 1:
                    return [draw_area_room, "绘画分区"]
                else:
                    Printer().printer(f"检测到房间未开播，立即尝试重新获取", "Error", "red")
            except Exception as e:
                Printer().printer(f"获取 [绘画分区] 房间列表失败，5s后进行下次尝试 {repr(e)}", "Error", "red")
                await asyncio.sleep(5)

    async def radio_area(self):
        while True:
            try:
                url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=5&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
                response = await bilibili().bili_section_get(url)
                json_response = await response.json(content_type=None)
                checklen = len(json_response['data'])
                radio_area_room = json_response['data'][random.randint(0, checklen-1)]['roomid']
                state = await bilibili().check_room_state(radio_area_room)
                if state == 1:
                    return [radio_area_room, "电台分区"]
                else:
                    Printer().printer(f"检测到房间未开播，立即尝试重新获取", "Error", "red")
            except Exception as e:
                Printer().printer(f"获取 [电台分区] 房间列表失败，5s后进行下次尝试 {repr(e)}", "Error", "red")
                await asyncio.sleep(5)

    async def check_state(self, area, roomid=None):
        if roomid is not None:
            response = await bilibili().check_room_info(roomid)
            json_response = await response.json()
            live_status = json_response['data']['live_status']
            curr_area_name = json_response['data']['parent_area_name']
            if live_status == 1 and curr_area_name in area:
                Printer().printer(f'[{area}] 房间 {roomid} 直播状态正常', "Info", "green")
                return [roomid, area]
            elif live_status != 1:
                Printer().printer(f"[{area}] 房间 {roomid} 已未直播！将切换监听房间", "Info", "green")
            else:
                # print(type(live_status), live_status, curr_area_name)
                Printer().printer(f"[{area}] 房间 {roomid} 已切换分区[{curr_area_name}]！将切换监听房间", "Info", "green")
        if area == "娱乐分区":
            asmr = await self.asmr_area()
            return asmr
        elif area == "游戏分区":
            game = await self.game_area()
            return game
        elif area == "手游分区":
            mobile = await self.mobile_area()
            return mobile
        elif area == "绘画分区":
            draw = await self.draw_area()
            return draw
        elif area == "电台分区":
            radio = await self.radio_area()
            return radio

    async def get_all(self):
        asmr = await self.asmr_area()
        game = await self.game_area()
        mobile = await self.mobile_area()
        draw = await self.draw_area()
        radio = await self.radio_area()
        return [asmr, game, mobile, draw, radio]
