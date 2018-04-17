import utils
from statistics import Statistics
from connect import connect
from printer import Printer
import threading
import asyncio

def guide_of_console():
    print('___________________________')
    print('| 欢迎使用本控制台           |')
    print('|1 输出本次的参与抽奖统计     |')
    print('|2 输出本次的抽奖结果统计     |')
    print('|3 查看目前拥有礼物的统计     |')
    print('|4 查看持有勋章状态          |')
    print('|5 获取直播个人的基本信息     |')
    print('|6 检查今日任务的完成情况     |')
    print('|7 模拟安卓客户端发送弹幕     |')
    print('|8 模拟电脑网页端发送弹幕     |')
    print('|9 直播间的长短号码的转化     |')
    print('￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣')
    

def preprocess_send_danmu_msg_andriod():
    msg = input('请输入要发送的信息:')
    roomid = input('请输入要发送的房间号:')
    Biliconsole().append2list_console([[msg, int(roomid)], utils.send_danmu_msg_andriod])
    
def preprocess_send_danmu_msg_web():
    msg = input('请输入要发送的信息:')
    roomid = input('请输入要发送的房间号:')
    Biliconsole().append2list_console([[msg, int(roomid)], utils.send_danmu_msg_web])

def preprocess_check_room():
    roomid = input('请输入要转化的房间号:')
    Biliconsole().append2list_console([[roomid], utils.check_room])

def process_send_gift_web():
    Biliconsole().append2list_console([[True], utils.fetch_bag_list])
    bagid = input('请输入要发送的礼物编号:')
    # print('是谁', giftid)
    giftnum = input('请输入要发送的礼物数目:')
    roomid = input('请输入要发送的房间号:')
    Biliconsole().append2list_console([[roomid, [[False, bagid],utils.fetch_bag_list], giftnum, bagid],utils.send_gift_web])
    
def preprocess_change_danmuji_roomid():
    roomid = input('请输入roomid')
    connect().reconnect(roomid)

def change_printer_dic_user():
    new_words = input('弹幕控制')
    if new_words == 'T':
        Printer().dic_user['print_control']['弹幕'] = True
    else:
        Printer().dic_user['print_control']['弹幕'] = False
def preprocess_fetch_liveuser_info():
    real_roomid = input('请输入roomid')
    Biliconsole().append2list_console([[real_roomid], utils.fetch_liveuser_info])
    

options ={
    '1': Statistics().getlist,
    '2': Statistics().getresult,
    '3': utils.fetch_bag_list,#async
    '4': utils.fetch_medal,#async
    '5': utils.fetch_user_info,#async
    '6': utils.check_taskinfo,#async
    '7': preprocess_send_danmu_msg_andriod,#input async
    '8': preprocess_send_danmu_msg_web,#input async
    '9': preprocess_check_room,#input async
    '10': process_send_gift_web,#input async !!!
    '11': preprocess_change_danmuji_roomid,
    '12': change_printer_dic_user,
    '13': preprocess_fetch_liveuser_info,
    'help': guide_of_console
}

def return_error():
    print('命令无法识别，请重新输入')

def controler():
    while True:
        x = input('')
        # input and async
        if x == ['7', '8', '9', '10', '13']:
            # func = options.get(x, return_error)
            args, func = options.get(x, return_error)()
            #print(args)
            #Biliconsole().append2list_console(answer)
        # async
        elif x in ['3', '4', '5', '6']:
            answer = options.get(x, return_error)
            Biliconsole().append2list_console(answer)
        # normal
        else:
            options.get(x, return_error)()
        
class Biliconsole():
    instance = None

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(Biliconsole, cls).__new__(cls, *args, **kw)
            cls.instance.list_console = []
            cls.lock = threading.Lock()
        return cls.instance
        
    def append2list_console(self, request):
        self.lock.acquire()
        self.list_console.append(request)
        self.lock.release()
        
    async def run(self):
        while True:
            len_list_console = len(self.list_console)
            tasklist = []
            for i in self.list_console:
                if isinstance(i, list):
                    # 对10号单独简陋处理
                    for j in range(len(i[0])):
                        if isinstance(i[0][j], list):
                            i[0][j] = await i[0][j][1](*(i[0][j][0]))
                    task = asyncio.ensure_future(i[1](*i[0]))
                else:
                    task = asyncio.ensure_future(i())
                tasklist.append(task)
            if tasklist:  
                await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)
                #print('本批次结束')
            else:
                #print('本批次轮空')
                pass
                
            if len_list_console == 0:
                await asyncio.sleep(1)
            else:
                self.lock.acquire()
                del self.list_console[:len_list_console]
                self.lock.release()
                await asyncio.sleep(0.3)
        
        
        
    
    
    
