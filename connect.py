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
            cls.instance.handle_area = []
        return cls.instance

    async def recreate(self, area_name, new_roomid=None):
        if area_name in self.handle_area:
            Printer().printer(f"[{area_name}] 重连任务已在处理", "Info", "green")
            return
        else:
            self.handle_area.append(area_name)
            # Printer().printer(f"[{area_name}] 重连任务开始处理", "Info", "green")
        try:
            old_roomid = connect.roomids[connect.area_name.index(area_name)]
            item = connect.tasks[old_roomid]
            task1 = item[0]
            task2 = item[1]
            if not task1.done():
                task1.cancel()
            if not task2.done():
                task2.cancel()
            connect.tasks[old_roomid] = []

            if new_roomid is None:
                [new_roomid, new_area_name] = await MultiRoom().check_state(area_name)

            if not new_roomid == old_roomid:
                connect.roomids.remove(old_roomid)
                connect.area_name.remove(area_name)
                del connect.tasks[old_roomid]
                connect.roomids.append(new_roomid)
                connect.area_name.append(area_name)
                connect.tasks[new_roomid] = []
                Printer().printer(f"更新四个分区房间{connect.roomids} {connect.area_name}","Info","green")

            self.danmuji = bilibiliClient(new_roomid, new_area_name)
            task11 = asyncio.ensure_future(self.danmuji.connectServer())
            task21 = asyncio.ensure_future(self.danmuji.HeartbeatLoop())
            connect.tasks[new_roomid] = [task11, task21]
        except Exception:
            traceback.print_exc()
        # Printer().printer(f"[{area_name}] 重连任务处理完毕", "Info", "green")
        self.handle_area.remove(area_name)

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
            try:
                for roomid in list(connect.tasks):
                    item = connect.tasks.get(roomid, None)
                    if (item is None) or (not len(item)):
                        Printer().printer(f"房间 {roomid} 任务已被清理，跳过", "Info", "green")
                        continue
                    task1 = item[0]
                    task2 = item[1]
                    if task1.done() == True or task2.done() == True:
                        area_name = connect.area_name[connect.roomids.index(roomid)]
                        Printer().printer(f"[{area_name}] 房间 {roomid} 任务出现异常", "Info", "green")
                        [ckd_roomid, ckd_area_name] = await MultiRoom().check_state(roomid=roomid, area=area_name)
                        await self.recreate(new_roomid=ckd_roomid, area_name=area_name)
                    else:
                        # Printer().printer(f"[{area_name}] 房间 {roomid} 任务保持正常", "Info", "green")
                        pass
            except Exception:
                traceback.print_exc()

    async def check_connect(self, skip_area=None):
        if self.tag_reconnect:
            Printer().printer(f"connect检查任务已在运行", "Info", "green")
            return
        else:
            self.tag_reconnect = True
        # print('connect类属性:', connect.roomids, connect.area_name)
        if not len(connect.roomids):
            # 说明程序刚启动还没获取监控房间，此时也不需要检查
            self.tag_reconnect = False
            return
        else:
            for roomid, area_name in list(zip(connect.roomids, connect.area_name)):
                if (skip_area is not None) and (skip_area == area_name):
                    continue
                elif not roomid in connect.roomids:
                    continue
                else:
                    [ckd_roomid, ckd_area_name] = await MultiRoom().check_state(roomid=roomid, area=area_name)
                    if ckd_roomid == roomid:
                        continue
                    else:
                        await self.recreate(new_roomid=ckd_roomid, area_name=area_name)
        Printer().printer(f"connect检查任务已完成", "Info", "green")
        self.tag_reconnect = False
