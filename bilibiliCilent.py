from bilibili import bilibili
from statistics import Statistics
from printer import Printer
from rafflehandler import Rafflehandler
from schedule import Schedule
import utils
import traceback
import asyncio
import random
import struct
import zlib
import json
import sys


async def handle_1_TV_raffle(type, raffleid, time_wait, time_limit, num, real_roomid):
    Statistics().append_to_TVlist(raffleid, time_limit)
    if Schedule().scheduled_sleep:
        Printer().printer(f"定时休眠，跳过房间 {real_roomid} 广播道具抽奖 {raffleid}", "Info", "green")
        return
    if bilibili().black_status:
        Printer().printer(f"黑屋休眠，跳过房间 {real_roomid} 广播道具抽奖 {raffleid}", "Info", "green")
        return
    await asyncio.sleep(min(max(0, time_wait) + random.uniform(0, min(num, 30)), time_limit-1))
    response2 = await bilibili().get_gift_of_TV(type, real_roomid, raffleid)
    # Printer().printer(f"参与了房间 {real_roomid} 的广播抽奖 {raffleid}", "Lottery", "cyan")
    json_response2 = await response2.json(content_type=None)
    # Printer().printer(f"参与房间 {real_roomid} 广播道具抽奖 {raffleid} 状态: {json_response2['msg']}", "Lottery", "cyan")
    if json_response2['code'] == 0:
        data = json_response2["data"]
        Printer().printer(f"房间 {real_roomid} 广播道具抽奖 {raffleid} 结果: {data['award_name']}X{data['award_num']}",
                          "Lottery", "cyan")
        Statistics().add_to_result(data['award_name'], int(data['award_num']))
    else:
        # {"code":-403,"data":null,"message":"访问被拒绝","msg":"访问被拒绝"}
        # {'code': 503, 'data': None, 'message': '请求太多了！', 'msg': '请求太多了！'}
        # {'code': -509, 'message': '请求过于频繁，请稍后再试', 'ttl': 1}
        Printer().printer(f"房间 {real_roomid} 广播道具抽奖 {raffleid} 结果: {json_response2['message']}",
                          "Lottery", "cyan")
        print(json_response2)


async def handle_1_room_TV(real_roomid):
    await asyncio.sleep(random.uniform(0, 1))
    response = await bilibili().get_giftlist_of_TV(real_roomid)
    json_response = await response.json(content_type=None)
    checklen = json_response['data']['gift']
    num = len(checklen)
    if num:
        result = await utils.check_room_true(real_roomid)
        if True in result:
            Printer().printer(f"检测到房间 {real_roomid} 的钓鱼操作", "Warning", "red")
        else:
            await bilibili().post_watching_history(real_roomid)
            list_available_raffleid = []
            for j in range(0, num):
                raffleid = json_response['data']['gift'][j]['raffleId']
                if Statistics().check_TVlist(raffleid):
                    type = json_response['data']['gift'][j]['type']
                    time_wait = json_response['data']['gift'][j]['time_wait']
                    time_limit = json_response['data']['gift'][j]['time']
                    list_available_raffleid.append([type, raffleid, time_wait, time_limit])
            tasklist = []
            num_available = len(list_available_raffleid)
            for k in list_available_raffleid:
                task = asyncio.ensure_future(handle_1_TV_raffle(*k, num_available, real_roomid))
                tasklist.append(task)
            if tasklist:
                await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)


