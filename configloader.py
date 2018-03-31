import configparser
import webcolors
import codecs

# "#969696"
def hex_to_rgb_percent(hex_str):
    color = webcolors.hex_to_rgb_percent(hex_str)
    # print([float(i.strip('%'))/100.0 for i in color])
    return [float(i.strip('%'))/100.0 for i in color]
    

# "255 255 255"
def rgb_to_percent(rgb_str):
    color = webcolors.rgb_to_rgb_percent(map(int, rgb_str.split()))
    # print([float(i.strip('%'))/100.0 for i in color])
    return [float(i.strip('%'))/100.0 for i in color]

    
class ConfigLoader():
    
    def __init__(self, colorfile, userfile, bilibilifile):
        self.dic_color = self.load_color(colorfile)
        # print(self.dic_color)
        
        self.dic_user = self.load_user(userfile)
        # print(self.dic_user)
        
        self.dic_bilibili = self.load_bilibili(bilibilifile)
        # print(self.dic_bilibili)
        print("# 初始化完成")
        
    def load_bilibili(self, file):
        cf_bilibili = configparser.ConfigParser()
        cf_bilibili.optionxform = str
        # cf_bilibili.read(file)
        cf_bilibili.read_file(codecs.open(file, "r", "utf8"))
        dic_bilibili = cf_bilibili._sections
        # print(dic_bilibili)
                
        dic_nomalised_bilibili = dic_bilibili['normal'].copy()
        # print(dic_nomalised_bilibili)
        
        dic_bilibili_type = dic_bilibili['types']
        # str to int
        for i in dic_bilibili_type['int'].split():
            # print(dic_bilibili['other'][i])
            dic_nomalised_bilibili[i] = int(dic_bilibili['normal'][i])
            
        # str to bool
        for i in dic_bilibili_type['bool'].split():
            # print(i)
            dic_nomalised_bilibili[i] = True if dic_bilibili['normal'][i] == 'True' else False

        # str to bool
        for i in dic_bilibili_type['list'].split():
            # print(i)
            dic_nomalised_bilibili[i] = []
               
        # print(dic_nomalised_bilibili)
        # str to dic
        for i in dic_bilibili.keys():
            # print(i)
            if i[0:3] == 'dic':
                dic_nomalised_bilibili[i[4:]] = dic_bilibili[i]
                
        # print(dic_nomalised_bilibili['connected'])
        # print(dic_nomalised_bilibili['pcheaders']['Host'])
        return dic_nomalised_bilibili
        
    def load_color(self, file):
        cf_color = configparser.ConfigParser()
        # cf_color.read(file)
        cf_color.read_file(codecs.open(file, "r", "utf8"))

        dic_color = cf_color._sections
        for i in dic_color.values():
            for j in i.keys():
                # print(i[j])
                if i[j][0] == '#':
                    i[j] = hex_to_rgb_percent(i[j])
                else:
                    i[j] = rgb_to_percent(i[j])
                    
        # print(dic_color['user-level']['ul0'])
        return dic_color
        
    def load_user(self, file):
        cf_user = configparser.ConfigParser()
        # cf_user.read(file)
        cf_user.read_file(codecs.open(file, "r", "utf8"))
        # print(cf_user._sections['platform']['platform'])
        return cf_user._sections
        

# configloader = ConfigLoader("color.conf", "user.conf", "bilibili.conf")
