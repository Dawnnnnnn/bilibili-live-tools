from statistics import Statistics
import asyncio


class LotteryResult():

    async def query(self):
        while 1:
            await Statistics().clean_activity()

            await Statistics().clean_TV()

            await asyncio.sleep(30)
