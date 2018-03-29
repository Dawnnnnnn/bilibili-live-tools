import asyncio
from bilibiliCilent import bilibiliClient
from bilibili import bilibili
from printer import Printer


class connect():
    tasks = {}
    
    def __init__(self, printer,bilibili, api):
        self.printer = printer
        self.bilibili = bilibili 
        self.api = api
        
    async def connect(self):
        danmuji = bilibiliClient(self.printer, self.bilibili, self.api)
        task1 = asyncio.ensure_future(danmuji.connectServer())
        # print('task1启动')
        task2 = asyncio.ensure_future(danmuji.HeartbeatLoop())
        # print('task2启动')
        self.tasks[self.bilibili.roomid] = [task1, task2]
        while True:
            await asyncio.sleep(5)
            for roomid in self.tasks:
                item = self.tasks[roomid]
                task1 = item[0]
                task2 = item[1]
                if task1.done() == True or task2.done() == True:
                    # print('task断线')
                    if task1.done() == False:
                        # print('仅task2断线')
                        task1.cancel()
                    if task2.done() == False:
                        # print('仅task1断线')
                        task2.cancel()
                    print('# 重新连接直播间 %s' % roomid)
                    with open("log.txt","a+")as f:
                        f.write("reconnect success!!!!!")
                    danmuji = bilibiliClient(self.printer, self.bilibili, self.api)
                    task11 = asyncio.ensure_future(danmuji.connectServer())
                    task22 = asyncio.ensure_future(danmuji.HeartbeatLoop())
                    self.tasks[roomid] = [task11, task22]
