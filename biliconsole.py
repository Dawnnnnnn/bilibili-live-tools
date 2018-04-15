import utils
from statistics import Statistics
from connect import connect
from printer import Printer
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
    

async def preprocess_send_danmu_msg_andriod():
    msg = input('请输入要发送的信息:')
    roomid = input('请输入要发送的房间号:')
    await utils.send_danmu_msg_andriod(msg, int(roomid))
    
async def preprocess_send_danmu_msg_web():
    msg = input('请输入要发送的信息:')
    roomid = input('请输入要发送的房间号:')
    await utils.send_danmu_msg_web(msg, int(roomid))

async def preprocess_check_room():
    roomid = input('请输入要转化的房间号:')
    await utils.check_room(roomid)

def process_send_gift_web():
    utils.fetch_bag_list(verbose=True)
    bagid = input('请输入要发送的礼物编号:')
    giftid = utils.fetch_bag_list(bagid=bagid)
    # print('是谁', giftid)
    giftnum = input('请输入要发送的礼物数目:')
    roomid = input('请输入要发送的房间号:')
    utils.send_gift_web(roomid, giftid, giftnum, bagid)
    
def preprocess_change_danmuji_roomid():
    roomid = input('请输入roomid')
    connect().reconnect(roomid)

def change_printer_dic_user():
    new_words = input('弹幕控制')
    if new_words == 'T':
        Printer().dic_user['print_control']['弹幕'] = True
    else:
        Printer().dic_user['print_control']['弹幕'] = False
    

options ={
    '1': Statistics().getlist,
    '2': Statistics().getresult,
    '3': utils.fetch_bag_list,
    '4': utils.fetch_medal,
    '5': utils.fetch_user_info,
    '6': utils.check_taskinfo,
    '7': preprocess_send_danmu_msg_andriod,
    '8': preprocess_send_danmu_msg_web,
    '9': preprocess_check_room,
    '10': process_send_gift_web,
    '11': preprocess_change_danmuji_roomid,
    '12': change_printer_dic_user,
    'help': guide_of_console
}

def return_error():
    print('命令无法识别，请重新输入')

async def controler():
    while True:
        x = input('')
        if x == '7':
            # func = options.get(x, return_error)
            await preprocess_check_room()
        else:
            options.get(x, return_error)()
        await asyncio.sleep(0.1)
        
def main():
    loop = asyncio.new_event_loop()
    tasks = [
        controler()
    ]
    
    loop.run_until_complete(asyncio.wait(tasks))
    #console_thread.join()
    
    loop.close()
    
    
