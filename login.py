from bilibili import bilibili
from printer import Printer
import base64
import configloader
import requests
import time


# temporary app parameter
# appkey = '4409e2ce8ffd12b8'
# build = '101800'
# device = 'android_tv_yst'
# mobi_app = 'android_tv_yst'
# app_secret = '59b43e04ad6965f34319062b478f83dd'

app_headers = {
    "User-Agent": "Mozilla/5.0 BiliDroid/5.58.0 (bbcallen@gmail.com)",
    "Accept-encoding": "gzip",
    "Buvid": "XZ11bfe2654a9a42d885520a680b3574582eb3",
    "Display-ID": "146771405-1521008435",
    "Device-Guid": "2d0bbec5-df49-43c5-8a27-ceba3f74ffd7",
    "Device-Id": "469a6aaf431b46f8b58a1d4a91d0d95b202004211125026456adffe85ddcb44818",
    "Accept-Language": "zh-CN",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Connection": "keep-alive",
    'cookie': ''
}

class login():
    auto_captcha_times = 3

    def normal_login(self, username, password):
        # url = 'https://passport.bilibili.com/api/oauth2/login'   //旧接口
        # url = "https://passport.bilibili.com/api/v2/oauth2/login"
        url = "https://passport.bilibili.com/api/v3/oauth2/login"
        params_dic = {
            "actionKey": bilibili().dic_bilibili["actionKey"],
            "appkey": bilibili().dic_bilibili["appkey"],
            "build": bilibili().dic_bilibili["build"],
            "captcha": '',
            "device": bilibili().dic_bilibili["device"],
            "mobi_app": bilibili().dic_bilibili["mobi_app"],
            "password": password,
            "platform": bilibili().dic_bilibili["platform"],
            "username": username
        }
        temp_params = '&'.join([f'{key}={value}' for key, value in params_dic.items()])
        sign = bilibili().calc_sign(temp_params)
        # headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = f'{temp_params}&sign={sign}'
        response = requests.post(url, params=payload, headers=app_headers)
        return response

    def login_with_captcha(self, username, password):
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'cookie': "sid=hxt5szbb"
        }
        s = requests.session()
        url = "https://passport.bilibili.com/captcha"
        res = s.get(url, headers=headers)
        tmp1 = base64.b64encode(res.content)
        for _ in range(login.auto_captcha_times):
            try:
                captcha = bilibili().cnn_captcha(tmp1)
                break
            except Exception:
                Printer().printer("验证码识别服务器连接失败", "Error", "red")
                login.auto_captcha_times -= 1
        else:
            try:
                from PIL import Image
                from io import BytesIO
                img = Image.open(BytesIO(res.content))
                img.show()
                captcha = input('输入验证码\n').strip()
            except ImportError:
                Printer().printer("安装 Pillow 库后重启，以弹出验证码图片", "Error", "red")
                exit()

        params_dic = {
            "actionKey": bilibili().dic_bilibili["actionKey"],
            "appkey": bilibili().dic_bilibili["appkey"],
            "build": bilibili().dic_bilibili["build"],
            "captcha": captcha,
            "device": bilibili().dic_bilibili["device"],
            "mobi_app": bilibili().dic_bilibili["mobi_app"],
            "password": password,
            "platform": bilibili().dic_bilibili["platform"],
            "username": username
        }
        temp_params = '&'.join([f'{key}={value}' for key, value in params_dic.items()])
        sign = bilibili().calc_sign(temp_params)
        payload = f'{temp_params}&sign={sign}'
        headers = app_headers.copy()
        headers['cookie'] = "sid=hxt5szbb"
        url = "https://passport.bilibili.com/api/v3/oauth2/login"
        response = s.post(url, params=payload, headers=headers)
        return response

    # def access_token_2_cookies(self, access_token):
    #     params = f"access_key={access_token}&appkey={appkey}&gourl=https%3A%2F%2Faccount.bilibili.com%2Faccount%2Fhome"
    #     url = f"https://passport.bilibili.com/api/login/sso?{params}&sign={bilibili().calc_sign(params, app_secret)}"
    #     response = requests.get(url, allow_redirects=False)
    #     return response.cookies.get_dict(domain=".bilibili.com")

    def login(self):
        username = str(bilibili().dic_bilibili['account']['username'])
        password = str(bilibili().dic_bilibili['account']['password'])
        if username != "":
            while True:
                response = bilibili().request_getkey()
                value = response.json()['data']
                key = value['key']
                Hash = str(value['hash'])
                calcd_username, calcd_password = bilibili().calc_name_passw(key, Hash, username, password)
                response = self.normal_login(calcd_username, calcd_password)
                while response.json()['code'] == -105:
                    response = self.login_with_captcha(calcd_username, calcd_password)
                if response.json()['code'] == -662:  # "can't decrypt rsa password~"
                    Printer().printer("打码时间太长key失效，重试", "Error", "red")
                    continue
                if response.json()['code'] == -449:
                    # {'code': -449, 'message': '服务繁忙, 请稍后再试', 'ts': 1593853665}
                    Printer().printer("服务繁忙，10分钟后重试", "Error", "red")
                    Printer().printer(f"疑似登录接口失效，请联系开发者 {response.json()}", "Warning", "red")
                    time.sleep(600)
                    continue
                break
            try:
                access_key = response.json()['data']['token_info']['access_token']
                refresh_token = response.json()['data']['token_info']['refresh_token']
                cookie = response.json()['data']['cookie_info']['cookies']
                cookie_format = ""
                for i in range(len(cookie)):
                    cookie_format = cookie_format + cookie[i]['name'] + "=" + cookie[i]['value'] + ";"
                bilibili().dic_bilibili['csrf'] = cookie[0]['value']
                bilibili().dic_bilibili['access_key'] = access_key
                bilibili().dic_bilibili['refresh_token'] = refresh_token
                bilibili().dic_bilibili['cookie'] = cookie_format
                bilibili().dic_bilibili['uid'] = cookie[1]['value']
                bilibili().dic_bilibili['pcheaders']['cookie'] = cookie_format
                bilibili().dic_bilibili['appheaders']['cookie'] = cookie_format
                dic_saved_session = {
                    'csrf': cookie[0]['value'],
                    'access_key': access_key,
                    'refresh_token': refresh_token,
                    'cookie': cookie_format,
                    'uid': cookie[1]['value']
                }
                configloader.write2bilibili(dic_saved_session)
                Printer().printer(f"登录成功", "Info", "green")
            except:
                Printer().printer(f"登录失败,错误信息为:{response.json()}", "Error", "red")

    async def login_new(self):
        if bilibili().dic_bilibili['saved-session']['cookie']:
            Printer().printer(f"复用cookie", "Info", "green")
            bilibili().load_session(bilibili().dic_bilibili['saved-session'])
        else:
            return self.login()

    def refresh_token(self):
        url = "https://passport.bilibili.com/api/v2/oauth2/refresh_token"
        params_dic = {
            "access_token": bilibili().dic_bilibili["access_key"],
            "actionKey": bilibili().dic_bilibili["actionKey"],
            "appkey": bilibili().dic_bilibili["appkey"],
            "build": bilibili().dic_bilibili["build"],
            "device": bilibili().dic_bilibili["device"],
            "mobi_app": bilibili().dic_bilibili["mobi_app"],
            "platform": bilibili().dic_bilibili["platform"],
            'refresh_token': bilibili().dic_bilibili["refresh_token"],
        }
        temp_params = '&'.join([f'{key}={value}' for key, value in params_dic.items()])
        sign = bilibili().calc_sign(temp_params)
        payload = f'{temp_params}&sign={sign}'
        response = requests.post(url, params=payload, headers=app_headers)
        json_response = response.json()
        if json_response["code"] == 0:
            access_key = json_response['data']['token_info']['access_token']
            refresh_token = json_response['data']['token_info']['refresh_token']
            cookie = json_response['data']['cookie_info']['cookies']
            cookie_format = ""
            for i in range(len(cookie)):
                cookie_format = cookie_format + cookie[i]['name'] + "=" + cookie[i]['value'] + ";"
            bilibili().dic_bilibili['csrf'] = cookie[0]['value']
            bilibili().dic_bilibili['access_key'] = access_key
            bilibili().dic_bilibili['refresh_token'] = refresh_token
            bilibili().dic_bilibili['cookie'] = cookie_format
            bilibili().dic_bilibili['uid'] = cookie[1]['value']
            bilibili().dic_bilibili['pcheaders']['cookie'] = cookie_format
            bilibili().dic_bilibili['appheaders']['cookie'] = cookie_format
            dic_saved_session = {
                'csrf': cookie[0]['value'],
                'access_key': access_key,
                'refresh_token': refresh_token,
                'cookie': cookie_format,
                'uid': cookie[1]['value']
            }
            configloader.write2bilibili(dic_saved_session)
            Printer().printer(f"token刷新成功", "Info", "green")
        else:
            Printer().printer(f"token刷新失败，将重新登录 {json_response}", "Info", "green")
            self.login()
