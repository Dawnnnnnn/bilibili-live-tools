from OnlineHeart import OnlineHeart
from Silver import Silver
from LotteryResult import LotteryResult
from Tasks import Tasks
from connect import connect
import asyncio
import utils
from printer import Printer
from statistics import Statistics
from bilibili import bilibili
import threading
import biliconsole


# print('Hello world.')
printer = Printer()
bilibili()
Statistics()

utils.fetch_user_info()
utils.fetch_bag_list()
utils.fetch_medal()



task = OnlineHeart()
task1 = Silver()
task2 = Tasks()
task3 = LotteryResult()
task4 = connect()


def main(loop):  
    tasks = [
        task.run(),
        task1.run(),
        task2.run(),
        task4.connect(),
        task3.query(),
        printer.clean_printlist()
    ]
    
    asyncio.set_event_loop(loop)
    
    loop.run_until_complete(asyncio.wait(tasks))
    
    loop.close()
    

        
loop = asyncio.get_event_loop()        
mainthread = threading.Thread(target=main, args=(loop,))
controlthread = threading.Thread(target=biliconsole.controler)

mainthread.start()
controlthread.start()

mainthread.join()
controlthread.join()

