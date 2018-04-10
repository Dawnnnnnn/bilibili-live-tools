import sys
from imp import reload
import configloader
import os
import hashlib
import random
import datetime
import time
import requests
import rsa
import base64
from urllib import parse

reload(sys)


def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)

def cnn_captcha(img):
    url = "http://101.236.6.31:8080/code"
    data = {"image": img}
    ressponse = requests.post(url, data=data)
    captcha = ressponse.text
    print("此次登录出现验证码,识别结果为%s"%(captcha))
    return captcha

def calc_name_passw(key, Hash, username, password):
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode())
    password = base64.b64encode(rsa.encrypt((Hash + password).encode('utf-8'), pubkey))
    password = parse.quote_plus(password)
    username = parse.quote_plus(username)
    return username, password

    





class bilibili():
    instance = None

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(bilibili, cls).__new__(cls, *args, **kw)
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            file_bilibili = fileDir + "/conf/bilibili.conf"
            cls.instance.dic_bilibili = configloader.load_bilibili(file_bilibili)
            cls.instance.bili_section = requests.session()
            print('正在登陆中...')
            tag, msg = cls.instance.login()
            if tag:
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "登陆成功")
            else:
                print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), "登录失败,错误信息为:", msg)
        return cls.instance
        
    def calc_sign(self, str):
        str = str + self.dic_bilibili['app_secret']
        hash = hashlib.md5()
        hash.update(str.encode('utf-8'))
        sign = hash.hexdigest()
        return sign

    def post_watching_history(self, room_id):
        data = {
            "room_id": room_id,
            "csrf_token": self.dic_bilibili['csrf']
        }
        url = "https://api.live.bilibili.com/room/v1/Room/room_entry_action"
        response = self.bili_section.post(url, data=data, headers=self.dic_bilibili['pcheaders'])
        return response

    
    def silver2coin(self):
        url = "https://api.live.bilibili.com/exchange/silver2coin"
        response = self.bili_section.post(url, headers=self.dic_bilibili['pcheaders'])
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili[
                          'mobi_app'] + '&platform=' + self.dic_bilibili['platform'] + '&ts=' + CurrentTime()
        sign = self.calc_sign(temp_params)
        app_url = "https://api.live.bilibili.com/AppExchange/silver2coin?" + temp_params + "&sign=" + sign
        response1 = self.bili_section.post(app_url, headers=self.dic_bilibili['appheaders'])
        return response, response1
        
    def request_check_room(self, roomid):
        url = "https://api.live.bilibili.com/room/v1/Room/room_init?id=" + str(roomid)
        response = self.bili_section.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def request_fetch_bag_list(self):
        url = "https://api.live.bilibili.com/gift/v2/gift/bag_list"
        response = self.bili_section.get(url, headers=self.dic_bilibili['pcheaders'])
        return response
        
    def request_check_taskinfo(self):
        url = 'https://api.live.bilibili.com/i/api/taskInfo'
        response = self.bili_section.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def request_send_gift_web(self, giftid, giftnum, bagid, ruid, biz_id):
        url = "https://api.live.bilibili.com/gift/v2/live/bag_send"
        data = {
            'uid': self.dic_bilibili['uid'],
            'gift_id': giftid,
            'ruid': ruid,
            'gift_num': giftnum,
            'bag_id': bagid,
            'platform': 'pc',
            'biz_code': 'live',
            'biz_id': biz_id,
            'rnd': CurrentTime(),
            'storm_beat_id': '0',
            'metadata': '',
            'price': '0',
            'csrf_token': self.dic_bilibili['csrf']
        }
        response = self.bili_section.post(url, headers=self.dic_bilibili['pcheaders'], data=data)
        return response

    def request_fetch_user_info(self):
        url = "https://api.live.bilibili.com/i/api/liveinfo"
        response = self.bili_section.get(url, headers=self.dic_bilibili['pcheaders'])
        return response


    def request_send_danmu_msg_andriod(self, msg, roomId):
        url = 'https://api.live.bilibili.com/api/sendmsg?'
        # page ??
        time = CurrentTime()
        list_url = ["access_key=" + self.dic_bilibili['access_key'], "appkey=" + self.dic_bilibili['appkey'], 'aid=',
                    'page=1', "build=" + self.dic_bilibili['build']]
        sign = self.calc_sign('&'.join(sorted(list_url)))

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

        response = self.bili_section.post(url, headers=self.dic_bilibili['appheaders'], data=data)
        return response

    def request_send_danmu_msg_web(self, msg, roomId):
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

        response = self.bili_section.post(url, headers=self.dic_bilibili['pcheaders'], data=data)
        return response


    def request_fetchmedal(self):
        url = 'https://api.live.bilibili.com/i/api/medal?page=1&pageSize=50'
        response = self.bili_section.post(url, headers=self.dic_bilibili['pcheaders'])
        return response
        
    def request_getkey(self):
        url = 'https://passport.bilibili.com/api/oauth2/getKey'
        temp_params = 'appkey=' + self.dic_bilibili['appkey']
        sign = self.calc_sign(temp_params)
        params = {'appkey': self.dic_bilibili['appkey'], 'sign': sign}
        response = requests.post(url, data=params)
        return response
        
        
        
    def normal_login(self, username, password):
        # url = 'https://passport.bilibili.com/api/oauth2/login'   //旧接口
        url = "https://passport.bilibili.com/api/v2/oauth2/login"
        temp_params = 'appkey=' + self.dic_bilibili['appkey'] + '&password=' + password + '&username=' + username
        sign = self.calc_sign(temp_params)
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = "appkey=" + self.dic_bilibili[
            'appkey'] + "&password=" + password + "&username=" + username + "&sign=" + sign
        response = requests.post(url, data=payload, headers=headers)
        return response
        
    def login_with_captcha(self, username, password):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Host': 'passport.bilibili.com',
            'cookie':"sid=hxt5szbb"
        }
        s = requests.session()
        url = "https://passport.bilibili.com/captcha"
        res = s.get(url,headers=headers)
        tmp1 = base64.b64encode(res.content)
        
        captcha = cnn_captcha(tmp1)
        temp_params = 'actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&captcha='+captcha+'&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili['mobi_app'] + '&password='+ password +'&platform=' + self.dic_bilibili[
                          'platform'] +'&username='+username
        sign = self.calc_sign(temp_params)
        payload = temp_params + '&sign=' + sign
        headers['Content-type'] = "application/x-www-form-urlencoded"
        headers['cookie'] = "sid=hxt5szbb"
        url = "https://passport.bilibili.com/api/v2/oauth2/login"
        response = s.post(url,data=payload,headers=headers)
        return response
        
    
    def login(self):
        username = str(self.dic_bilibili['account']['username'])
        password = str(self.dic_bilibili['account']['password'])

        if username != "":
            response = self.request_getkey()
            value = response.json()['data']
            key = value['key']
            Hash = str(value['hash'])
            username, password = calc_name_passw(key, Hash, username, password)
            
            response = self.normal_login(username, password)
            while response.json()['code'] == -105:
                
                response = self.login_with_captcha(username, password)
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
                self.dic_bilibili['pcheaders']['cookie'] = cookie_format
                self.dic_bilibili['appheaders']['cookie'] = cookie_format     
                return True, None           
                
            except:
                return False, response.json()['message']


    def get_gift_of_storm(self, dic):
        roomid = dic['roomid']
        get_url = "https://api.live.bilibili.com/lottery/v1/Storm/check?roomid=" + str(roomid)
        response = self.bili_section.get(get_url, headers=self.dic_bilibili['pcheaders'])
        temp = response.json()
        check = len(temp['data'])
        if check != 0 and temp['data']['hasJoin'] != 1:
            id = temp['data']['id']
            storm_url = 'https://api.live.bilibili.com/lottery/v1/Storm/join'
            payload = {
                "id": id,
                "color": "16777215",
                "captcha_token": "",
                "captcha_phrase": "",
                "token": "",
                "csrf_token": self.dic_bilibili['csrf']}
            response1 = self.bili_section.post(storm_url, data=payload, headers=self.dic_bilibili['pcheaders'], timeout=2)
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
        sign = self.calc_sign(temp_params)
        true_url = 'https://api.live.bilibili.com/YunYing/roomEvent?' + temp_params + '&sign=' + sign
        pc_url = 'https://api.live.bilibili.com/activity/v1/Raffle/join?roomid=' + str(
            text1) + '&raffleId=' + str(raffleid)
        response1 = self.bili_section.get(true_url, params=params, headers=headers)
        pc_response = self.bili_section.get(pc_url, headers=headers)

        return response1, pc_response

    def get_gift_of_TV(self, real_roomid, raffleid):
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&id=' + str(
            raffleid) + '&mobi_app=' + self.dic_bilibili['mobi_app'] + '&platform=' + self.dic_bilibili[
                          'platform'] + '&roomid=' + str(
            real_roomid) + '&ts=' + CurrentTime()
        sign = self.calc_sign(temp_params)
        true_url = 'https://api.live.bilibili.com/AppSmallTV/join?' + temp_params + '&sign=' + sign
        response2 = self.bili_section.get(true_url, headers=self.dic_bilibili['appheaders'])
        return response2

    def get_gift_of_captain(self, roomid, id):
        join_url = "https://api.live.bilibili.com/lottery/v1/lottery/join"
        payload = {"roomid": roomid, "id": id, "type": "guard", "csrf_token": self.dic_bilibili['csrf']}
        response2 = self.bili_section.post(join_url, data=payload, headers=self.dic_bilibili['pcheaders'])
        return response2

    def get_giftlist_of_events(self, text1):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'Host': 'api.live.bilibili.com',
        }
        url = 'https://api.live.bilibili.com/activity/v1/Raffle/check?roomid=' + str(text1)
        response = self.bili_section.get(url, headers=headers)

        return response

    def get_giftlist_of_TV(self, real_roomid):
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + \
                      '&mobi_app=' + self.dic_bilibili['mobi_app'] + '&platform=' + self.dic_bilibili[
                          'platform'] + '&roomid=' + str(
            real_roomid) + '&ts=' + CurrentTime()
        sign = self.calc_sign(temp_params)
        check_url = 'https://api.live.bilibili.com/AppSmallTV/index?' + temp_params + '&sign=' + sign
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        }
        response = self.bili_section.get(check_url, headers=headers)

        return response

    def get_giftlist_of_captain(self, roomid):
        true_url = 'https://api.live.bilibili.com/lottery/v1/lottery/check?roomid=' + str(roomid)
        headers = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q = 0.8",
        "Accept-Encoding":"gzip,deflate,br",
        "Accept-Language":"zh-CN",
        "DNT": "1",
        "Cookie":"LIVE_BUVID=AUTO7715232653604550",
        "Connection":"keep-alive",
        "Cache-Control":"max-age =0",
        "Host":"api.live.bilibili.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent":'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:59.0) Gecko/20100101 Firefox/59.0'
        }
        response1 = self.bili_section.get(true_url,headers=headers)
        return response1



    def get_giftids_raffle(self, str):
        return self.dic_bilibili['giftids_raffle'][str]

    def get_giftids_raffle_keys(self):
        return self.dic_bilibili['giftids_raffle'].keys()

    def get_activity_result(self, activity_roomid, activity_raffleid):
        url = "https://api.live.bilibili.com/activity/v1/Raffle/notice?roomid=" + str(
            activity_roomid) + "&raffleId=" + str(activity_raffleid)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'Host': 'api.live.bilibili.com',
            'cookie': self.dic_bilibili['cookie'],
        }
        response = self.bili_section.get(url, headers=headers)
        return response

    def get_TV_result(self, TV_roomid, TV_raffleid):
        url = "https://api.live.bilibili.com/gift/v2/smalltv/notice?roomid=" + str(TV_roomid) + "&raffleId=" + str(
            TV_raffleid)
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'Host': 'api.live.bilibili.com',
            'cookie': self.dic_bilibili['cookie'],
        }
        response = self.bili_section.get(url, headers=headers)
        return response

    def pcpost_heartbeat(self):
        url = 'https://api.live.bilibili.com/User/userOnlineHeart'
        response = self.bili_section.post(url, headers=self.dic_bilibili['pcheaders'])
        return response

    # 发送app心跳包
    def apppost_heartbeat(self):
        time = CurrentTime()
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili[
                          'mobi_app'] + '&platform=' + self.dic_bilibili['platform'] + '&ts=' + time
        sign = self.calc_sign(temp_params)
        url = 'https://api.live.bilibili.com/mobile/userOnlineHeart?' + temp_params + '&sign=' + sign
        payload = {'roomid': 23058, 'scale': 'xhdpi'}
        response = self.bili_section.post(url, data=payload, headers=self.dic_bilibili['appheaders'])
        return response

    # 心跳礼物
    def heart_gift(self):
        url = "https://api.live.bilibili.com/gift/v2/live/heart_gift_receive?roomid=3&area_v2_id=34"
        response = self.bili_section.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def get_lotterylist(self, i):
        url = "https://api.live.bilibili.com/lottery/v1/box/getStatus?aid=" + str(i)
        response = self.bili_section.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def get_gift_of_lottery(self, i, g):
        url1 = 'https://api.live.bilibili.com/lottery/v1/box/draw?aid=' + str(i) + '&number=' + str(g + 1)
        response1 = self.bili_section.get(url1, headers=self.dic_bilibili['pcheaders'])
        return response1

    def get_time_about_silver(self):
        time = CurrentTime()
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili[
                          'mobi_app'] + '&platform=' + self.dic_bilibili['platform'] + '&ts=' + time
        sign = self.calc_sign(temp_params)
        GetTask_url = 'https://api.live.bilibili.com/mobile/freeSilverCurrentTask?' + temp_params + '&sign=' + sign
        response = self.bili_section.get(GetTask_url, headers=self.dic_bilibili['appheaders'])
        return response

    def get_silver(self, timestart, timeend):
        time = CurrentTime()
        temp_params = 'access_key=' + self.dic_bilibili['access_key'] + '&actionKey=' + self.dic_bilibili[
            'actionKey'] + '&appkey=' + self.dic_bilibili['appkey'] + '&build=' + self.dic_bilibili[
                          'build'] + '&device=' + self.dic_bilibili['device'] + '&mobi_app=' + self.dic_bilibili[
                          'mobi_app'] + '&platform=' + self.dic_bilibili[
                          'platform'] + '&time_end=' + timeend + '&time_start=' + timestart + '&ts=' + time
        sign = self.calc_sign(temp_params)
        url = 'https://api.live.bilibili.com/mobile/freeSilverAward?' + temp_params + '&sign=' + sign
        response = self.bili_section.get(url, headers=self.dic_bilibili['appheaders'])
        return response

    def get_dailybag(self):
        url = 'https://api.live.bilibili.com/gift/v2/live/receive_daily_bag'
        response = self.bili_section.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def get_dosign(self):
        url = 'https://api.live.bilibili.com/sign/doSign'
        response = self.bili_section.get(url, headers=self.dic_bilibili['pcheaders'])
        return response

    def get_dailytask(self):
        url = 'https://api.live.bilibili.com/activity/v1/task/receive_award'
        payload2 = {'task_id': 'double_watch_task'}
        response2 = self.bili_section.post(url, data=payload2, headers=self.dic_bilibili['appheaders'])
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
        sign = self.calc_sign(temp_params)
        url = "https://api.vc.bilibili.com/link_setting/v1/link_setting/sign_in?" + temp_params + "&sign=" + sign
        appheaders = self.dic_bilibili['appheaders'].copy()
        appheaders['Host'] = "api.vc.bilibili.com"
        response = requests.get(url, headers=appheaders)
        return response


