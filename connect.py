import asyncio
import traceback
from MultiRoom import MultiRoom
from bilibiliCilent import bilibiliClient
from printer import Printer



class connect():
    instance = None
    area_name = []
    roomids = []
    tasks = {}

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(connect, cls).__new__(cls, *args, **kw)
            cls.instance.danmuji = None
            cls.instance.tag_reconnect = False
        return cls.instance

    async def recreate(self, area):
        try:
            roomid = connect.roomids[connect.area_name.index(area)]

            item = connect.tasks[roomid]
            task1 = item[0]
            task2 = item[1]
            task1.cancel()
            task2.cancel()

            connect.roomids.remove(roomid)
            connect.area_name.remove(area)
            del connect.tasks[roomid]

            tmp = await MultiRoom().get_all(area)
            for i in range(len(tmp)):
                connect.roomids.append(tmp[i][0])
            for n in range(len(tmp)):
                connect.area_name.append(tmp[n][1])
            Printer().printer(f"更新四个分区房间{connect.roomids}[{connect.area_name}]","Info","green")

            roomid = tmp[0][0]
            area_name = tmp[0][1]
            self.danmuji = bilibiliClient(roomid,area_name)
            task11 = asyncio.ensure_future(self.danmuji.connectServer())
            task21 = asyncio.ensure_future(self.danmuji.HeartbeatLoop())
            connect.tasks[roomid] = [task11, task21]
        except Exception as e:
                print(e)
                traceback.print_exc()

    async def create(self):
        tmp = await MultiRoom().get_all()
        for i in range(len(tmp)):
            connect.roomids.append(tmp[i][0])
        for n in range(len(tmp)):
            connect.area_name.append(tmp[n][1])
        for roomid,area_name in zip(connect.roomids,connect.area_name):
            self.danmuji = bilibiliClient(roomid,area_name)
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
                    danmuji = bilibiliClient(roomid,connect.area_name[connect.roomids.index(roomid)])
                    task11 = asyncio.ensure_future(danmuji.connectServer())
                    task22 = asyncio.ensure_future(danmuji.HeartbeatLoop())
                    connect.tasks[roomid] = [task11, task22]

