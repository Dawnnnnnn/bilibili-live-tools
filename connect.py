import asyncio
import utils
from bilibiliCilent import bilibiliClient
from printer import Printer
from bilibili import bilibili


class connect():
    instance = None
    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(connect, cls).__new__(cls, *args, **kw)
            cls.instance.danmuji = None
            cls.instance.tag_reconnect = False
        return cls.instance
        
    async def connect(self):
        while True:
            Printer().printlist_append(['join_lottery', '', 'user', "正在启动弹幕姬"], True)
            time_start = int(utils.CurrentTime())
            self.danmuji = bilibiliClient()
            task_main = asyncio.ensure_future(self.danmuji.connectServer())
            task_heartbeat = asyncio.ensure_future(self.danmuji.HeartbeatLoop())
            finished, pending = await asyncio.wait([task_main, task_heartbeat], return_when=asyncio.FIRST_COMPLETED)
            print('# 弹幕姬异常或主动断开，处理完剩余信息后重连')
            self.danmuji.connected = False
            time_end = int(utils.CurrentTime())
            if task_heartbeat.done() == False:
                task_heartbeat.cancel()
                print('# 弹幕主程序退出，立即取消心跳模块')
            else:
                await asyncio.wait(pending)
                print('# 弹幕心跳模块退出，主程序剩余任务处理完毕')
            # 类似于lock功能，当reconnect模块使用时，禁止重启，直到reconnect模块修改完毕)
            while self.tag_reconnect:
                await asyncio.sleep(0.5)
                print('pending')
            if time_end - time_start < 5:
                print('# 当前网络不稳定，为避免频繁不必要尝试，将自动在5秒后重试')
                await asyncio.sleep(5)
            
        
    def reconnect(self, roomid):
        self.tag_reconnect = True
        if self.danmuji is not None:
            self.danmuji.close_connection()
        bilibili().dic_bilibili['roomid'] = roomid
        print('已经切换roomid')
        self.tag_reconnect = False
