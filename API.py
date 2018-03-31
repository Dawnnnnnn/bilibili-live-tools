from bilibili import bilibili
import hashlib
import random
import requests
import datetime
import time


def CurrentTime():
    currenttime = str(int(time.mktime(datetime.datetime.now().timetuple())))
    return currenttime

def calculate_sign(str):
    #value = self.GetHash()
   # key = value['key']
    #Hash = str(value['hash'])
   # pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode())
   # password = base64.b64encode(rsa.encrypt((Hash + password).encode('utf-8'), pubkey))
  #  password = parse.quote_plus(password)
   # username = parse.quote_plus(username)
    hash = hashlib.md5()
    hash.update(str.encode('utf-8'))
    sign = hash.hexdigest()
    return sign
        
class API():
    def __init__(self, bilibili):
        self.bilibili = bilibili
    # 本函数只是实现了直播观看历史里的提交，与正常观看仍有区别！！
    # 其实csrf_token就是用了token，我懒得再提出来了
    # 就是Login函数里面的cookie[0]['value']

        

    def post_watching_history(self,csrf_token, room_id):
        data = {
            "room_id": room_id,
            "csrf_token": csrf_token
            }
        url = "https://api.live.bilibili.com/room/v1/Room/room_entry_action"
        response = requests.post(url, data=data, headers=self.bilibili.pcheaders)
        #print(response.json())
        return 0
    def check_room_true(self,roomid):
        url = "https://api.live.bilibili.com/room/v1/Room/room_init?id="+str(roomid)
        response = requests.get(url,headers=self.bilibili.pcheaders)
        if response.json()['code'] == 0:
            param1 = response.json()['data']['is_hidden']
            param2 = response.json()['data']['is_locked']
            param3 = response.json()['data']['encrypted']
            return param1,param2,param3


    def get_bag_list(self):
        url = "https://api.live.bilibili.com/gift/v2/gift/m_bag_list?" + 'access_key='+self.bilibili.access_key+'&actionKey='+self.bilibili.actionKey+'&appkey='+self.bilibili.appkey+'&build='+self.bilibili.build+'&device='+self.bilibili.device + '&mobi_app='+self.bilibili.mobi_app+'&platform='+self.bilibili.platform + '&ts=' + CurrentTime()
        response = requests.get(url, headers=self.bilibili.pcheaders)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '查询可用礼物')
        for i in range(len(response.json()['data'])):
            gift_name = response.json()['data'][i]['gift_name']
            gift_num = str(response.json()['data'][i]['gift_num']).center(4)
            expireat = str(round(int(response.json()['data'][i]['expireat']) / 86400, 1)).center(6)
            print("# " + gift_name + 'X' + gift_num, '(在' + expireat + '天后过期)')
    
    def user_info(self):
        url = "https://api.live.bilibili.com/User/getUserInfo?ts=" + CurrentTime()
        response = requests.get(url, headers=self.bilibili.pcheaders)
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

    def send_danmu_msg_andriod(self, msg, roomId):
        url = 'https://api.live.bilibili.com/api/sendmsg?'
        # page ??
        time = CurrentTime()
        list_url = ["access_key=" + self.bilibili.access_key, "appkey=" + self.bilibili.appkey,  'aid=', 'page=1', "build=" + self.bilibili.build]
        sign = calculate_sign('&'.join(sorted(list_url))+self.bilibili.app_secret)
                
        url = url + '&'.join(list_url[:3] + ['sign='+sign] + list_url[3:])
        # print(url)
        data = {
            'access_key': self.bilibili.access_key,
            'actionKey': "appkey",
            'appkey':  self.bilibili.appkey,
            'build':  self.bilibili.build,
            # 房间号
            'cid':  roomId,
            # 颜色
            'color':  '16777215',
            'device':  self.bilibili.device,
            # 字体大小
            'fontsize': '25',
            # 实际上并不需要包含 mid 就可以正常发送弹幕, 但是真实的 Android 客户端确实发送了 mid
            # 自己的用户 ID!!!!
            'from': '',
            # 'mid': '1008****'
            'mobi_app':  self.bilibili.mobi_app,
            # 弹幕模式
            # 1 普通  4 底端  5 顶端 6 逆向  7 特殊   9 高级
            # 一些模式需要 VIP
            'mode': '1',
            # 内容
            "msg": msg,
            'platform': self.bilibili.platform,
            # 播放时间
            'playTime': '0.0',
            # 弹幕池  尚且只见过为 0 的情况
            'pool': '0',
            # random   随机数
            # 在 web 端发送弹幕, 该字段是固定的, 为用户进入直播页面的时间的时间戳. 但是在 Android 端, 这是一个随机数
            # 该随机数不包括符号位有 9 位
            # '1367301983632698015'
            'rnd': str((int)(1000000000000000000.0 + 2000000000000000000.0 * random.random())),
            "screen_state": '',
            # 反正不管用 没实现的
            'sign':  sign,
            'ts':  time,
            # 必须为 "json"
            'type': "json"
        }
        # print(data)
        response = requests.post(url, headers=self.bilibili.appheaders, data=data)
        print(response.json())

    
    def send_danmu_msg_web(self,msg, roomId):
        url = 'https://api.live.bilibili.com/msg/send'
        data = {
            'color' : '16777215',
            'fontsize' : '25',
            'mode' : '1',
            'msg' : msg,
            'rnd' : '0',
            'roomid' : roomId,
            'csrf_token' :self.bilibili.csrf
        }


        response = requests.post(url, headers=self.bilibili.pcheaders, data=data)
        print(response.json())
