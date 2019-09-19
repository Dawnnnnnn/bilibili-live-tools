from bilibili import bilibili
from statistics import Statistics
from printer import Printer
from rafflehandler import Rafflehandler
import utils
import asyncio
import random
import struct
import json
import sys


async def handle_1_TV_raffle(type, num, real_roomid, raffleid):
    await asyncio.sleep(random.uniform(0, min(num, 30)))
    response2 = await bilibili().get_gift_of_TV(type, real_roomid, raffleid)
    # Printer().printer(f"参与了房间 {real_roomid} 的广播抽奖 {raffleid}", "Lottery", "cyan")
    json_response2 = await response2.json(content_type=None)
    Printer().printer(f"参与房间 {real_roomid} 广播道具抽奖 {raffleid} 状态: {json_response2['msg']}", "Lottery", "cyan")
    if json_response2['code'] == 0:
        Statistics().append_to_TVlist(raffleid, real_roomid)
    else:
        print(json_response2)


async def handle_1_room_TV(real_roomid):
    await asyncio.sleep(random.uniform(0, 1))
    result = await utils.check_room_true(real_roomid)
    if True in result:
        Printer().printer(f"检测到房间 {real_roomid} 的钓鱼操作", "Warning", "red")
    else:
        await bilibili().post_watching_history(real_roomid)
        response = await bilibili().get_giftlist_of_TV(real_roomid)
        json_response = await response.json(content_type=None)
        checklen = json_response['data']['list']
        num = len(checklen)
        list_available_raffleid = []
        for j in range(0, num):
            raffleid = json_response['data']['list'][j]['raffleId']
            type = json_response['data']['list'][j]['type']
            if Statistics().check_TVlist(raffleid):
                list_available_raffleid.append([type, raffleid])
        tasklist = []
        num_available = len(list_available_raffleid)
        for k in list_available_raffleid:
            task = asyncio.ensure_future(handle_1_TV_raffle(k[0], num_available, real_roomid, k[1]))
            tasklist.append(task)
        if tasklist:
            await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)


