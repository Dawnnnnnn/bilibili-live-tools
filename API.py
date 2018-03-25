from bilibili import bilibili
import requests
import datetime
import time


class API(bilibili):
    # 本函数只是实现了直播观看历史里的提交，与正常观看仍有区别！！
    # 其实csrf_token就是用了token，我懒得再提出来了
    # 就是Login函数里面的cookie[0]['value']
    def post_watching_history(csrf_token, room_id):
        data = {
            "room_id": room_id,
            "csrf_token": csrf_token
            }
        url = "https://api.live.bilibili.com/room/v1/Room/room_entry_action"
        requests.post(url, data=data, headers=bilibili.pcheaders)
        # print(response.json())
        return 0
        
    def CurrentTime():
        currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
        return currenttime
    
    def get_bag_list():
        url = "https://api.live.bilibili.com/gift/v2/gift/m_bag_list?" + 'access_key='+bilibili.access_key+'&actionKey='+bilibili.actionKey+'&appkey='+bilibili.appkey+'&build='+bilibili.build+'&device='+bilibili.device + '&mobi_app='+bilibili.mobi_app+'&platform='+bilibili.platform + '&ts=' + API.CurrentTime()
        response = requests.get(url, headers=bilibili.pcheaders)
        for i in range(len(response.json()['data'])):
            gift_name = response.json()['data'][i]['gift_name']
            gift_num = str(response.json()['data'][i]['gift_num']).center(4)
            expireat = str(round(int(response.json()['data'][i]['expireat']) / 86400, 1)).center(6)
            print(gift_name, 'X', gift_num, '(在', expireat, '天后过期)')
