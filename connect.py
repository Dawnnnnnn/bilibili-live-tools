import asyncio
from MultiRoom import MultiRoom
from bilibiliCilent import bilibiliClient
from printer import Printer
from bilibili import bilibili


class connect():
    instance = None
    roomids = []
    tasks = {}
    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(connect, cls).__new__(cls, *args, **kw)
            cls.instance.danmuji = None
            cls.instance.tag_reconnect = False
        return cls.instance

    async def recreate(self):

        for roomid in connect.tasks:
            item = connect.tasks[roomid]
            task1 = item[0]
            task2 = item[1]
            task1.cancel()
            task2.cancel()
        connect.tasks.clear()
        connect.roomids = MultiRoom().get_all()
        Printer().printlist_append(['join_lottery', '', 'user', "获取新的四个分区房间{0}".format(connect.roomids)], True)
        for roomid in connect.roomids:
            self.danmuji = bilibiliClient(roomid)
            task1 = asyncio.ensure_future(self.danmuji.connectServer())
            task2 = asyncio.ensure_future(self.danmuji.HeartbeatLoop())
            connect.tasks[roomid] = [task1, task2]

    async def create(self):
        connect.roomids = MultiRoom().get_all()
        for roomid in connect.roomids:
            self.danmuji = bilibiliClient(roomid)
            task1 = asyncio.ensure_future(self.danmuji.connectServer())
            task2 = asyncio.ensure_future(self.danmuji.HeartbeatLoop())
            connect.tasks[roomid] = [task1, task2]


        while True:
            await asyncio.sleep(10)
            for roomid in connect.tasks:
                item = connect.tasks[roomid]
                task1 = item[0]
                task2 = item[1]
                if task1.done() == True or task2.done() == True:
                    if task1.done() == False:
                        task1.cancel()
                    if task2.done() == False:
                        task2.cancel()
                    danmuji = bilibiliClient(roomid)
                    task11 = asyncio.ensure_future(danmuji.connectServer())
                    task22 = asyncio.ensure_future(danmuji.HeartbeatLoop())
                    connect.tasks[roomid] = [task11, task22]

    def reconnect(self, roomid):
        self.tag_reconnect = True
        if self.danmuji is not None:
            self.danmuji.close_connection()
        bilibili().dic_bilibili['roomid'] = roomid
        print('已经切换roomid')
        self.tag_reconnect = False
