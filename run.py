import utils
from TCP_monitor import TCP_monitor
from OnlineHeart import OnlineHeart
from LotteryResult import LotteryResult
from Tasks import Tasks
from connect import connect
from rafflehandler import Rafflehandler
import asyncio
from login import login
from printer import Printer
from statistics import Statistics
from bilibili import bilibili
import threading
import biliconsole
from schedule import Schedule
import configloader
import os

fileDir = os.path.dirname(os.path.realpath('__file__'))
file_user = fileDir + "/conf/user.conf"
dic_user = configloader.load_user(file_user)


loop = asyncio.get_event_loop()
printer = Printer(dic_user['thoroughly_log']['on/off'])
bilibili()
Statistics()
rafflehandler = Rafflehandler()
biliconsole.Biliconsole()

task = OnlineHeart()
task2 = Tasks()
task3 = LotteryResult()
task4 = connect()

tasks1 = [
    login().login_new()
]
loop.run_until_complete(asyncio.wait(tasks1))

console_thread = threading.Thread(target=biliconsole.controler)
console_thread.start()



tasks = [
    task.run(),
    task2.run(),
    biliconsole.Biliconsole().run(),
    task4.create(),
    task3.query(),
    rafflehandler.run(),
]


if dic_user['monitoy_server']['on/off'] == "1":
    monitor = TCP_monitor()
    task_tcp_conn = monitor.connectServer(
        dic_user['monitoy_server']['host'], dic_user['monitoy_server']['port'], dic_user['monitoy_server']['key'])
    task_tcp_heart = monitor.HeartbeatLoop()
    tasks.append(task_tcp_conn)
    tasks.append(task_tcp_heart)

schedule = Schedule()
if dic_user['regular_sleep']['on/off'] == "1":
    tasks.append(schedule.run(dic_user['regular_sleep']['schedule']))
    Schedule().scheduled_sleep = True


tasks = list(map(asyncio.ensure_future, tasks))
loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION))
Printer().printer('\n'.join(map(repr, asyncio.Task.all_tasks())), "Info", "green")
for task in tasks:
    Printer().printer(repr(task._state), "Info", "green")
    if task._state == 'FINISHED':
        Printer().printer(f"Task err: {repr(task.exception())}", "Error", "red")
loop.close()

console_thread.join()
