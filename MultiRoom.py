import requests
import random

class MultiRoom():
    def asmr_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=online&page=1&page_size=-1"
        response = requests.get(url,timeout=3)
        checklen = len(response.json()['data'])
        asmr_area_room = response.json()['data'][random.randint(0,checklen)]['roomid']
        return asmr_area_room

    def game_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=2&cate_id=0&area_id=0&sort_type=online&page=1&page_size=-1"
        response = requests.get(url,timeout=3)
        checklen = len(response.json()['data'])
        game_area_room = response.json()['data'][random.randint(0,checklen)]['roomid']
        return game_area_room

    def mobile_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=3&cate_id=0&area_id=0&sort_type=online&page=1&page_size=-1"
        response = requests.get(url,timeout=3)
        checklen = len(response.json()['data'])
        mobile_area_room = response.json()['data'][random.randint(0,checklen)]['roomid']
        return mobile_area_room

    def draw_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=4&cate_id=0&area_id=0&sort_type=online&page=1&page_size=-1"
        response = requests.get(url,timeout=3)
        checklen = len(response.json()['data'])
        draw_area_room = response.json()['data'][random.randint(0,checklen)]['roomid']
        return draw_area_room

    def get_all(self):
        try:
            asmr = 23058
            game = self.game_area()
            mobile = self.mobile_area()
            draw = self.draw_area()
            return [asmr,game,mobile,draw]
        except:
            tmp = self.get_all()
            return tmp