class bilibiliClient():

    def __init__(self, roomid, area):
        self.bilibili = bilibili()
        self._reader = None
        self._writer = None
        self._uid = None
        self.connected = False
        self._UserCount = 0
        self.dic_bulletin = {
            'cmd': 'str',
            'msg': 'str',
            'rep': 'int',
            'url': 'str'
        }
        self._roomId = roomid
        self.area = area

    def close_connection(self):
        self._writer.close()
        self.connected = False

    async def connectServer(self):
        try:
            reader, writer = await asyncio.open_connection(self.bilibili.dic_bilibili['_ChatHost'],
                                                           self.bilibili.dic_bilibili['_ChatPort'])
        except:
            print("连接无法建立，请检查本地网络状况")
            await asyncio.sleep(5)
            return
        self._reader = reader
        self._writer = writer
        if (await self.SendJoinChannel(self._roomId) == True):
            self.connected = True
            Printer().printer(f'[{self.area}分区] 连接 {self._roomId} 弹幕服务器成功', "Info", "green")
            await self.ReceiveMessageLoop()

    async def HeartbeatLoop(self):
        while not self.connected:
            await asyncio.sleep(0.5)

        while self.connected:
            await self.SendSocketData(0, 16, self.bilibili.dic_bilibili['_protocolversion'], 2, 1, "")
            await asyncio.sleep(30)

    async def SendJoinChannel(self, channelId):
        self._uid = (int)(100000000000000.0 + 200000000000000.0 * random.random())
        body = '{"roomid":%s,"uid":%s}' % (channelId, self._uid)
        await self.SendSocketData(0, 16, self.bilibili.dic_bilibili['_protocolversion'], 7, 1, body)
        return True

    async def SendSocketData(self, packetlength, magic, ver, action, param, body):
        bytearr = body.encode('utf-8')
        if packetlength == 0:
            packetlength = len(bytearr) + 16
        sendbytes = struct.pack('!IHHII', packetlength, magic, ver, action, param)
        if len(bytearr) != 0:
            sendbytes = sendbytes + bytearr
        try:
            self._writer.write(sendbytes)
        except:
            Printer().printer(f"Error when self._writer.write(sendbytes): {sys.exc_info()[0]}, {sys.exc_info()[1]}","Error","red")
            self.connected = False
        try:
            await self._writer.drain()
        except ConnectionError:
            pass
        except Exception:
            Printer().printer(f"Error when self._writer.drain(): {sys.exc_info()[0]}, {sys.exc_info()[1]}","Error","red")

    async def ReadSocketData(self, len_wanted):
        bytes_data = b''
        if len_wanted == 0:
            return bytes_data
        len_remain = len_wanted
        while len_remain != 0:
            try:
                tmp = await asyncio.wait_for(self._reader.read(len_remain), timeout=35.0)
            except asyncio.TimeoutError:
                # 由于心跳包30s一次，但是发现35s内没有收到任何包，说明已经悄悄失联了，主动断开
                Printer().printer(f'心跳失联，主动断开 @[{self.area}分区]{self._roomId}',"Error","red")
                self.close_connection()
                await asyncio.sleep(1)
                return None
            except ConnectionResetError:
                Printer().printer(f'RESET，网络不稳定或者远端不正常断开 @[{self.area}分区]{self._roomId}',"Error","red")
                self.close_connection()
                await asyncio.sleep(5)
                return None
            except ConnectionAbortedError:
                Printer().printer(f'你的主机中的软件中止了一个已建立的连接 @[{self.area}分区]{self._roomId}',"Error","red")
                self.close_connection()
                await asyncio.sleep(5)
                return None
            except asyncio.CancelledError:

                return None
            except:
                Printer().printer(f"{sys.exc_info()[0]}, {sys.exc_info()[1]} @[{self.area}分区]{self._roomId}","Error","red")
                Printer().printer(f'请联系开发者',"Warning","red")
                self.close_connection()
                return None

            if not tmp:
                Printer().printer(f"主动关闭或者远端主动发来FIN @[{self.area}分区]{self._roomId}","Error","red")
                self.close_connection()
                await asyncio.sleep(1)
                return None
            else:
                bytes_data = bytes_data + tmp
                len_remain = len_remain - len(tmp)

        return bytes_data

    async def ReceiveMessageLoop(self):
        while self.connected == True:
            tmp = await self.ReadSocketData(16)
            if tmp is None:
                break

            expr, = struct.unpack('!I', tmp[:4])

            num, = struct.unpack('!I', tmp[8:12])

            num2 = expr - 16

            tmp = await self.ReadSocketData(num2)
            if tmp is None:
                break

            if num2 != 0:
                num -= 1
                if num == 0 or num == 1 or num == 2:
                    num3, = struct.unpack('!I', tmp)
                    self._UserCount = num3
                    continue
                elif num == 3 or num == 4:
                    try:
                        messages = tmp.decode('utf-8')
                    except:
                        continue
                    await self.parseDanMu(messages)
                    continue
                elif num == 5 or num == 6 or num == 7:
                    continue
                else:
                    if num != 16:
                        pass
                    else:
                        continue

    async def parseDanMu(self, messages):
        try:
            dic = json.loads(messages)

        except:
            return
        cmd = dic['cmd']

        if cmd == 'LIVE':
            # Printer().printer(f"[{self.area}分区] 房间 {self._roomId} 疑似切换分区！启动分区检查", "Info", "green")
            # await utils.check_area_list([self.area], mandatory_check=True)
            pass
        elif cmd == 'PREPARING':
            Printer().printer(f"[{self.area}分区] 房间 {self._roomId} 下播！将切换监听房间", "Info", "green")
            self.close_connection()
            await utils.reconnect(self.area)
        elif cmd == 'DANMU_MSG':
            # Printer().printer(f"{dic}", "Message", "cyan", printable=False)
            pass
        elif cmd == 'SYS_GIFT':
            # Printer().printer(f"出现了远古的SYS_GIFT,请尽快联系开发者{dic}", "Warning", "red")
            pass
        elif cmd == 'NOTICE_MSG':
            # msg_type: 1 小时榜首绘马大奖等通报
            #           2 抽奖 (TV, 大楼, etc.)
            #           3 舰队
            #           4 总督进入直播间
            #           5 当前房间高能大奖
            #           6 风暴
            #           8 任意门
            #           9 活动中主播达成星级通报
            try:
                if dic.get('msg_type') in [2, 8]:
                    real_roomid = dic.get('real_roomid')
                    Printer().printer(f"检测到房间 {real_roomid} 的广播抽奖 @[{self.area}分区]{self._roomId}", "Lottery", "cyan")
                    Rafflehandler().append2list_TV(real_roomid)
                    Statistics().append2pushed_TVlist(real_roomid, self.area[0])
                else:
                    Printer().printer(f"{dic['msg_common']} @[{self.area}分区]{self._roomId}", "Info", "green")
            except Exception:
                Printer().printer(f"NOTICE_MSG出错，请联系开发者 {dic}", "Warning", "red")
        elif cmd == 'SYS_MSG':
            if set(dic) in [set(self.dic_bulletin), {'cmd', 'msg', 'msg_text'}, {'cmd', 'msg', 'url'}]:
                Printer().printer(f"{dic['msg']} @[{self.area}分区]{self._roomId}", "Info", "green")
            else:
                try:
                    real_roomid = dic['real_roomid']
                    Printer().printer(f"检测到房间 {real_roomid} 的广播抽奖 @[{self.area}分区]{self._roomId}", "Lottery", "cyan")
                    Rafflehandler().append2list_TV(real_roomid)
                    Statistics().append2pushed_TVlist(real_roomid, self.area[0])
                except:
                    Printer().printer(f"SYS_MSG出错，请联系开发者 {dic}", "Warning", "red")

        # 观众相关 [欢迎入场，送礼，发弹幕]
        elif cmd in ["WELCOME", "SEND_GIFT", "DANMU_MSG"]:
            pass
        # 各种通知 [通知（当前房间开奖 活动小时榜 各种SYS_MSG都会同时有NOTICE_MSG），系统通知（友爱社 心愿达成 绘马 主播招募 直播间强推）]
        elif cmd in ["NOTICE_MSG", "SYS_MSG"]:
            pass
        # 各种高能 [节奏风暴（开始 结束），高能广播（无抽奖 活动高能 全频风暴），抽奖通知（现在广播全在这里了），总督广播]
        elif cmd in ["SPECIAL_GIFT", "SYS_GIFT", "SYS_MSG", "GUARD_MSG", "GUIARD_MSG"]:
            pass
        # 礼物效果 [连击开始，连击结束，使用积分加成卡]
        elif cmd in ["COMBO_SEND", "COMBO_END", "SCORE_CARD"]:
            pass
        # PK相关
        elif cmd in ["PK_INVITE_INIT", "PK_INVITE_FAIL", "PK_INVITE_CANCEL", "PK_INVITE_SWITCH_OPEN", "PK_INVITE_SWITCH_CLOSE",
                     "PK_PRE", "PK_START", "PK_PROCESS", "PK_SETTLE", "PK_END", "PK_MIC_END",
                     "PK_MATCH", "PK_CLICK_AGAIN", "PK_AGAIN"]:
            pass
        # 当前房间抽奖相关
        elif cmd in ["RAFFLE_START", "RAFFLE_END", "TV_START", "TV_END", "GUARD_LOTTERY_START", "LOTTERY_START"]:
            pass
        # 房间管理相关 [屏蔽关键词，用户被加入黑名单，禁言开启，禁言关闭，新设房管，房管变更]
        elif cmd in ["ROOM_SHIELD", "ROOM_BLOCK_MSG", "ROOM_SILENT_ON", "ROOM_SILENT_OFF", "room_admin_entrance", "ROOM_ADMINS"]:
            pass
        # 舰队相关 [本房间购买舰长，船票购买，本房间舰队消息（登船），船员进房间，进房间特效]
        elif cmd in ["USER_TOAST_MSG", "GUARD_BUY", "GUARD_MSG", "WELCOME_GUARD", "ENTRY_EFFECT"]:
            pass
        # 直播状态相关 [开播，下播，警告，被切直播，房间被封]
        elif cmd in ["LIVE", "PREPARING", "WARNING", "CUT_OFF", "ROOM_LOCK"]:
            pass
        # 活动榜单相关 [进入小时榜，未知，获小时榜第一道具奖励]
        elif cmd in ["ROOM_RANK", "new_anchor_reward", "HOUR_RANK_AWARDS"]:
            pass
        # 活动相关 [活动获得的直播间入场特效，活动事件（如充能值信息），以前的高能事件，送礼抽奖活动开奖，LOL竞猜活动，LOL助力活动，？（不知道是啥，每个直播间都有，无论开播，每分钟发一次），？，？，冲鸭！机甲大作战相关，周星活动相关]
        elif cmd in ["WELCOME_ACTIVITY", "ACTIVITY_EVENT", "EVENT_CMD", "BOX_LOTTERY_WIN", "LOL_ACTIVITY", "ACTIVITY_MATCH_GIFT",
                     "ACTIVITY_BANNER_RED_NOTICE_CLOSE", "ACTIVITY_BANNER_CLOSE", "DAILY_QUEST_NEWDAY",
                     "BOSS_ENERGY", "NOTICE_MSG_H5", "BOSS_INJURY", "BOSS_BATTLE", "ANIMATION", "BOSS_INFO",
                     "WEEK_STAR_CLOCK", "ROOM_BOX_MASTER", "ROOM_BOX_USER"]:
            pass
        # 直播间信息相关 [直播间更换壁纸，直播间界面皮肤变化，许愿瓶进度变化，关注数变化，直播间更名，实物抽奖宝箱提醒，实物抽奖宝箱开奖，弹幕抽奖结束]
        elif cmd in ["CHANGE_ROOM_INFO", "ROOM_SKIN_MSG", "WISH_BOTTLE", "ROOM_REAL_TIME_MESSAGE_UPDATE", "ROOM_CHANGE", "BOX_ACTIVITY_START", "WIN_ACTIVITY", "DANMU_LOTTERY_END"]:
            pass
        # 大乱斗活动
        elif cmd in ["PK_BATTLE_ENTRANCE", "PK_BATTLE_PRE", "PK_BATTLE_MATCH_TIMEOUT", "PK_BATTLE_START", "PK_BATTLE_VOTES_ADD",
                     "PK_BATTLE_PROCESS", "PK_BATTLE_PRO_TYPE", "PK_BATTLE_GIFT", "PK_BATTLE_END", "PK_BATTLE_RANK_CHANGE",
                     "PK_BATTLE_SETTLE_USER", "PK_BATTLE_SETTLE", "PK_LOTTERY_START", "ACTIVITY_BANNER_UPDATE"]:
            pass
        else:
            # Printer().printer(f"出现一个未知msg @[{self.area}分区]{self._roomId} {dic}", "Warning", "red")
            pass
