from bilibili import bilibili
import requests
import datetime
import time


def CurrentTime():
    currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
    return currenttime

        
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
            
    def get_bag_list():
        url = "https://api.live.bilibili.com/gift/v2/gift/m_bag_list?" + 'access_key='+bilibili.access_key+'&actionKey='+bilibili.actionKey+'&appkey='+bilibili.appkey+'&build='+bilibili.build+'&device='+bilibili.device + '&mobi_app='+bilibili.mobi_app+'&platform='+bilibili.platform + '&ts=' + CurrentTime()
        response = requests.get(url, headers=bilibili.pcheaders)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '查询可用礼物')
        for i in range(len(response.json()['data'])):
            gift_name = response.json()['data'][i]['gift_name']
            gift_num = str(response.json()['data'][i]['gift_num']).center(4)
            expireat = str(round(int(response.json()['data'][i]['expireat']) / 86400, 1)).center(6)
            print("# " + gift_name + 'X' + gift_num, '(在' + expireat + '天后过期)')
    
    def user_info():
        url = "https://api.live.bilibili.com/User/getUserInfo?ts=" + CurrentTime()
        response = requests.get(url, headers=bilibili.pcheaders)
        json = response.json()
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '查询用户信息')
        if(json['code'] == 'REPONSE_OK'):
            data = json['data']
            uname = data['uname']
            silver = data['silver']
            gold = data['gold']
            achieve = data['achieve']
            user_level = data['user_level']
            user_next_level = data['user_next_level']
            user_intimacy = data['user_intimacy']
            user_next_intimacy = data['user_next_intimacy']
            user_level_rank = data['user_level_rank']
            billCoin = data['billCoin']
            print('# 用户名', uname)
            print('# 银瓜子', silver)
            print('# 金瓜子', gold)
            print('# 硬币数', billCoin)
            print('# 成就值', achieve)
            print('# 等级值', user_level, '———>', user_next_level)
            print('# 经验值', user_intimacy)
            print('# 剩余值', user_next_intimacy - user_intimacy)
            arrow = int(user_intimacy * 30 / user_next_intimacy)
            line = 30 - arrow
            percent = user_intimacy / user_next_intimacy * 100.0
            process_bar = '[' + '>' * arrow + '-' * line + ']' + '%.2f' % percent + '%'
            print(process_bar)
            print('# 等级榜', user_level_rank)
