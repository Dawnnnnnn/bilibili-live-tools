from configloader import ConfigLoader


class bilibili():
    def __init__(self, configloader):
        for i, j in configloader.dic_bilibili.items():
            exec("self." + i + '=j')
        # print(self.appkey)

# configloader = ConfigLoader("color.conf", "user.conf", "bilibili.conf")
# bilibili(configloader)
