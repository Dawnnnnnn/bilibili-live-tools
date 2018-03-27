import configparser
import webcolors


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
    
    def __init__(self, colorfile, userfile):
        cf_color = configparser.ConfigParser()
        cf_color.read(colorfile)
        self.dic_color = cf_color._sections
        
        cf_user = configparser.ConfigParser()
        cf_user.read(userfile)
        self.dic_user = cf_user._sections        
        # print(dic_color['user-level'])
        
        for i in self.dic_color.values():
            for j in i.keys():
                # print(i[j])
                if i[j][0] == '#':
                    i[j] = hex_to_rgb_percent(i[j])
                else:
                    i[j] = rgb_to_percent(i[j])
                    
        print("# 初始化完成")
  
