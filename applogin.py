#!/usr/bin/python
#coding:utf-8
import requests
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from base64 import b64encode
import hashlib
from urllib import parse

appkey = '1d8b6e7d45233436'
app_secret = '560c52ccd288fed045859ed18bffd973'


def GetHash():
    url = 'https://passport.bilibili.com/api/oauth2/getKey'
    temp_params = 'appkey='+appkey+app_secret
    hash = hashlib.md5()
    hash.update(temp_params.encode('utf-8'))
    sign = hash.hexdigest()
    params = {'appkey': appkey, 'sign': sign}
    response = requests.post(url, data=params)
    value = response.json()['data']
    return value



def Login():
    username = input("请输入用户名:")
    password = input("请输入密码:")
    key = GetHash()['key']
    Hash = str(GetHash()['hash'])
    encryptor = PKCS1_v1_5.new(RSA.importKey(bytes(key, 'utf-8')))
    password = str(b64encode(encryptor.encrypt(bytes(Hash+password, 'utf-8'))), 'utf-8')
    password = parse.quote_plus(password)
    url = 'https://passport.bilibili.com/api/oauth2/login'
    temp_params = 'appkey='+appkey+'&password='+password+'&username='+username
    params = temp_params + app_secret
    hash = hashlib.md5()
    hash.update(params.encode('utf-8'))
    sign = hash.hexdigest()
    headers = {"Content-type": "application/x-www-form-urlencoded"}
    payload = "appkey="+appkey+"&password="+password+"&username="+username+"&sign="+sign
    response = requests.post(url, data=payload, headers=headers)
    print(response.json())


Login()