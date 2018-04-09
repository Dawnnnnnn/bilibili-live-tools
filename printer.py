try:
    import console
except ImportError:
    pass
import webcolors
import asyncio
import os
import configloader

# "#969696"
def hex_to_rgb_percent(hex_str):
    color = webcolors.hex_to_rgb_percent(hex_str)
    # print([float(i.strip('%'))/100.0 for i in color])
    return [float(i.strip('%'))/100.0 for i in color]
 

def level(str):
    if str == "user":
        return 0
    if str == "debug":
        return 1


class Printer():       
    instance = None

    def __new__(cls, *args, **kw):
        if not cls.instance:
            cls.instance = super(Printer, cls).__new__(cls, *args, **kw)
            fileDir = os.path.dirname(os.path.realpath('__file__'))
            file_color = fileDir + "/conf/color.conf"
            cls.instance.dic_color = configloader.load_color(file_color)
            file_user = fileDir + "/conf/user.conf"
            cls.instance.dic_user = configloader.load_user(file_user)
            cls.instance.printlist=[]
        return cls.instance
    def concole_print(self, msg, color=[]):
        if color:
            for i, j in zip(msg, color):
                console.set_color(*j)
                print(i, end='')
            print()
            console.set_color()
        else:
            print(''.join(msg))  
              
    def printlist_append(self, dic):
        tag = False
        dic_printcontrol = self.dic_user['print_control']
        if dic[0] in dic_printcontrol.keys():
            if dic_printcontrol[dic[0]] >= level(dic[2]):
                tag = True
                if dic[1] in dic_printcontrol.keys():
                    tag = dic_printcontrol[dic[1]]
        if tag:
            if dic[1] == '弹幕':
                list_msg, list_color = self.print_danmu_msg(dic[3]) 
                self.printlist.append([0, list_msg, list_color])
                return 
            
            if isinstance(dic[3], list):
              #  print(dic[3])
                # [[list]]
                self.printlist.append([dic[3]])
            else:
               # print(dic[3:])
                # [ss, ss]
                self.printlist.append(dic[3:])
        
    async def clean_printlist(self):
        
        while True:
            for i in self.printlist:
                if i[0] == 0:
                    if (self.dic_user['platform']['platform'] == 'ios_pythonista'):
                        self.concole_print(i[1], i[2])
                    else:
                        self.concole_print(i[1])
        
                    
                elif isinstance(i[0], list):
                    for j in i[0]:
                        print(j)
                else:
                    print(' '.join(i))
            self.printlist=[]
            await asyncio.sleep(0.1)
                        
            
            
        
    def print_danmu_msg(self, dic):
        info = dic['info']
        # tmp = dic['info'][2][1] + ':' + dic['info'][1]
        list_msg = []
        list_color =[]
        if info[7] == 3:
            # print('舰', end=' ')
            list_msg.append('⚓️ ')
            list_color.append([])
        else:
            if info[2][3] == 1:
                if info[2][4] == 0:
                    list_msg.append('爷 ')
                    list_color.append(self.dic_color['others']['vip'])
                else:
                    list_msg.append('爷 ')
                    list_color.append(self.dic_color['others']['svip'])
            if info[2][2] == 1:
                list_msg.append('房管 ')
                list_color.append(self.dic_color['others']['admin'])
                
            # 勋章
            if info[3]:
                list_color.append(self.dic_color['fans-level']['fl' + str(info[3][0])])
                list_msg.append(info[3][1] + '|' + str(info[3][0]) + ' ')              
            # 等级
            if not info[5]:
                list_color.append(self.dic_color['user-level']['ul' + str(info[4][0])])
                list_msg.append('UL' + str(info[4][0]) + ' ')
        try:
            if info[2][7] != '': 
                list_color.append(hex_to_rgb_percent(info[2][7]))
                list_msg.append(info[2][1])
            else:
                list_msg.append(info[2][1])    
                list_color.append([])
            # print(info)
        except :
            print("# 小电视降临本直播间")
            list_msg.append(info[2][1])    
            list_color.append([])
            
        list_msg.append(':' + info[1])
        list_color.append([])
        return list_msg, list_color
            

        
        
        


