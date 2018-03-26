import webcolors
import console
import configparser

class printf:
    def __init__(self):
        cf = configparser.ConfigParser()
        cf.read("color.conf")
        self.configparser = cf
        print("初始化")


    # "#969696"
    def hex_print(self, hex_str, str, end=' '):
        # print(str)
        color = webcolors.hex_to_rgb_percent(hex_str)
        console.set_color(*[float(i.strip('%'))/100.0 for i in color])
        print(str, end=end)
        console.set_color()

        # "255 255 255"
    def rgb_print(self, rgb_str, str, end=' '):
        # print(str)
        color = webcolors.rgb_to_rgb_percent(rgb_str)
        console.set_color(*[float(i.strip('%'))/100.0 for i in color])
        print(str, end=end)
        console.set_color()
        
    def print_danmu_msg(self, dic):
        # print(dic)
        info = dic['info']
        tmp = dic['info'][2][1] + ':' + dic['info'][1]
        if info[7] == 3:
            print('舰', end=' ')
        else:
            if info[2][3] == 1:
                if info[2][4] == 0:
                    color = self.configparser.get('others', 'vip')
                    self.rgb_print(color, '爷')
                else:
                    color = self.configparser.get('others', 'vip')
                    self.rgb_print(color, '爷')
            if info[2][2] == 1:
                color = self.configparser.get('others', 'admin')
                self.hex_print(color, '房管')
            # 勋章
            if info[3]:
                color = self.configparser.get('fans-level','fl' + str(info[3][0]))
                self.hex_print(color, info[3][1] + '|' + str(info[3][0]))                
            # 等级
            if not info[5]:
                color = self.configparser.get('user-level','ul' + str(info[4][0]))
                self.hex_print(color, 'UL' + str(info[4][0]))
        if info[2][7] != '':
            self.hex_print(info[2][7],dic['info'][2][1], '')
        else:
            print(dic['info'][2][1], end='')
        print(':' + dic['info'][1]) 

