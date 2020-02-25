import time
import asyncio
import traceback
import MultiRoom
from statistics import Statistics
from bilibiliCilent import bilibiliClient
from printer import Printer


class connect():
    instance = None
    areas = []
    roomids = []
    tasks = {}

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(connect, cls).__new__(cls, *args, **kw)
            cls.instance.danmuji = None
            cls.instance.tag_reconnect = False
            cls.instance.check_time = {}
            cls.instance.handle_area = []
        return cls.instance

    async def create(self):
        area_list = await MultiRoom.get_area_list()
        tmp = await MultiRoom.get_all(area_list)
        # 新的战疫分区直播间实际上没有弹幕区
        tmp = [x for x in tmp if '战疫' not in x[1]]
        for i in range(len(tmp)):
            connect.roomids.append(tmp[i][0])
        for n in range(len(tmp)):
            connect.areas.append(tmp[n][1])
        Printer().printer(f"获取到分区列表: {connect.areas}", "Info", "green")
        ckd_area_list = [int(area[:1]) for area in connect.areas]
        Statistics().adjust_basis(ckd_area_list)
        init_time = time.time()
        for area in connect.areas:
            self.check_time[area] = init_time
        for roomid,area in zip(connect.roomids, connect.areas):
            self.danmuji = bilibiliClient(roomid,area)
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
                        area = connect.areas[connect.roomids.index(roomid)]
                        Printer().printer(f"[{area}分区] 房间 {roomid} 任务出现异常", "Info", "green")
                        await self.check_area(roomid=roomid, area=area, mandatory_recreate=True)
                    else:
                        # Printer().printer(f"[{area}分区] 房间 {roomid} 任务保持正常", "Info", "green")
                        pass
            except Exception:
                Printer().printer(traceback.format_exc(), "Error", "red")

    async def check_connect(self, skip_area=None):
        if self.tag_reconnect:
            Printer().printer("connect检查任务已在运行", "Info", "green")
            return
        else:
            self.tag_reconnect = True
        # print('connect类属性:', connect.roomids, connect.areas)
        if not len(connect.roomids):
            # 说明程序刚启动还没获取监控房间，此时也不需要检查
            self.tag_reconnect = False
            return
        else:
            for roomid, area in list(zip(connect.roomids, connect.areas)):
                if (skip_area is not None) and (skip_area == area):
                    continue
                else:
                    await self.check_area(roomid=roomid, area=area)
        Printer().printer("connect检查任务已完成", "Info", "green")
        self.tag_reconnect = False

    async def check_area(self, area, roomid=None, mandatory_check=False, mandatory_recreate=False):
        if len(str(area)) == 1:
            area = [tem_area for tem_area in connect.areas if str(area) in tem_area][0]
        if roomid is None:
            roomid = connect.roomids[connect.areas.index(area)]

        if not mandatory_check and time.time() - self.check_time[area] < 60:
            Printer().printer(f"[{area}分区] 近已检查，跳过", "Info", "green")
            [ckd_roomid, ckd_area] = [roomid, area]
        else:
            # Printer().printer(f"[{area}分区] {roomid} 检查开始", "Info", "green")
            self.check_time[area] = time.time()
            [ckd_roomid, ckd_area] = await MultiRoom.check_state(roomid=roomid, area=area)
            self.check_time[area] = time.time()
        if mandatory_recreate or ckd_roomid != roomid:
            await self.recreate(new_roomid=ckd_roomid, area=ckd_area)

    async def recreate(self, area, new_roomid=None):
        if area in self.handle_area:
            Printer().printer(f"[{area}分区] 重连任务已在处理", "Info", "green")
            return
        else:
            self.handle_area.append(area)
            # Printer().printer(f"[{area}分区] 重连任务开始处理", "Info", "green")
        try:
            old_roomid = connect.roomids[connect.areas.index(area)]
            item = connect.tasks[old_roomid]
            task1 = item[0]
            task2 = item[1]
            if not task1.done():
                task1.cancel()
            if not task2.done():
                task2.cancel()
            connect.tasks[old_roomid] = []

            if new_roomid is None:
                self.check_time[area] = time.time()
                [new_roomid, new_area] = await MultiRoom.check_state(area)
                self.check_time[area] = time.time()
            else:
                new_area = area

            if not new_roomid == old_roomid:
                connect.roomids.remove(old_roomid)
                connect.areas.remove(area)
                del connect.tasks[old_roomid]
                connect.roomids.append(new_roomid)
                connect.areas.append(new_area)
                connect.tasks[new_roomid] = []
                Printer().printer(f"更新监听房间列表{connect.roomids} {connect.areas}","Info","green")

            self.danmuji = bilibiliClient(new_roomid, new_area)
            task11 = asyncio.ensure_future(self.danmuji.connectServer())
            task21 = asyncio.ensure_future(self.danmuji.HeartbeatLoop())
            connect.tasks[new_roomid] = [task11, task21]
        except Exception:
            Printer().printer(traceback.format_exc(), "Error", "red")
        # Printer().printer(f"[{area}分区] 重连任务处理完毕", "Info", "green")
        self.handle_area.remove(area)
