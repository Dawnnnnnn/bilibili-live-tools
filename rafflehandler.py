import asyncio
import bilibiliCilent

class Rafflehandler:
    instance = None

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(Rafflehandler, cls).__new__(cls, *args, **kw)
            cls.instance.list_activity = []
            cls.instance.list_TV = []
        return cls.instance
        
    async def run(self):
        while True:
            len_list_activity = len(self.list_activity)
            len_list_TV = len(self.list_TV)
            
            #print('准备执行')

            # 过滤相同房间
            # set_activity = set(self.list_activity)
            set_activity = []
            for i in self.list_activity:
                if i not in set_activity:
                    set_activity.append(i)
            set_TV = set(self.list_TV)
            #print('过滤完毕')
            #if len(set_activity) != len_list_activity or len(set_TV) != len_list_TV:
                #print('过滤机制起作用')
            
            tasklist = []
            for i in set_TV:
                task = asyncio.ensure_future(bilibiliCilent.handle_1_room_TV(i))
                tasklist.append(task)
            for i in set_activity:
                task = asyncio.ensure_future(bilibiliCilent.handle_1_room_activity(i[0], i[1], i[2]))
                tasklist.append(task)
            if tasklist:  
                await asyncio.wait(tasklist, return_when=asyncio.ALL_COMPLETED)
                #print('本批次结束')
            else:
                #print('本批次轮空')
                pass
                
            del self.list_activity[:len_list_activity]
            del self.list_TV[:len_list_TV]
            if len_list_activity == 0 and len_list_TV == 0:
                await asyncio.sleep(5)
            else:
                await asyncio.sleep(1)
            
            
            
    def append2list_TV(self, real_roomid):
        #print('welcome to appending') 
        self.list_TV.append(real_roomid)
        #print('appended TV')
        return
        
    def append2list_activity(self, giftId, text1, text2):
        #print('welcome to appending') 
        self.list_activity.append([giftId, text1, text2])
        #print('appended activity')
        return
        
         
