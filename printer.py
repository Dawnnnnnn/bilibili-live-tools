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
        
    def rgbprint(self, rgb, msg, end=' '):
        console.set_color(*rgb)
        print(msg, end=end)
        console.set_color()
    
    def normalprint(self, msg, end='\n'):
        print(msg, end=end)
        
    def print_danmu_msg_ios(self, dic):
        info = dic['info']
        # tmp = dic['info'][2][1] + ':' + dic['info'][1]
        if info[7] == 3:
            print('舰', end=' ')
        else:
            if info[2][3] == 1:
                if info[2][4] == 0:
                    self.rgbprint(self.configloader.dic_color['others']['vip'], '爷')
                    # color = self.configparser.get('others', 'vip')
                    # self.rgb_print(color, '爷')
                else:
                    self.rgbprint(self.configloader.dic_color['others']['svip'], '爷')
                    # color = self.configparser.get('others', 'svip')
                    # self.rgb_print(color, '爷')
            if info[2][2] == 1:
                self.rgbprint(self.configloader.dic_color['others']['admin'], '房管')
                # color = self.configparser.get('others', 'admin')
                # self.hex_print(color, '房管')
            # 勋章
            if info[3]:
                self.rgbprint(self.configloader.dic_color['fans-level']['fl' + str(info[3][0])], info[3][1] + '|' + str(info[3][0])) 
                # color = self.configparser.get('fans-level','fl' + str(info[3][0]))
                # self.hex_print(color, info[3][1] + '|' + str(info[3][0]))                
            # 等级
            if not info[5]:
                self.rgbprint(self.configloader.dic_color['user-level']['ul' + str(info[4][0])], 'UL' + str(info[4][0]))
                # color = self.configparser.get('user-level','ul' + str(info[4][0]))
                # self.hex_print(color, 'UL' + str(info[4][0]))
        if info[2][7] != '':
            self.rgbprint(hex_to_rgb_percent(info[2][7]), info[2][1], '')
            # self.hex_print(info[2][7],dic['info'][2][1], '')
        else:
            self.normalprint(dic['info'][2][1], end='')
        self.normalprint(':' + dic['info'][1])
    
    def print_danmu_msg_other(self, dic):
        info = dic['info']
        # print(dic)
        tmp = dic['info'][2][1] + ':' + dic['info'][1]
        if info[7] == 3:
            self.normalprint('舰', end=' ')
        else:
            if info[2][3] == 1:
                if info[2][4] == 0:
                    # tmp = '爷 ' + tmp
                    self.normalprint('月爷', end=' ')
                else:
                    self.normalprint('年老', end=' ')
            if info[2][2] == 1:
                self.normalprint('房管', end=' ')
            # 勋章
            if info[3]:
                self.normalprint(info[3][1] + '|' + str(info[3][0]), end=' ')
            # 等级
            if not info[5]:
                self.normalprint('UL' + str(info[4][0]), end=' ')
        self.normalprint(tmp)
        
    def print_danmu_msg(self, dic):
        if (self.configloader.dic_user['platform']['platform'] == 'ios_pythonista'):
            self.print_danmu_msg_ios(dic)
        else:
            self.print_danmu_msg_other(dic)

