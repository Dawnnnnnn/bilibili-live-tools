import requests
import random


class MultiRoom():

    def asmr_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
        response = requests.get(url, timeout=3)
        checklen = len(response.json()['data'])
        asmr_area_room = response.json()['data'][random.randint(0, checklen)]['roomid']
        state = self.check_state(asmr_area_room)
        if state == 1:
            return [asmr_area_room,"娱乐分区"]
        else:
            print("检测到房间未开播，立即尝试重新获取")
            tmp = self.asmr_area()
            return tmp


    def game_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=2&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
        response = requests.get(url, timeout=3)
        checklen = len(response.json()['data'])
        game_area_room = response.json()['data'][random.randint(0, checklen)]['roomid']
        state = self.check_state(game_area_room)
        if state == 1:
            return [game_area_room,"游戏分区"]
        else:
            print("检测到房间未开播，立即尝试重新获取")
            tmp = self.game_area()
            return tmp

    def mobile_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=3&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
        response = requests.get(url, timeout=3)
        checklen = len(response.json()['data'])
        mobile_area_room = response.json()['data'][random.randint(0, checklen)]['roomid']
        state = self.check_state(mobile_area_room)
        if state == 1:
            return [mobile_area_room,"手游分区"]
        else:
            print("检测到房间未开播，立即尝试重新获取")
            tmp = self.mobile_area()
            return tmp

    def draw_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=4&cate_id=0&area_id=0&sort_type=online&page=1&page_size=30"
        response = requests.get(url, timeout=3)
        checklen = len(response.json()['data'])
        draw_area_room = response.json()['data'][random.randint(0, checklen)]['roomid']
        state = self.check_state(draw_area_room)
        if state == 1:
            return [draw_area_room,"绘画分区"]
        else:
            print("检测到房间未开播，立即尝试重新获取")
            tmp = self.draw_area()
            return tmp

    def check_state(self,roomid):
        url = "https://api.live.bilibili.com/room/v1/Room/room_init?id="+str(roomid)
        response = requests.get(url)
        state = response.json()['data']['live_status']
        return state

    def get_all(self):
        try:
            asmr = [23058,"娱乐分区"]
            game = self.game_area()
            mobile = self.mobile_area()
            draw = self.draw_area()
            return [asmr, game, mobile, draw]
        except:
            print("获取房间列表失败,立即进行下次尝试")
            tmp = self.get_all()
            return tmp
