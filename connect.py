import asyncio
from bilibiliCilent import bilibiliClient
from bilibili import bilibili
from printer import Printer


class connect(bilibili):
    tasks = {}
    
    def __init__(self, printer):
        self.printer = printer 
        
    async def connect(self):
        danmuji = bilibiliClient(self.printer)
        task1 = asyncio.ensure_future(danmuji.connectServer())
        task2 = asyncio.ensure_future(danmuji.HeartbeatLoop())
        self.tasks[bilibili.roomid] = [task1, task2]
        while True:
            await asyncio.sleep(10)
            for roomid in self.tasks:
                item = self.tasks[roomid]
                task1 = item[0]
                task2 = item[1]
                if task1.done() == True or task2.done() == True:
                    if task1.done() == False:
                        task1.cancel()
                    if task2.done() == False:
                        task2.cancel()
                    print ('# 重新连接直播间 %s' % roomid)
                    with open("log.txt","a+")as f:
                        f.write("reconnect success!!!!!")
                    danmuji = bilibiliClient(self.printer)
                    task11 = asyncio.ensure_future(danmuji.connectServer())
                    task22 = asyncio.ensure_future(danmuji.HeartbeatLoop())
                    self.tasks[roomid] = [task11, task22]
