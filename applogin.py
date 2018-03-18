#!/usr/bin/python
# coding:utf-8
import base64
import requests
import rsa
import hashlib
from urllib import parse

appkey = '1d8b6e7d45233436'
app_secret = '560c52ccd288fed045859ed18bffd973'


def GetHash():
    url = 'https://passport.bilibili.com/api/oauth2/getKey'
    temp_params = 'appkey=' + appkey + app_secret
    hash = hashlib.md5()
    hash.update(temp_params.encode('utf-8'))
    sign = hash.hexdigest()
    params = {'appkey': appkey, 'sign': sign}
    response = requests.post(url, data=params)
    value = response.json()['data']
    return value


def Login():
    username = input("输入用户名:")
    password = input("输入密码:")
    key = GetHash()['key']
    Hash = str(GetHash()['hash'])
    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(key.encode())
    password = base64.b64encode(rsa.encrypt((Hash + password).encode('utf-8'), pubkey))
    password = parse.quote_plus(password)
    # url = 'https://passport.bilibili.com/api/oauth2/login'   //旧接口
    url = "https://passport.bilibili.com/api/v2/oauth2/login"
    temp_params = 'appkey=' + appkey + '&password=' + password + '&username=' + username
    params = temp_params + app_secret
    hash = hashlib.md5()
    hash.update(params.encode('utf-8'))
    sign = hash.hexdigest()
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    payload = "appkey=" + appkey + "&password=" + password + "&username=" + username + "&sign=" + sign
    response = requests.post(url, data=payload, headers=headers)
    print(response.json())
    print("access_key为：", response.json()['data']['token_info']['access_token'])
    cookie = (response.json()['data']['cookie_info']['cookies'])
    cookie_format = ""
    for i in range(0, len(cookie)):
        cookie_format = cookie_format + cookie[i]['name'] + "=" + cookie[i]['value'] + ";"
    print("Cookie为：", cookie_format)


Login()
