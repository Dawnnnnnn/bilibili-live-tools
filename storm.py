import requests
import time

cookies = ''
token = ''

tokenlist = [token]
cookielist = [cookies]


def storm():
    roomid = []
    try:
        for g in range(1, 11):
            url = 'http://api.live.bilibili.com/room/v1/room/get_user_recommend?page=' + str(g)
            response = requests.get(url, timeout=1)
            for i in range(0, 30):
                temp = response.json()['data'][i]['roomid']
                roomid.append(temp)
    except:
        pass
    try:
        for i in roomid:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                'cookie': cookies,
            }
            try:
                url = 'http://api.live.bilibili.com/lottery/v1/Storm/check?roomid=' + str(i)
                response = requests.get(url, headers=headers)
                temp = response.json()
                print(temp)
            except:
                pass
            check = len(temp['data'])
            if check != 0 and temp['data']['hasJoin'] != 1:
                id = temp['data']['id']
                roomid = temp['data']['roomid']
                for c in range(len(cookielist)):
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'cookie': cookielist[c],
                        'referer': 'http://live.bilibili.com/' + str(roomid)
                    }
                    storm_url = 'http://api.live.bilibili.com/lottery/v1/Storm/join'
                    payload = {"id": id, "color": "16772431", "captcha_token": "", "captcha_phrase": "", "token": "",
                               "csrf_token": tokenlist[c]}
                    response1 = requests.post(storm_url, data=payload, headers=headers, timeout=2)
                    print(response1.json())

    except:
        pass


while 1:
    storm()
