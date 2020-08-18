import datetime
import asyncio
import traceback
import time
import utils
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
            cls.instance.init_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            cls.instance.activity_raffleid_list = []
            cls.instance.activity_roomid_list = []
            cls.instance.TV_raffleid_dict = {}
            # cls.instance.TV_roomid_list = []

            # cls.instance.pushed_event = []
            cls.instance.pushed_TV = []
            cls.instance.monitor = {}

            # cls.instance.joined_event = []
            cls.instance.joined_TV = []
            cls.instance.total_area = 1
            cls.instance.area_basis = 1
            cls.instance.result = {}

        return cls.instance

    def adjust_basis(self, area_list: [int]):
        self.total_area = len(area_list)
        self.area_basis = sum([2**(area_id-1) for area_id in area_list])

    def add_to_result(self, type, num):
        self.result[type] = self.result.get(type, 0) + int(num)

    def getlist(self):
        print('本次运行开始于:', self.init_time)
        # print(self.joined_event)
        # print(self.joined_TV)
        # print('本次推送活动抽奖次数:', len(self.pushed_event))
        print('本次推送广播抽奖次数:', len(self.pushed_TV))
        # print('本次参与活动抽奖次数:', len(self.joined_event))
        print('本次参与广播抽奖次数:', len(self.joined_TV))

    def getresult(self):
        print('本次参与抽奖结果为：')
        for k, v in self.result.items():
            print('{}X{}'.format(k, v))

    def delete_0st_TVlist(self):
        del self.TV_roomid_list[0]
        del self.TV_raffleid_dict[0]

    async def clean_TV(self):
        for raffleid in list(self.TV_raffleid_dict):
            await asyncio.sleep(0.2)
            if self.TV_raffleid_dict[raffleid] < time.time():
                del self.TV_raffleid_dict[raffleid]

            # response = await bilibili().get_TV_result(self.TV_roomid_list[0], self.TV_raffleid_list[0])
            # json_response = await response.json()
            # try:
            #     if json_response['msg'] == '正在抽奖中..':
            #         break
            #     data = json_response['data']
            #     if not len(data):
            #         # Printer().printer(f"房间 {self.TV_roomid_list[0]} 广播道具抽奖 {self.TV_raffleid_list[0]} 结果: {json_response['msg']}",
            #         #                   "Lottery", "cyan")
            #         # print('B站错误返回，报已错过')
            #         continue
            #     if data['gift_id'] != '-1':
            #         Printer().printer(f"房间 {self.TV_roomid_list[0]} 广播道具抽奖 {self.TV_raffleid_list[0]} 结果: {data['gift_name']}X{data['gift_num']}",
            #                           "Lottery", "cyan")
            #         self.add_to_result(data['gift_name'], int(data['gift_num']))
            #     else:
            #         Printer().printer(f"房间 {self.TV_roomid_list[0]} 广播道具抽奖 {self.TV_raffleid_list[0]} 结果: {json_response['msg']}",
            #                           "Lottery", "cyan")
            #
            #     self.delete_0st_TVlist()
            # except Exception:
            #     Printer().printer(f'获取到异常抽奖结果: {json_response}', "Warning", "red")

        if self.monitor:
            check_list = list(self.monitor)
            await asyncio.sleep(3)

            for roomid in check_list:
                check_str = bin(self.monitor[roomid]).replace('0b', '')
                # print(roomid, check_str)
                check_int = [int(check) for check in check_str]
                area_sum = sum(check_int)
                try:
                    if area_sum in [1, self.total_area]:
                        pass
                    elif area_sum == 2:
                        to_check = [-index for index in range(-1, -len(check_int)-1, -1) if check_int[index] == 1]
                        Printer().printer(f"发现监控重复 {to_check}", "Info", "green")
                        await utils.check_area_list(to_check)
                    elif area_sum == self.total_area-1:
                        to_check = [len(bin(self.area_basis-self.monitor[roomid]).replace('0b', ''))]
                        Printer().printer(f"发现监控缺失 {to_check}", "Info", "green")
                        await utils.check_area_list(to_check)
                    else:
                        Printer().printer(f"对房间 {roomid} 的抽奖出现意外的监控情况({check_str}/{self.area_basis:b})，启动分区检查", "Info", "green")
                        await utils.reconnect()
                except Exception:
                    Printer().printer(traceback.format_exc(), "Error", "red")
                finally:
                    del self.monitor[roomid]

    def append_to_TVlist(self, raffleid, time_limit):
        self.TV_raffleid_dict[raffleid] = time.time() + time_limit
        self.joined_TV.append(decimal_time())

    def append2pushed_TVlist(self, real_roomid, area_id):
        self.pushed_TV.append(decimal_time())
        self.monitor[real_roomid] = self.monitor.get(real_roomid, 0) | 2**(int(area_id)-1)

    def check_TVlist(self, raffleid):
        if self.TV_raffleid_dict.get(raffleid, None) is None:
            return True
        return False
