from statistics import Statistics
import requests
import asyncio
import time


class LotteryResult():

    async def query(self):
        
        while 1:
            # print('lotteryresult test')
            await Statistics().clean_activity()

            await Statistics().clean_TV()
            
            
            # print('自动延迟参数', sleeptime1, sleeptime2)
            await asyncio.sleep(30) 
            '''
            if sleeptime1 != None and sleeptime2 != None:
                # print(sleeptime1, sleeptime2)            
                await asyncio.sleep(min(sleeptime1, sleeptime2))
            elif sleeptime1 == None and sleeptime2 == None:
                await asyncio.sleep(60) 
            elif sleeptime1 != None:
                # print(sleeptime1)
                await asyncio.sleep(sleeptime1)
            else:
                # print(sleeptime2)
                await asyncio.sleep(sleeptime2)
 '''
