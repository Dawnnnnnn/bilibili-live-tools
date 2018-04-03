from bilibili import bilibili
import requests
import asyncio
import time


class LotteryResult():
    
    def __init__(self, bilibili):
        self.bilibili =bilibili

    async def query(self):
        while 1:
            if self.bilibili.activity_raffleid_list:               
                for i in range(0,len(self.bilibili.activity_roomid_list)):
                    url = "http://api.live.bilibili.com/activity/v1/Raffle/notice?roomid="+str(self.bilibili.activity_roomid_list[0])+"&raffleId="+str(self.bilibili.activity_raffleid_list[0])
                    headers = {
                        'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'accept-encoding': 'gzip, deflate',
                        'Host': 'api.live.bilibili.com',
                        'cookie': self.bilibili.cookie,
                    }
                    response = requests.get(url, headers=headers)
                    try:
                        print("# 房间", str(self.bilibili.activity_roomid_list[0]).center(9), "网页端活动抽奖结果:", response.json()['data']['gift_name']+"x"+str(response.json()['data']['gift_num']))
                        del self.bilibili.activity_roomid_list[0]
                        del self.bilibili.activity_raffleid_list[0]
                        del self.bilibili.activity_time_list[0]
                    except:
                        pass

            # print(self.bilibili.TV_raffleid_list)
            if self.bilibili.TV_raffleid_list:
                for i in range(0, len(self.bilibili.TV_roomid_list)):
                    url="http://api.live.bilibili.com/gift/v2/smalltv/notice?roomid="+str(self.bilibili.TV_roomid_list[0])+"&raffleId="+str(self.bilibili.TV_raffleid_list[0])
                    headers = {
                        'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'accept-encoding': 'gzip, deflate',
                        'Host': 'api.live.bilibili.com',
                        'cookie': self.bilibili.cookie,
                    }
                    response = requests.get(url, headers=headers)
                    if response.json()['data']['gift_name'] != "":
                        try:
                            print("# 房间", str(self.bilibili.TV_roomid_list[0]).center(9), "小电视道具抽奖结果:", (response.json()['data']['gift_name'])+"x"+str(response.json()['data']['gift_num']))
                            del self.bilibili.TV_roomid_list[0]
                            del self.bilibili.TV_raffleid_list[0]
                            del self.bilibili.TV_time_list[0]
                        except:
                            pass
            await asyncio.sleep(60)
