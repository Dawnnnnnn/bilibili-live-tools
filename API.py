from bilibili import bilibili
import requests


class API(bilibili):
    # 本函数只是实现了直播观看历史里的提交，与正常观看仍有区别！！
    # 其实csrf_token就是用了token，我懒得再提出来了
    # 就是Login函数里面的cookie[0]['value']
    def post_watching_history(csrf_token, room_id):
        data = {
            "room_id": room_id,
            "csrf_token": csrf_token
            }
        ulr = "https://api.live.bilibili.com/room/v1/Room/room_entry_action"
        response = requests.post(ulr, data=data, headers=bilibili.pcheaders)
        # print(response.json())
        return 0
