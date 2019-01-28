import random
import asyncio
from bilibili import bilibili
from printer import Printer


async def area2room(area_id):
    while True:
        try:
            url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=" + \
                  str(area_id) + "&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
            response = await bilibili().bili_section_get(url)
            json_response = await response.json(content_type=None)
            checklen = len(json_response['data'])
            rand_num = random.randint(0, checklen-1)
            new_area_id = json_response['data'][rand_num]['parent_id']
            if not new_area_id == int(area_id):
                continue
            area_room = json_response['data'][rand_num]['roomid']
            state = await bilibili().check_room_state(area_room)
            if state == 1:
                new_area = str(new_area_id) + json_response['data'][rand_num]['parent_name']
                return [area_room, new_area]
            else:
                Printer().printer("检测到获取房间未开播，立即尝试重新获取", "Error", "red")
        except Exception as e:
            Printer().printer(f"获取房间列表失败，5s后进行下次尝试 {repr(e)}", "Error", "red")
            await asyncio.sleep(5)


async def check_state(area, roomid=None):
    if roomid is not None:
        response = await bilibili().check_room_info(roomid)
        json_response = await response.json(content_type=None)
        live_status = json_response['data']['live_status']
        curr_area_name = json_response['data']['parent_area_name']
        if live_status == 1 and curr_area_name in area:
            Printer().printer(f'[{area}分区] 房间 {roomid} 直播状态正常', "Info", "green")
            return [roomid, area]
        elif live_status != 1:
            Printer().printer(f"[{area}分区] 房间 {roomid} 已未直播！将切换监听房间", "Info", "green")
        else:
            # print(type(live_status), live_status, curr_area_name)
            Printer().printer(f"[{area}分区] 房间 {roomid} 已切换分区[{curr_area_name}]！将切换监听房间", "Info", "green")

    return await area2room(area[0])


async def get_all():
    return [await area2room(i+1) for i in range(6)]
