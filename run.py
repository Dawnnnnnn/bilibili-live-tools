from OnlineHeart import OnlineHeart
from Silver import Silver
from Tasks import Tasks
from bilibiliCilent import bilibiliClient
import asyncio
task = OnlineHeart()
task1 = Silver()
task2 = Tasks()
danmuji = bilibiliClient()
tasks = [
    task.run(),
    task1.run(),
    task2.run(),
	danmuji.connectServer() ,
    danmuji.HeartbeatLoop(),
]

loop = asyncio.get_event_loop()

loop.run_until_complete(asyncio.wait(tasks))

loop.close()