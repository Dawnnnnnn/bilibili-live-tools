import datetime
from bilibili import bilibili
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
            cls.instance.joined_event = []
            cls.instance.joined_TV = []
            # cls.instance.TVsleeptime = 185
            # cls.instance.activitysleeptime = 125
        return cls.instance

    def getlist(self):
        # print(self.joined_event)
        # print(self.joined_TV)
        print('本次参与活动抽奖次数:', len(self.joined_event))
        print('本次参与电视抽奖次数:', len(self.joined_TV))

    def delete_0st_activitylist(self):
        del self.activity_roomid_list[0]
        del self.activity_raffleid_list[0]
        # del self.activity_time_list[0]

    def delete_0st_TVlist(self):
        del self.TV_roomid_list[0]
        del self.TV_raffleid_list[0]
        # del self.TV_time_list[0]

    def clean_activity(self):
        # print(self.activity_raffleid_list)
        if self.activity_raffleid_list:
            for i in range(0, len(self.activity_roomid_list)):
                response = bilibili().get_activity_result(self.activity_roomid_list[0], self.activity_raffleid_list[0])
                json_response = response.json()
                # print(json_response)
                if json_response['code'] == 0:
                    data = json_response['data']
                    print("# 房间", str(self.activity_roomid_list[0]).center(9), "网页端活动抽奖结果:",
                          data['gift_name'] + "x" + str(data['gift_num']))

                    self.delete_0st_activitylist()

                elif json_response['code'] == -400:
                    # sleepseconds = self.activitysleeptime + self.activity_time_list[0] - int(CurrentTime())+ 2
                    # sleepseconds = self.activity_time_list[0] - int(CurrentTime())
                    # return sleepsecondsq
                    return

                else:
                    print('未知情况')
                    print(json_response)

        else:
            return

    def clean_TV(self):
        # print(self.TV_raffleid_list)
        if self.TV_raffleid_list:
            for i in range(0, len(self.TV_roomid_list)):

                response = bilibili().get_TV_result(self.TV_roomid_list[0], self.TV_raffleid_list[0])
                # if response.json()['data']['gift_name'] != "":
                json_response = response.json()
                # print(json_response)
                if json_response['data']['gift_id'] == '-1':
                    return
                elif json_response['data']['gift_id'] != '-1':

                    data = json_response['data']
                    print("# 房间", str(self.TV_roomid_list[0]).center(9), "小电视道具抽奖结果:",
                          data['gift_name'] + "x" + str(data['gift_num']))

                    self.delete_0st_TVlist()
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

    def check_TVlist(self, raffleid):
        if raffleid not in self.TV_raffleid_list:
            return True
        return False

    def check_activitylist(self, raffleid):
        if raffleid not in self.activity_raffleid_list:
            return True
        return False