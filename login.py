from bilibili import bilibili
from printer import Printer
import base64
import configloader
import requests


class login():
    auto_captcha_times = 3

    def normal_login(self, username, password):
        # url = 'https://passport.bilibili.com/api/oauth2/login'   //旧接口
        url = "https://passport.snm0516.aisee.tv/api/tv/login"
        temp_params = f"appkey={bilibili().dic_bilibili['appkey']}&build={bilibili().dic_bilibili['build']}&captcha=&channel=master&guid=XYEBAA3E54D502E37BD606F0589A356902FCF&mobi_app=android_tv_yst&password={password}&platform=android&token=5598158bcd8511e2&ts=0&username={username}"
        data = f"{temp_params}&sign={bilibili().calc_sign(temp_params)}"
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        response = requests.post(url, data=data, headers=headers)
        return response

    def login_with_captcha(self, username, password):
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Host': 'passport.bilibili.com',
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

        temp_params = f"appkey={bilibili().dic_bilibili['appkey']}&build={bilibili().dic_bilibili['build']}&captcha={captcha}&channel=master&guid=XYEBAA3E54D502E37BD606F0589A356902FCF&mobi_app=android_tv_yst&password={password}&platform=android&token=5598158bcd8511e2&ts=0&username={username}"
        data = f"{temp_params}&sign={bilibili().calc_sign(temp_params)}"
        headers['Content-type'] = "application/x-www-form-urlencoded"
        headers['cookie'] = "sid=hxt5szbb"
        url = "https://passport.snm0516.aisee.tv/api/tv/login"
        response = s.post(url, data=data, headers=headers)
        return response

    def access_token_2_cookies(self, access_token):
        params = f"access_key={access_token}&appkey={bilibili().dic_bilibili['appkey']}&gourl=https%3A%2F%2Faccount.bilibili.com%2Faccount%2Fhome"
        url = f"https://passport.bilibili.com/api/login/sso?{params}&sign={bilibili().calc_sign(params)}"
        response = requests.get(url, allow_redirects=False)
        return response.cookies.get_dict(domain=".bilibili.com")

    def login(self):
        username = str(bilibili().dic_bilibili['account']['username'])
        password = str(bilibili().dic_bilibili['account']['password'])
        if username != "":
            while True:
                response = bilibili().request_getkey()
                value = response.json()['data']
                key = value['key']
                Hash = str(value['hash'])
                username, password = bilibili().calc_name_passw(key, Hash, username, password)
                response = self.normal_login(username, password)
                while response.json()['code'] == -105:
                    response = self.login_with_captcha(username, password)
                if response.json()['code'] == -662:  # "can't decrypt rsa password~"
                    Printer().printer("打码时间太长key失效，重试", "Error", "red")
                    continue
                break
            try:
                access_key = response.json()['data']['token_info']['access_token']
                cookie_info = self.access_token_2_cookies(access_key)
                cookie_format = ""
                for key, value in cookie_info.items():
                    cookie_format = cookie_format + key + "=" + value + ";"
                bilibili().dic_bilibili['csrf'] = cookie_info['bili_jct']
                bilibili().dic_bilibili['access_key'] = access_key
                bilibili().dic_bilibili['cookie'] = cookie_format
                bilibili().dic_bilibili['uid'] = cookie_info['DedeUserID']
                bilibili().dic_bilibili['pcheaders']['cookie'] = cookie_format
                bilibili().dic_bilibili['appheaders']['cookie'] = cookie_format
                dic_saved_session = {
                    'csrf': cookie_info['bili_jct'],
                    'access_key': access_key,
                    'cookie': cookie_format,
                    'uid': cookie_info['DedeUserID']
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
