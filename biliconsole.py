import utils
from statistics import Statistics
from connect import connect
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
    print('￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣')





options = {
    '1': Statistics().getlist,
    '2': Statistics().getresult,
    '3': utils.fetch_bag_list,  # async
    '4': utils.fetch_medal,  # async
    '5': utils.fetch_user_info,  # async
    '6': utils.check_taskinfo,  # async
    'help': guide_of_console
}


def return_error():
    print('命令无法识别，请重新输入')


def controler():
    while True:
        x = input('')
        # input and async
        if x in ['3', '4', '5', '6']:
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
                # print('本批次结束')
            else:
                # print('本批次轮空')
                pass

            if len_list_console == 0:
                await asyncio.sleep(1)
            else:
                self.lock.acquire()
                del self.list_console[:len_list_console]
                self.lock.release()
                await asyncio.sleep(0.3)
