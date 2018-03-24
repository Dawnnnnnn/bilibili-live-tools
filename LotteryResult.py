from bilibili import bilibili
import requests
import asyncio


class LotteryResult(bilibili):

    async def query(self):
        while 1:
            #print(self.activity_raffleid_list)
            if self.activity_raffleid_list != None:
                for i in range(0,len(self.activity_roomid_list)):
                    url = "http://api.live.bilibili.com/activity/v1/Raffle/notice?roomid="+str(self.activity_roomid_list[0])+"&raffleId="+str(self.activity_raffleid_list[0])
                    headers = {
                        'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'accept-encoding': 'gzip, deflate',
                        'Host': 'api.live.bilibili.com',
                        'cookie': self.cookie,
                    }
                    response = requests.get(url, headers=headers)
                    try:
                        print("房间 %-9s 网页端活动抽奖结果:" %(self.activity_roomid_list[0]),response.json()['data']['gift_name']+"x"+str(response.json()['data']['gift_num']))
                        del self.activity_roomid_list[0]
                        del self.activity_raffleid_list[0]
                        del self.activity_time_list[0]
                    except:
                        pass

            if self.TV_raffleid_list != None:
                for i in range(0, len(self.TV_roomid_list)):
                    url="http://api.live.bilibili.com/gift/v2/smalltv/notice?roomid="+str(self.TV_roomid_list[0])+"&raffleId="+str(self.TV_raffleid_list[0])
                    headers = {
                        'Accept': 'application/json, text/plain, */*',
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'accept-encoding': 'gzip, deflate',
                        'Host': 'api.live.bilibili.com',
                        'cookie': self.cookie,
                    }
                    response = requests.get(url, headers=headers)
                    if response.json()['data']['gift_name'] != "":
                        try:
                            print("房间 %-9s 小电视道具抽奖结果:" %(self.TV_roomid_list[0]),(response.json()['data']['gift_name'])+"x"+str(response.json()['data']['gift_num']))
                            del self.TV_roomid_list[0]
                            del self.TV_raffleid_list[0]
                            del self.TV_time_list[0]
                        except:
                            pass
            await asyncio.sleep(60)
