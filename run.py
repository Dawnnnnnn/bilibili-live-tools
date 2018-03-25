from OnlineHeart import OnlineHeart
from Silver import Silver
from LotteryResult import LotteryResult
from Tasks import Tasks
from bilibiliCilent import bilibiliClient
from login import Login
import asyncio
from API import API
login = Login().success()
API.user_info()
API.get_bag_list()
task = OnlineHeart()
task1 = Silver()
task2 = Tasks()
danmuji = bilibiliClient()
task3 = LotteryResult()

tasks = [
    task.run(),
    task1.run(),
    task2.run(),
    danmuji.connectServer(),
    danmuji.HeartbeatLoop(),
    task3.query()
]

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait(tasks))

loop.close()
