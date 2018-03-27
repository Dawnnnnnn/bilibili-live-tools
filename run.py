from OnlineHeart import OnlineHeart
from Silver import Silver
from LotteryResult import LotteryResult
from Tasks import Tasks
from login import Login
from connect import connect
import asyncio
from API import API


login = Login().success()
API.user_info()
API.get_bag_list()
API.send_danmu_msg_web("我是弹幕测试呀", roomid)
task = OnlineHeart()
task1 = Silver()
task2 = Tasks()
task3 = LotteryResult()
task4 = connect()

tasks = [
    task.run(),
    task1.run(),
    task2.run(),
    task4.connect(),
    task3.query()
]

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait(tasks))

loop.close()

