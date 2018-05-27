import requests
import random

class MultiRoom():
    def asmr_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=1&cate_id=0&area_id=0&sort_type=online&page=1&page_size=100"
        response = requests.get(url,timeout=3)
        asmr_area_room = response.json()['data'][0]['roomid']
        return asmr_area_room

    def game_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=2&cate_id=0&area_id=0&sort_type=online&page=1&page_size=100"
        response = requests.get(url,timeout=3)
        game_area_room = response.json()['data'][random.randint(0,30)]['roomid']
        return game_area_room

    def mobile_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=3&cate_id=0&area_id=0&sort_type=online&page=1&page_size=100"
        response = requests.get(url,timeout=3)
        mobile_area_room = response.json()['data'][random.randint(0,30)]['roomid']
        return mobile_area_room

    def draw_area(self):
        url = "https://api.live.bilibili.com/room/v1/area/getRoomList?platform=web&parent_area_id=4&cate_id=0&area_id=0&sort_type=online&page=1&page_size=100"
        response = requests.get(url,timeout=3)
        draw_area_room = response.json()['data'][random.randint(0,30)]['roomid']
        return draw_area_room

    def get_all(self):
        try:
            asmr = 23058
            game = self.game_area()
            mobile = self.mobile_area()
            draw = self.draw_area()
            return [asmr,game,mobile,draw]
        except:
            self.get_all()




