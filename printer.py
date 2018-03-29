try:
    import console
except ImportError:
    pass
import webcolors


# "#969696"
def hex_to_rgb_percent(hex_str):
    color = webcolors.hex_to_rgb_percent(hex_str)
    # print([float(i.strip('%'))/100.0 for i in color])
    return [float(i.strip('%'))/100.0 for i in color]
 
class Printer():
    def __init__(self, configloader):
        self.configloader = configloader
    def concole_print(self, msg, color=[]):
        if color:
            for i, j in zip(msg, color):
                console.set_color(*j)
                print(i, end='')
            print()
            console.set_color()
        else:
            print(''.join(msg))    
    
        
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
                    # self.rgbprint(self.configloader.dic_color['others']['vip'], '爷')
                    list_msg.append('爷 ')
                    list_color.append(self.configloader.dic_color['others']['vip'])
                else:
                    # self.rgbprint(self.configloader.dic_color['others']['svip'], '爷')
                    list_msg.append('爷 ')
                    list_color.append(self.configloader.dic_color['others']['svip'])
            if info[2][2] == 1:
                # self.rgbprint(self.configloader.dic_color['others']['admin'], '房管')
                list_msg.append('房管 ')
                list_color.append(self.configloader.dic_color['others']['admin'])
                
            # 勋章
            if info[3]:
                list_color.append(self.configloader.dic_color['fans-level']['fl' + str(info[3][0])])
                list_msg.append(info[3][1] + '|' + str(info[3][0]) + ' ')              
            # 等级
            if not info[5]:
                list_color.append(self.configloader.dic_color['user-level']['ul' + str(info[4][0])])
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
        if (self.configloader.dic_user['platform']['platform'] == 'ios_pythonista'):
            self.concole_print(list_msg, list_color)
        else:
            self.concole_print(list_msg)
        
        
        


