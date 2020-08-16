#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/12/30 13:24
# @Author  : Dawnnnnnn
# @Contact: 1050596704@qq.com

import asyncio
import json
import traceback
from struct import Struct

from printer import Printer
from rafflehandler import Rafflehandler


class TCP_monitor():
    header_struct = Struct('>I')

    def __init__(self):
        self._reader = None
        self._writer = None
        self.connected = False

    def _encapsulate(self, str_body):
        body = str_body.encode('utf-8')
        len_body = len(body)
        len_header = 4
        header = self.header_struct.pack(len_body + len_header)
        return header + body

    def close_connection(self):
        self._writer.close()
        self.connected = False

    async def connectServer(self, host, port, key):
        while True:
            try:
                reader, writer = await asyncio.open_connection(host, port)
                self._reader = reader
                self._writer = writer
                Printer().printer(f'监控服务器连接成功', "Info", "green")
                await self.send_bytes(self.Auth_Key(key))
                self.connected = True
            except Exception:
                Printer().printer(f'连接无法建立，请检查本地网络状况,2s后重连', "Error", "red")
                self.connected = False
                await asyncio.sleep(2)
                continue
            await self.ReceiveMessageLoop()
            Printer().printer(f'与服务器连接断开,2s后尝试重连', "Error", "red")
            self.connected = False
            await asyncio.sleep(2)

    async def HeartbeatLoop(self):
        while True:
            try:
                while not self.connected:
                    await asyncio.sleep(0.5)
                while self.connected:
                    await self.send_bytes(self.Heartbeat())
                    await asyncio.sleep(25)
            except:
                traceback.print_exc()

    def Auth_Key(self, key):
        dict_enter = {
            "cmd": "Auth",
            "data": {"key": key},
            "code": 0
        }
        str_enter = json.dumps(dict_enter)
        bytes_enter = self._encapsulate(str_body=str_enter)
        return bytes_enter

    def Heartbeat(self):
        dict_enter = {
            "cmd": "HeartBeat",
            "data": {},
            "code": 0
        }
        str_enter = json.dumps(dict_enter)
        bytes_enter = self._encapsulate(str_body=str_enter)
        return bytes_enter

    async def send_bytes(self, bytes_data) -> bool:
        try:
            self._writer.write(bytes_data)
            await self._writer.drain()
        except asyncio.CancelledError:
            return False
        except Exception:
            return False
        return True

    async def ReadSocketData(self):
        try:
            header = await asyncio.wait_for(self._reader.read(4), timeout=35.0)
        except Exception:
            Printer().printer("与服务器连接断开", "Error", "red")
            self.connected = False
            return False
        if len(header) == 0:
            return False
        try:
            len_body, = self.header_struct.unpack_from(header)
        except:
            Printer().printer(f"unpack_from出现错误,header:{header} len(header):{len(header)}", "Error", "red")
            self.connected = False
            return False
        if not len_body:
            return False
        try:
            body = await self._reader.read(len_body - 4)
            Printer().printer(f"接收到服务器的header数据{header} body数据{body}", "DEBUG", "yellow")
        except Exception:
            Printer().printer("与服务器连接断开", "Error", "red")
            self.connected = False
            return False
        if body is None:
            return False
        try:
            body = body.decode('utf-8')
            body = body.replace("True", "true").replace("False", "false").replace("None", "null")
        except:
            Printer().printer(f"body.decode出现错误,body:{body}", "Error", "red")
            self.connected = False
            return False
        try:
            json_data = json.loads(body)
            await self.parseDanMu(json_data)
        except Exception:
            Printer().printer(f"json.loads出现错误,body:{body}", "Error", "red")
            self.connected = False
            return False
        return True

    async def ReceiveMessageLoop(self):
        while self.connected:
            tmp = await self.ReadSocketData()
            if not tmp:
                break

    async def parseDanMu(self, dic):

        cmd = dic.get('cmd')
        if cmd is None:
            Printer().printer(dic, "Error", "red")
            return
        if cmd == 'HeartBeat':
            pass
        elif cmd == 'Storm':
            pass
        elif cmd == 'Guard':
            pass
        elif cmd == 'PKLottery':
            pass
        elif cmd == 'Raffle':
            Rafflehandler().append2list_TV(dic["data"]["RoomId"])
        else:
            Printer().printer(dic, "Info", "green")
