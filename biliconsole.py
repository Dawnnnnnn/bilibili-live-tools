import utils
from statistics import Statistics

def guide_of_console():
    print('___________________________')
    print('| 欢迎使用本控制台           |')
    print('|1 输出本次的参与抽奖统计     |')
    print('|2 输出本次的抽奖结果统计     |')
    print('|3 查看目前拥有礼物的统计     |')
    print('|4 查看持有勋章状态          |')
    print('|5 获取直播个人的基本信息     |')
    print('|6 检查今日任务的完成情况     |')
    print('￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣')
    




options ={
    '1': Statistics().getlist,
    '2': Statistics().getresult,
    '3': utils.fetch_bag_list,
    '4': utils.fetch_medal,
    '5': utils.fetch_user_info,
    '6': utils.check_taskinfo,
    'help': guide_of_console
}


def controler():
    while True:
        x = input('')
        options[x]()
