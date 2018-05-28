import datetime
from bilibili import bilibili
from printer import Printer


# 13:30  --->  13.5
def decimal_time():
    now = datetime.datetime.now()
    return now.hour + now.minute / 60.0


class Statistics:
    instance = None

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(Statistics, cls).__new__(cls, *args, **kw)
            cls.instance.activity_raffleid_list = []
            cls.instance.activity_roomid_list = []
            # cls.instance.activity_time_list = []
            cls.instance.TV_raffleid_list = []
            cls.instance.TV_roomid_list = []

            # cls.instance.TV_time_list = []

            cls.instance.pushed_event = []
            cls.instance.pushed_TV = []

            cls.instance.joined_event = []
            cls.instance.joined_TV = []
            cls.instance.result = {}
            # cls.instance.TVsleeptime = 185
            # cls.instance.activitysleeptime = 125
        return cls.instance

    def add_to_result(self, type, num):
        self.result[type] = self.result.get(type, 0) + int(num)

    def getlist(self):
        # print(self.joined_event)
        # print(self.joined_TV)
        print('本次推送活动抽奖次数:', len(self.pushed_event))
        print('本次推送电视抽奖次数:', len(self.pushed_TV))
        print()
        print('本次参与活动抽奖次数:', len(self.joined_event))
        print('本次参与电视抽奖次数:', len(self.joined_TV))

    def getresult(self):
        print('本次参与抽奖结果为：')
        for k, v in self.result.items():
            print('{}X{}'.format(k, v))

    def delete_0st_activitylist(self):
        del self.activity_roomid_list[0]
        del self.activity_raffleid_list[0]
        # del self.activity_time_list[0]

    def delete_0st_TVlist(self):
        del self.TV_roomid_list[0]
        del self.TV_raffleid_list[0]
        # del self.TV_time_list[0]

    async def clean_activity(self):
        # print(self.activity_raffleid_list)
        if self.activity_raffleid_list:
            for i in range(0, len(self.activity_roomid_list)):
                response = await bilibili().get_activity_result(self.activity_roomid_list[0],
                                                                self.activity_raffleid_list[0])
                json_response = await response.json()
                # print(json_response)
                try:
                    if json_response['code'] == 0:
                        data = json_response['data']
                        Printer().printlist_append(['join_lottery', '', 'user',
                                                    "房间{:^9}网页端活动抽奖结果: {}X{}".format(self.activity_roomid_list[0],
                                                                                     data['gift_name'],
                                                                                     data['gift_num'])], True)
                        self.add_to_result(data['gift_name'], int(data['gift_num']))

                        self.delete_0st_activitylist()
                    # {'code': -400, 'msg': '尚未开奖，请耐心等待！', 'message': '尚未开奖，请耐心等待！', 'data': []}
                    elif json_response['code'] == -400:
                        # sleepseconds = self.activitysleeptime + self.activity_time_list[0] - int(CurrentTime())+ 2
                        # sleepseconds = self.activity_time_list[0] - int(CurrentTime())
                        # return sleepsecondsq
                        return

                    else:
                        print('未知情况')
                        print(json_response)
                except:
                    print(json_response)

        else:
            return

    async def clean_TV(self):
        printlist = []
        # print(self.TV_raffleid_list)
        if self.TV_raffleid_list:
            for i in range(0, len(self.TV_roomid_list)):

                response = await  bilibili().get_TV_result(self.TV_roomid_list[0], self.TV_raffleid_list[0])
                # if response.json()['data']['gift_name'] != "":
                json_response = await response.json()
                # print(json_response)
                try:
                    # {'code': 0, 'msg': '正在抽奖中..', 'message': '正在抽奖中..', 'data': {'gift_id': '-1', 'gift_name': '', 'gift_num': 0, 'gift_from': '', 'gift_type': 0, 'gift_content': '', 'status': 3}}

                    if json_response['data']['gift_id'] == '-1':
                        return
                    elif json_response['data']['gift_id'] != '-1':
                        data = json_response['data']
                        Printer().printlist_append(['join_lottery', '', 'user',
                                                    "房间{:^9}广播道具抽奖结果: {}X{}".format(self.TV_roomid_list[0],
                                                                                     data['gift_name'],
                                                                                     data['gift_num'])], True)
                        self.add_to_result(data['gift_name'], int(data['gift_num']))

                        self.delete_0st_TVlist()
                except:
                    print(json_response)
            # else:
            # print(int(CurrentTime()))
            # sleepseconds = self.TV_time_list[0] - int(CurrentTime()) + 1
            # sleepseconds = self.TV_time_list[0] - int(CurrentTime())
            # return

            #  else:
            # print('未知')
        else:
            return

    def append_to_activitylist(self, raffleid, text1, time=''):
        self.activity_raffleid_list.append(raffleid)
        self.activity_roomid_list.append(text1)
        # self.activity_time_list.append(int(time))
        # self.activity_time_list.append(int(CurrentTime()))
        self.joined_event.append(decimal_time())
        # print("activity加入成功", self.joined_event)

    def append_to_TVlist(self, raffleid, real_roomid, time=''):
        self.TV_raffleid_list.append(raffleid)
        self.TV_roomid_list.append(real_roomid)
        # self.TV_time_list.append(int(time)+int(CurrentTime()))
        # self.TV_time_list.append(int(CurrentTime()))
        self.joined_TV.append(decimal_time())
        # print("tv加入成功", self.joined_TV)

    def append2pushed_activitylist(self):
        self.pushed_event.append(decimal_time())

    def append2pushed_TVlist(self):
        self.pushed_TV.append(decimal_time())




    def check_TVlist(self, raffleid):
        if raffleid not in self.TV_raffleid_list:
            return True
        return False

    def check_activitylist(self, raffleid):
        if raffleid not in self.activity_raffleid_list:
            return True
        return False

