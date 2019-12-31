#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/9 23:24
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com
import requests
url = "http://118.25.108.153:8080/guard"
headers = {
    "User-Agent": "bilibili-live-tools/" + "1234"
}
response = requests.get(url, headers=headers)
print(response.json())

# import json
#
# with open("Governors_Data.json", "r", encoding="utf-8")as f:
#     data = f.read()
#     data = json.loads(data)
#     print(data)
