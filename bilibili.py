from PIL import Image
import sys
from imp import reload
import configloader
import os
import hashlib
import random
import requests
import datetime
import time
import math
import requests
import rsa
import base64
import configparser
from urllib import parse
import codecs
reload(sys)

def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)


def calculate_sign(str):
    hash = hashlib.md5()
    hash.update(str.encode('utf-8'))
    sign = hash.hexdigest()
    return sign


class bilibili():
    instance = None

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(bilibili, cls).__new__(cls, *args, **kw)
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            cls.instance.file_bilibili = fileDir + "/conf/bilibili.conf"
            cls.instance.dic_bilibili = configloader.load_bilibili(cls.instance.file_bilibili)
            cls.instance.activity_raffleid_list = []
            cls.instance.activity_roomid_list = []
            # cls.instance.activity_time_list = []
            cls.instance.TV_raffleid_list = []
            cls.instance.TV_roomid_list = []
            # cls.instance.TV_time_list = []
            # cls.instance.TVsleeptime = 185
            # cls.instance.activitysleeptime = 125

        return cls.instance

    def post_watching_history(self, room_id):
        data = {
            "room_id": room_id,
            "csrf_token": self.dic_bilibili['csrf']
        }
        url = "https://api.live.bilibili.com/room/v1/Room/room_entry_action"
        response = requests.post(url, data=data, headers=self.dic_bilibili['pcheaders'])
        return 0

    def check_room_true(self, roomid):
        url = "https://api.live.bilibili.com/room/v1/Room/room_init?id=" + str(roomid)
        response = requests.get(url, headers=self.dic_bilibili['pcheaders'])
        if response.json()['code'] == 0:
            param1 = response.json()['data']['is_hidden']
            param2 = response.json()['data']['is_locked']
            param3 = response.json()['data']['encrypted']
            return param1, param2, param3

    def silver2coin(self):
        url = "https://api.live.bilibili.com/exchange/silver2coin"
        response = requests.post(url, headers=self.dic_bilibili['pcheaders'])
        print("#", response.json()['msg'])
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili[
                          'mobi_app'] + '&platform=' + self.dic_bilibili['platform'] + '&ts=' + CurrentTime()
        params = temp_params + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        app_url = "https://api.live.bilibili.com/AppExchange/silver2coin?" + temp_params + "&sign=" + str(
            hash.hexdigest())
        response1 = requests.post(app_url, headers=self.dic_bilibili['appheaders'])
        print("#", response1.json()['msg'])

    def get_bag_list(self):
        url = "http://api.live.bilibili.com/gift/v2/gift/bag_list"
        response = requests.get(url, headers=self.dic_bilibili['pcheaders'])
        temp = []
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '查询可用礼物')
        for i in range(len(response.json()['data']['list'])):
            bag_id = (response.json()['data']['list'][i]['bag_id'])
            gift_id = (response.json()['data']['list'][i]['gift_id'])
            gift_num = str((response.json()['data']['list'][i]['gift_num'])).center(4)
            gift_name = response.json()['data']['list'][i]['gift_name']
            expireat = (response.json()['data']['list'][i]['expire_at'])
            left_time = (expireat - int(CurrentTime()))
            left_days = (expireat - int(CurrentTime())) / 86400
            print("# " + gift_name + 'X' + gift_num, '(在' + str(math.ceil(left_days)) + '天后过期)')
            if 0 < int(left_time) < 43200:   # 剩余时间少于半天时自动送礼
                temp.append([gift_id, gift_num, bag_id])
        return temp

    def get_uid_in_room(self, roomID):
        url = "https://api.live.bilibili.com/room/v1/Room/room_init?id=" + roomID
        response = requests.get(url, headers=self.dic_bilibili['pcheaders'])
        return response.json()['data']['uid'], response.json()['data']['room_id']

    def send_bag_gift_web(self, roomID, giftID, giftNum, bagID):
        url = "http://api.live.bilibili.com/gift/v2/live/bag_send"
        temp = self.get_uid_in_room(roomID)
        data = {
            'uid': self.dic_bilibili['uid'],
            'gift_id': giftID,
            'ruid': temp[0],
            'gift_num': giftNum,
            'bag_id': bagID,
            'platform': 'pc',
            'biz_code': 'live',
            'biz_id': temp[1],
            'rnd': CurrentTime(),
            'storm_beat_id': '0',
            'metadata': '',
            'price': '0',
            'csrf_token': self.dic_bilibili['csrf']
        }
        response = requests.post(url, headers=self.dic_bilibili['pcheaders'], data=data)
        try:
            # print(response.json())
            print("# 清理快到期礼物:", response.json()['data']['gift_name'] + "x" + str(response.json()['data']['gift_num']))
        except:
            print("# 清理快到期礼物成功，但请联系开发者修bug!")

    def user_info(self):
        url = "https://api.live.bilibili.com/i/api/liveinfo"
        response = requests.get(url, headers=self.dic_bilibili['pcheaders'])
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '查询用户信息')
        if (response.json()['code'] == 0):
            uname = response.json()['data']['userInfo']['uname']
            achieve = response.json()['data']['achieves']
            user_level = response.json()['data']['userCoinIfo']['user_level']
            silver = response.json()['data']['userCoinIfo']['silver']
            gold = response.json()['data']['userCoinIfo']['gold']
            user_next_level = response.json()['data']['userCoinIfo']['user_next_level']
            user_intimacy = response.json()['data']['userCoinIfo']['user_intimacy']
            user_next_intimacy = response.json()['data']['userCoinIfo']['user_next_intimacy']
            user_level_rank = response.json()['data']['userCoinIfo']['user_level_rank']
            billCoin = response.json()['data']['userCoinIfo']['coins']
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
        list_url = ["access_key=" + self.dic_bilibili['access_key'], "appkey=" + self.dic_bilibili['appkey'], 'aid=',
                    'page=1', "build=" + self.dic_bilibili['build']]
        sign = calculate_sign('&'.join(sorted(list_url)) + self.dic_bilibili['app_secret'])

        url = url + '&'.join(list_url[:3] + ['sign=' + sign] + list_url[3:])

        data = {
            'access_key': self.dic_bilibili['access_key'],
            'actionKey': "appkey",
            'appkey': self.dic_bilibili['appkey'],
            'build': self.dic_bilibili['build'],
            # 房间号
            'cid': roomId,
            # 颜色
            'color': '16777215',
            'device': self.dic_bilibili['device'],
            # 字体大小
            'fontsize': '25',
            # 实际上并不需要包含 mid 就可以正常发送弹幕, 但是真实的 Android 客户端确实发送了 mid
            # 自己的用户 ID!!!!
            'from': '',
            # 'mid': '1008****'
            'mobi_app': self.dic_bilibili['mobi_app'],
            # 弹幕模式
            # 1 普通  4 底端  5 顶端 6 逆向  7 特殊   9 高级
            # 一些模式需要 VIP
            'mode': '1',
            # 内容
            "msg": msg,
            'platform': self.dic_bilibili['platform'],
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
            'sign': sign,
            'ts': time,
            # 必须为 "json"
            'type': "json"
        }

        response = requests.post(url, headers=self.dic_bilibili['appheaders'], data=data)
        print(response.json())

    def send_danmu_msg_web(self, msg, roomId):
        url = 'https://api.live.bilibili.com/msg/send'
        data = {
            'color': '16777215',
            'fontsize': '25',
            'mode': '1',
            'msg': msg,
            'rnd': '0',
            'roomid': roomId,
            'csrf_token': self.dic_bilibili['csrf']
        }

        response = requests.post(url, headers=self.dic_bilibili['pcheaders'], data=data)
        print(response.json())

    def GetHash(self):
        url = 'https://passport.bilibili.com/api/oauth2/getKey'
        temp_params = 'appkey=' + self.dic_bilibili['appkey'] + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(temp_params.encode('utf-8'))
        sign = hash.hexdigest()
        params = {'appkey': self.dic_bilibili['appkey'], 'sign': sign}
        response = requests.post(url, data=params)
        value = response.json()['data']
        return value

    def login(self):
        if self.dic_bilibili['account']['username']:
            username = str(self.dic_bilibili['account']['username'])
            password = str(self.dic_bilibili['account']['password'])
        else:
            username = input("# 输入帐号: ")
            password = input("# 输入密码: ")
            config = configparser.ConfigParser()
            config.optionxform = str
            config.read_file(codecs.open(self.file_bilibili, "r", "utf8"))
            config.set('account', 'username', username)
            config.set('account', 'password', password)
            config.write(codecs.open(self.file_bilibili, "w+", "utf8"))
        if username != "":
            value = self.GetHash()
            key = value['key']
            Hash = str(value['hash'])
            pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode())
            password = base64.b64encode(rsa.encrypt((Hash + password).encode('utf-8'), pubkey))
            password = parse.quote_plus(password)
            username = parse.quote_plus(username)
            # url = 'https://passport.bilibili.com/api/oauth2/login'   //旧接口
            url = "https://passport.bilibili.com/api/v2/oauth2/login"
            temp_params = 'appkey=' + self.dic_bilibili['appkey'] + '&password=' + password + '&username=' + username
            params = temp_params + self.dic_bilibili['app_secret']
            hash = hashlib.md5()
            hash.update(params.encode('utf-8'))
            sign = hash.hexdigest()
            headers = {"Content-type": "application/x-www-form-urlencoded"}
            payload = "appkey=" + self.dic_bilibili[
                'appkey'] + "&password=" + password + "&username=" + username + "&sign=" + sign
            response = requests.post(url, data=payload, headers=headers)
            if response.json()['code'] == -105:
                headers = {
                    'Accept': 'application/json, text/plain, */*',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                    'Host': 'passport.bilibili.com',
                    'cookie':"sid=hxt5szbb"
                }
                s = requests.session()
                url = "https://passport.bilibili.com/captcha"
                res = s.get(url,headers=headers)
                with open("capture.png","wb")as f:
                    f.write(res.content)  # 验证码图片
                try:
                    img = Image.open('capture.png')
                    img.show()
                except:
                    self.capture_output()
                captcha=input("输入验证码:")
                temp_params = 'actionKey=' + self.dic_bilibili[
                    'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                                  'build'] + '&captcha='+captcha+'&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili['mobi_app'] + '&password='+ password +'&platform=' + self.dic_bilibili[
                                  'platform'] +'&username='+username
                params = temp_params + self.dic_bilibili['app_secret']
                hash = hashlib.md5()
                hash.update(params.encode('utf-8'))
                sign = hash.hexdigest()
                payload = temp_params + '&sign=' + sign
                headers['Content-type'] = "application/x-www-form-urlencoded"
                headers['cookie'] = "sid=hxt5szbb"
                url = "https://passport.bilibili.com/api/v2/oauth2/login"
                response = s.post(url,data=payload,headers=headers)
            try:
                access_key = response.json()['data']['token_info']['access_token']
                cookie = (response.json()['data']['cookie_info']['cookies'])
                cookie_format = ""
                for i in range(0, len(cookie)):
                    cookie_format = cookie_format + cookie[i]['name'] + "=" + cookie[i]['value'] + ";"
                self.dic_bilibili['csrf'] = cookie[0]['value']
                self.dic_bilibili['access_key'] = access_key
                self.dic_bilibili['cookie'] = cookie_format
                self.dic_bilibili['uid'] = cookie[1]['value']
                self.dic_bilibili['pcheaders'] = {
                    'Accept': 'application/json, text/plain, */*',
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'accept-encoding': 'gzip, deflate',
                    'Host': 'api.live.bilibili.com',
                    'cookie': cookie_format
                }
                self.dic_bilibili['appheaders'] = {
                    "User-Agent": "bili-universal/6570 CFNetwork/894 Darwin/17.4.0",
                    "Accept-encoding": "gzip",
                    "Buvid": "000ce0b9b9b4e342ad4f421bcae5e0ce",
                    "Display-ID": "146771405-1521008435",
                    "Accept-Language": "zh-CN",
                    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                    "Connection": "keep-alive",
                    "Host": "api.live.bilibili.com",
                    'cookie': cookie_format
                }

                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "登陆成功")
            except:
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "登录失败,错误信息为:",
                      response.json()['message'])

    def capture_output(self):
        output_width = 140  # 终端展现的大小
        output_height = 140  # 终端展现的大小
        image_path = 'capture.png'
        image = Image.open(image_path)
        if image.mode is not 'RGB':
            image = image.convert('RGB')
        image_width, image_height = image.size
        w_scale = output_width * 1.0 / image_width
        h_scale = output_height * 1.0 / image_height
        scale = w_scale if w_scale < h_scale else h_scale
        res_width = int(scale * image_width)
        res_height = int(scale * image_height)
        image = image.resize((res_width, res_height), Image.HAMMING)
        image_pixels = image.load()
        out_width, out_height = image.size
        replace_chars = '01'
        terminal_chars = ''
        for h in range(out_height):
            for w in range(out_width):
                point_pixel = image_pixels[w, h]
                terminal_chars += replace_chars[int(sum(point_pixel) / 3.0 / 256.0 * len(replace_chars))]
            terminal_chars += '\n'
        print(terminal_chars)

    def get_gift_of_storm(self, dic):
        roomid = dic['roomid']
        get_url = "http://api.live.bilibili.com/lottery/v1/Storm/check?roomid=" + str(roomid)
        response = requests.get(get_url, headers=self.dic_bilibili['pcheaders'])
        temp = response.json()
        check = len(temp['data'])
        if check != 0 and temp['data']['hasJoin'] != 1:
            id = temp['data']['id']
            storm_url = 'http://api.live.bilibili.com/lottery/v1/Storm/join'
            payload = {
                "id": id,
                "color": "16777215",
                "captcha_token": "",
                "captcha_phrase": "",
                "token": "",
                "csrf_token": self.dic_bilibili['csrf']}
            response1 = requests.post(storm_url, data=payload, headers=self.dic_bilibili['pcheaders'], timeout=2)
            return response1
        else:
            return None

    def get_gift_of_events(self, text1, text2, raffleid):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'cookie': self.dic_bilibili['cookie'],
            'referer': text2
        }
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&event_type=flower_rain-' + str(
            raffleid) + '&mobi_app=' + self.dic_bilibili['mobi_app'] + '&platform=' + self.dic_bilibili[
                          'platform'] + '&room_id=' + str(
            text1) + '&ts=' + CurrentTime()
        params = temp_params + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        true_url = 'http://api.live.bilibili.com/YunYing/roomEvent?' + temp_params + '&sign=' + str(
            hash.hexdigest())
        pc_url = 'http://api.live.bilibili.com/activity/v1/Raffle/join?roomid=' + str(
            text1) + '&raffleId=' + str(raffleid)
        response1 = requests.get(true_url, params=params, headers=headers)
        pc_response = requests.get(pc_url, headers=headers)

        return response1, pc_response

    def get_gift_of_TV(self, real_roomid, raffleid):
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&id=' + str(
            raffleid) + '&mobi_app=' + self.dic_bilibili['mobi_app'] + '&platform=' + self.dic_bilibili[
                          'platform'] + '&roomid=' + str(
            real_roomid) + '&ts=' + CurrentTime()
        params = temp_params + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        true_url = 'http://api.live.bilibili.com/AppSmallTV/join?' + temp_params + '&sign=' + str(
            hash.hexdigest())
        response2 = requests.get(true_url, headers=self.dic_bilibili['appheaders'])
        return response2

    def get_gift_of_captain(self, roomid, id):
        join_url = "https://api.live.bilibili.com/lottery/v1/lottery/join"
        payload = {"roomid": roomid, "id": id, "type": "guard", "csrf_token": self.dic_bilibili['csrf']}
        print(payload)
        response2 = requests.post(join_url, data=payload, headers=self.dic_bilibili['pcheaders'])
        return response2

    def get_giftlist_of_events(self, text1):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'Host': 'api.live.bilibili.com',
        }
        url = 'http://api.live.bilibili.com/activity/v1/Raffle/check?roomid=' + str(text1)
        response = requests.get(url, headers=headers)

        return response

    def get_giftlist_of_TV(self, real_roomid):
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + \
                      '&mobi_app=' + self.dic_bilibili['mobi_app'] + '&platform=' + self.dic_bilibili[
                          'platform'] + '&roomid=' + str(
            real_roomid) + '&ts=' + CurrentTime()
        params = temp_params + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        check_url = 'https://api.live.bilibili.com/AppSmallTV/index?' + temp_params + '&sign=' + str(
            hash.hexdigest())
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        }
        response = requests.get(check_url, headers=headers)

        return response

    def get_giftlist_of_captain(self, roomid):
        true_url = 'https://api.live.bilibili.com/lottery/v1/lottery/check?roomid=' + str(roomid)
        response1 = requests.get(true_url)
        return response1

    def append_to_activitylist(self, raffleid, text1, time=''):
        self.activity_raffleid_list.append(raffleid)
        self.activity_roomid_list.append(text1)
        # self.activity_time_list.append(int(time))
        # self.activity_time_list.append(int(CurrentTime()))

    def append_to_TVlist(self, raffleid, real_roomid, time=''):
        self.TV_raffleid_list.append(raffleid)
        self.TV_roomid_list.append(real_roomid)
        # self.TV_time_list.append(int(time)+int(CurrentTime()))
        # self.TV_time_list.append(int(CurrentTime()))

    def check_TVlist(self, raffleid):
        if raffleid not in self.TV_raffleid_list:
            return True
        return False

    def check_activitylist(self, raffleid):
        if raffleid not in self.activity_raffleid_list:
            return True
        return False

    def get_giftids_raffle(self, str):
        return self.dic_bilibili['giftids_raffle'][str]

    def get_giftids_raffle_keys(self):
        return self.dic_bilibili['giftids_raffle'].keys()

    def get_activity_result(self, activity_roomid, activity_raffleid):
        url = "http://api.live.bilibili.com/activity/v1/Raffle/notice?roomid=" + str(
            activity_roomid) + "&raffleId=" + str(activity_raffleid)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'Host': 'api.live.bilibili.com',
            'cookie': self.dic_bilibili['cookie'],
        }
        response = requests.get(url, headers=headers)
        return response

    def get_TV_result(self, TV_roomid, TV_raffleid):
        url = "http://api.live.bilibili.com/gift/v2/smalltv/notice?roomid=" + str(TV_roomid) + "&raffleId=" + str(
            TV_raffleid)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'Host': 'api.live.bilibili.com',
            'cookie': self.dic_bilibili['cookie'],
        }
        response = requests.get(url, headers=headers)
        return response

    def delete_0st_activitylist(self):
        del self.activity_roomid_list[0]
        del self.activity_raffleid_list[0]
        # del self.activity_time_list[0]

    def delete_0st_TVlist(self):
        del self.TV_roomid_list[0]
        del self.TV_raffleid_list[0]
        # del self.TV_time_list[0]

    def clean_activity(self):
        # print(self.activity_raffleid_list)
        if self.activity_raffleid_list:
            for i in range(0, len(self.activity_roomid_list)):
                response = self.get_activity_result(self.activity_roomid_list[0], self.activity_raffleid_list[0])
                json_response = response.json()
                # print(json_response)
                if json_response['code'] == 0:
                    data = json_response['data']
                    print("# 房间", str(self.activity_roomid_list[0]).center(9), "网页端活动抽奖结果:",
                          data['gift_name'] + "x" + str(data['gift_num']))

                    self.delete_0st_activitylist()

                elif json_response['code'] == -400:
                    # sleepseconds = self.activitysleeptime + self.activity_time_list[0] - int(CurrentTime())+ 2
                    # sleepseconds = self.activity_time_list[0] - int(CurrentTime())
                    # return sleepsecondsq
                    return

                else:
                    print('未知情况')
                    print(json_response)

        else:
            return

    def clean_TV(self):
        # print(self.TV_raffleid_list)
        if self.TV_raffleid_list:
            for i in range(0, len(self.TV_roomid_list)):

                response = self.get_TV_result(self.TV_roomid_list[0], self.TV_raffleid_list[0])
                # if response.json()['data']['gift_name'] != "":
                json_response = response.json()
                # print(json_response)
                if json_response['data']['gift_id'] == '-1':
                    return
                elif json_response['data']['gift_id'] != '-1':

                    data = json_response['data']
                    print("# 房间", str(self.TV_roomid_list[0]).center(9), "小电视道具抽奖结果:",
                          data['gift_name'] + "x" + str(data['gift_num']))

                    self.delete_0st_TVlist()
            # else:
            # print(int(CurrentTime()))
            # sleepseconds = self.TV_time_list[0] - int(CurrentTime()) + 1
            # sleepseconds = self.TV_time_list[0] - int(CurrentTime())
            # return

            #  else:
            # print('未知')
        else:
            return

    def pcpost_heartbeat(self):
        url = 'http://api.live.bilibili.com/User/userOnlineHeart'
        response = requests.post(url, headers=self.dic_bilibili['pcheaders'])

    # 发送app心跳包
    def apppost_heartbeat(self):
        time = CurrentTime()
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili[
                          'mobi_app'] + '&platform=' + self.dic_bilibili['platform'] + '&ts=' + time
        params = temp_params + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        url = 'https://api.live.bilibili.com/mobile/userOnlineHeart?' + temp_params + '&sign=' + str(hash.hexdigest())
        payload = {'roomid': 23058, 'scale': 'xhdpi'}
        response = requests.post(url, data=payload, headers=self.dic_bilibili['appheaders'])
        # print("app端心跳状态：" + response.json()['message'])

    # 心跳礼物
    def heart_gift(self):
        url = "https://api.live.bilibili.com/gift/v2/live/heart_gift_receive?roomid=3&area_v2_id=34"
        response = requests.get(url, headers=self.dic_bilibili['pcheaders'])
        # print(response.json())

    def get_lotterylist(self, i):
        url = "https://api.live.bilibili.com/lottery/v1/box/getStatus?aid=" + str(i)
        response = requests.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def get_gift_of_lottery(self, i, g):
        url1 = 'https://api.live.bilibili.com/lottery/v1/box/draw?aid=' + str(i) + '&number=' + str(g + 1)
        response1 = requests.get(url1, headers=self.dic_bilibili['pcheaders'])
        return response1

    def get_time_about_silver(self):
        time = CurrentTime()
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili[
                          'mobi_app'] + '&platform=' + self.dic_bilibili['platform'] + '&ts=' + time
        params = temp_params + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        GetTask_url = 'https://api.live.bilibili.com/mobile/freeSilverCurrentTask?' + temp_params + '&sign=' + str(
            hash.hexdigest())
        response = requests.get(GetTask_url, headers=self.dic_bilibili['appheaders'])
        return response

    def get_silver(self, timestart, timeend):
        time = CurrentTime()
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili[
                          'mobi_app'] + '&platform=' + self.dic_bilibili[
                          'platform'] + '&time_end=' + timeend + '&time_start=' + timestart + '&ts=' + time
        params = temp_params + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        url = 'https://api.live.bilibili.com/mobile/freeSilverAward?' + temp_params + '&sign=' + str(
            hash.hexdigest())
        response = requests.get(url, headers=self.dic_bilibili['appheaders'])
        return response

    def get_dailybag(self):
        url = 'http://api.live.bilibili.com/gift/v2/live/receive_daily_bag'
        response = requests.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def get_dosign(self):
        url = 'https://api.live.bilibili.com/sign/doSign'
        response = requests.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def get_dailytask(self):
        url = 'https://api.live.bilibili.com/activity/v1/task/receive_award'
        payload2 = {'task_id': 'double_watch_task'}
        response2 = requests.post(url, data=payload2, headers=self.dic_bilibili['appheaders'])
        return response2

    def get_grouplist(self):
        url = "https://api.vc.bilibili.com/link_group/v1/member/my_groups"
        pcheaders = self.dic_bilibili['pcheaders'].copy()
        pcheaders['Host'] = "api.vc.bilibili.com"
        response = requests.get(url, headers=pcheaders)
        return response

    def assign_group(self, i1, i2):
        temp_params = "_device=" + self.dic_bilibili[
            'device'] + "&_hwid=SX1NL0wuHCsaKRt4BHhIfRguTXxOfj5WN1BkBTdLfhstTn9NfUouFiUV&access_key=" + \
                      self.dic_bilibili['access_key'] + "&appkey=" + self.dic_bilibili['appkey'] + "&build=" + \
                      self.dic_bilibili['build'] + "&group_id=" + str(i1) + "&mobi_app=" + self.dic_bilibili[
                          'mobi_app'] + "&owner_id=" + str(i2) + "&platform=" + self.dic_bilibili[
                          'platform'] + "&src=xiaomi&trace_id=20171224024300024&ts=" + CurrentTime() + "&version=5.20.1.520001"
        params = temp_params + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        url = "https://api.vc.bilibili.com/link_setting/v1/link_setting/sign_in?" + temp_params + "&sign=" + str(
            hash.hexdigest())
        appheaders = self.dic_bilibili['appheaders'].copy()
        appheaders['Host'] = "api.vc.bilibili.com"
        response = requests.get(url, headers=appheaders)
        return response

# a = bilibili()
# b = bilibili()
# print(a is b)
# print(a.dic_bilibili['giftids_raffle'])
# bilibili().test(1)
# bilibili().login()
# print(bilibili().dic_bilibili)
