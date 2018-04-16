from OnlineHeart import OnlineHeart
from Silver import Silver
from LotteryResult import LotteryResult
from Tasks import Tasks
from connect import connect
from rafflehandler import Rafflehandler
import asyncio
import utils
from printer import Printer
from statistics import Statistics
from bilibili import bilibili
import threading
import biliconsole



loop = asyncio.get_event_loop() 

# print('Hello world.')
printer = Printer()
bilibili()

# print('ok')

Statistics()

rafflehandler = Rafflehandler()


task = OnlineHeart()
task1 = Silver()
task2 = Tasks()
task3 = LotteryResult()
task4 = connect()


console_thread = threading.Thread(target=biliconsole.main)

console_thread.start()

loop = asyncio.get_event_loop() 
tasks = [
    utils.fetch_user_info(),
    utils.fetch_bag_list(),
    utils.fetch_medal(),

    task.run(), 
    task1.run(),
    task2.run(),
    task4.connect(),
    task3.query(),
    printer.clean_printlist(),
    rafflehandler.run()
    
]

loop.run_until_complete(asyncio.wait(tasks))
console_thread.join()

loop.close()
    