class bilibiliClient():

    def __init__(self, roomid, area):
        self.bilibili = bilibili()
        self._protocol_version = self.bilibili.dic_bilibili['_protocolversion']
        self._reader = None
        self._writer = None
        self._uid = int(100000000000000 + 200000000000000 * random.random())
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
            self._reader, self._writer = await asyncio.open_connection(self.bilibili.dic_bilibili['_ChatHost'],
                                                                       self.bilibili.dic_bilibili['_ChatPort'])
        except:
            print("连接无法建立，请检查本地网络状况")
            await asyncio.sleep(5)
            return
        if await self.SendJoinChannel():
            self.connected = True
            Printer().printer(f'[{self.area}分区] 连接 {self._roomId} 弹幕服务器成功', "Info", "green")
            await self.ReceiveMessageLoop()

    async def HeartbeatLoop(self):
        while not self.connected:
            await asyncio.sleep(0.5)

        while self.connected:
            await self.SendSocketData(ver=self._protocol_version, action=2, body="")
            await asyncio.sleep(30)

    async def SendJoinChannel(self):
        body = json.dumps({
            "roomid": self._roomId,
            "uid": self._uid,
            # "protover": 2,
            # "key": token,
        }, separators=(',', ':'))
        return await self.SendSocketData(ver=self._protocol_version, action=7, body=body)

    async def SendSocketData(self, ver, action, body):
        bytearr = body.encode('utf-8')
        header_len = 16
        body_len = len(bytearr)
        packet_len = 16 + body_len
        sequence = 1
        sendbytes = struct.pack(f'!IHHII{body_len}s',
                                packet_len, header_len, ver, action, sequence, bytearr)
        try:
            self._writer.write(sendbytes)
        except Exception:
            Printer().printer(f"Error when self._writer.write(sendbytes): {sys.exc_info()[0]}, {sys.exc_info()[1]}",
                              "Error", "red")
            self.connected = False
            return False
        try:
            await self._writer.drain()
        except (ConnectionResetError, ConnectionAbortedError) as e:
            # [WinError 10054] 远程主机强迫关闭了一个现有的连接。
            # [WinError 10053] 你的主机中的软件中止了一个已建立的连接。
            Printer().printer(f"Failed @ self._writer.drain(): {repr(e)}", "Error", "red")
            return False
        except Exception:
            Printer().printer(f"Error when self._writer.drain(): {sys.exc_info()[0]}, {sys.exc_info()[1]}",
                              "Error", "red")
            return False
        return True

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
            except OSError:
                Printer().printer(f'[WinError 121] 信号灯超时时间已到 @[{self.area}分区]{self._roomId}',"Error","red")
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

            if not len(tmp):
                Printer().printer(f"主动关闭或者远端主动发来FIN @[{self.area}分区]{self._roomId}","Error","red")
                self.close_connection()
                await asyncio.sleep(1)
                return None
            else:
                bytes_data += tmp
                len_remain -= len(tmp)

        return bytes_data

    async def ReceiveMessageLoop(self):
        while self.connected:
            length = await self.ReadSocketData(4)
            if length is None:
                break

            packet_len, = struct.unpack('!I', length)
            body = await self.ReadSocketData(packet_len-4)
            if body is None:
                break

            await self.parse_packet(packet_len, body)

    async def parse_packet(self, packet_len: int, body: bytes):
        """
        len(body) == packet_len - 4
        :param packet_len: length of whole packet
        :param body: header except packet_len + subsequent main body
        """
        # 基础假设是每个packet都有16字节header的保守序列，没有另外再先读取header_len然后读header
        header_len, ver, action, sequence = struct.unpack('!HHII', body[:12])
        body = body[12:]
        # print(packet_len, header_len, ver, action, sequence, body)

        if action == 3:
            # 3 人气值，数据不是JSON，是4字节整数
            self._UserCount, = struct.unpack('!I', body)
        else:
            try:
                dic = json.loads(body)
            except UnicodeDecodeError:
                inner_packet = zlib.decompress(body)
                # print(f'{packet_len} 字节解压出 {inner_packet.count(b"cmd")} 条消息')

                pack_p = 0
                packs_len = len(inner_packet)
                while pack_p < packs_len:
                    pack_len, = struct.unpack('!I', inner_packet[pack_p:pack_p+4])
                    await self.parse_packet(pack_len, inner_packet[pack_p+4:pack_p+pack_len])
                    pack_p += pack_len
                return
            except json.JSONDecodeError as e:
                Printer().printer(f"{repr(e)} when json decode: {body}", "Error", "red")
                return
            except Exception:
                Printer().printer(f"Failed when parse_packet: {body}\n{traceback.format_exc()}", "Error", "red")
                return

            if action == 5:
                try:
                    await self.parseDanMu(dic)
                except Exception:
                    Printer().printer(f"Failed when parsing: {dic}\n{traceback.format_exc()}", "Error", "red")
            elif action == 8:
                # 26, 16, 2, 8, 1, b'{"code":0}'
                pass
            else:
                # lyyyuna原版有action=17就不去请求body的逻辑
                Printer().printer(f"异常action值: {packet_len, header_len, ver, action, sequence, dic}", "Warning", "red")

    async def parseDanMu(self, dic):
        cmd = dic.get('cmd')
        if cmd is None:
            Printer().printer(f"No cmd: {dic}", "Warning", "red")
            return

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