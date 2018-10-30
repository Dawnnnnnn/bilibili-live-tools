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
            cls.instance.TV_raffleid_list = []
            cls.instance.TV_roomid_list = []

            cls.instance.pushed_event = []
            cls.instance.pushed_TV = []

            cls.instance.joined_event = []
            cls.instance.joined_TV = []
            cls.instance.result = {}

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

    def delete_0st_TVlist(self):
        del self.TV_roomid_list[0]
        del self.TV_raffleid_list[0]

    async def clean_TV(self):
        printlist = []

        if self.TV_raffleid_list:
            for i in range(0, len(self.TV_roomid_list)):

                response = await  bilibili().get_TV_result(self.TV_roomid_list[0], self.TV_raffleid_list[0])
                json_response = await response.json()
                try:

                    if json_response['data']['gift_id'] == '-1':
                        return
                    elif json_response['data']['gift_id'] != '-1':
                        data = json_response['data']
                        Printer().printer(f"房间 {self.TV_roomid_list[0]} 广播道具抽奖结果: {data['gift_name']}X{data['gift_num']}",
                                          "Lottery", "cyan")
                        self.add_to_result(data['gift_name'], int(data['gift_num']))

                        self.delete_0st_TVlist()
                except:
                    print(json_response)

        else:
            return

    def append_to_TVlist(self, raffleid, real_roomid, time=''):
        self.TV_raffleid_list.append(raffleid)
        self.TV_roomid_list.append(real_roomid)
        self.joined_TV.append(decimal_time())

    def append2pushed_TVlist(self):
        self.pushed_TV.append(decimal_time())

    def check_TVlist(self, raffleid):
        if raffleid not in self.TV_raffleid_list:
            return True
        return False
