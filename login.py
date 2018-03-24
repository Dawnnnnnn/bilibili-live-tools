import requests
import hashlib
import rsa
import base64
from urllib import parse
from bilibili import bilibili
import time


class Login(bilibili):

    def GetHash(self):
        url = 'https://passport.bilibili.com/api/oauth2/getKey'
        temp_params = 'appkey=' + self.appkey + self.app_secret
        hash = hashlib.md5()
        hash.update(temp_params.encode('utf-8'))
        sign = hash.hexdigest()
        params = {'appkey': self.appkey, 'sign': sign}
        response = requests.post(url, data=params)
        value = response.json()['data']
        return value

    def success(self):
        username = input("输入用户名:")
        password = input("输入密码:")
        value = self.GetHash()
        key = value['key']
        Hash = str(value['hash'])
        pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode())
        password = base64.b64encode(rsa.encrypt((Hash + password).encode('utf-8'), pubkey))
        password = parse.quote_plus(password)
        username = parse.quote_plus(username)
        # url = 'https://passport.bilibili.com/api/oauth2/login'   //旧接口
        url = "https://passport.bilibili.com/api/v2/oauth2/login"
        temp_params = 'appkey=' + self.appkey + '&password=' + password + '&username=' + username
        params = temp_params + self.app_secret
        hash = hashlib.md5()
        hash.update(params.encode('utf-8'))
        sign = hash.hexdigest()
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        payload = "appkey=" + self.appkey + "&password=" + password + "&username=" + username + "&sign=" + sign
        response = requests.post(url, data=payload, headers=headers)
        access_key = response.json()['data']['token_info']['access_token']
        cookie = (response.json()['data']['cookie_info']['cookies'])
        cookie_format = ""
        for i in range(0, len(cookie)):
            cookie_format = cookie_format + cookie[i]['name'] + "=" + cookie[i]['value'] + ";"

        bilibili.access_key = access_key
        bilibili.cookie = cookie_format
        bilibili.pcheaders = {
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'accept-encoding': 'gzip, deflate',
            'Host': 'api.live.bilibili.com',
            'cookie': cookie_format
        }
        bilibili.appheaders = {
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
        #return access_key, cookie_format

