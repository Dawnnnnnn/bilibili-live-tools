import asyncio
from bilibiliCilent import bilibiliClient
from printer import Printer


class connect():
    tasks = {}
    
    def __init__(self):
        self.task = None
        
    async def connect(self):
        danmuji = bilibiliClient()
        task1 = asyncio.ensure_future(danmuji.connectServer())
        task2 = asyncio.ensure_future(danmuji.HeartbeatLoop())
        self.tasks = [task1, task2]
        while True:
            await asyncio.sleep(5)
            task1 = self.tasks[0]
            task2 = self.tasks[1]
            if task1.done() == True or task2.done() == True:
                print('Connect Fail')
                if task1.done() == False:
                    task1.cancel()
                if task2.done() == False:
                    task2.cancel()
                print('# 重新连接直播间')
                danmuji = bilibiliClient()
                task11 = asyncio.ensure_future(danmuji.connectServer())
                task22 = asyncio.ensure_future(danmuji.HeartbeatLoop())
                self.tasks = [task11, task22]
