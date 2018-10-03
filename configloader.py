import configparser
import codecs

def load_bilibili(file):
    cf_bilibili = configparser.ConfigParser()
    cf_bilibili.optionxform = str
    cf_bilibili.read_file(codecs.open(file, "r", "utf8"))
    dic_bilibili = cf_bilibili._sections
    dic_nomalised_bilibili = dic_bilibili['normal'].copy()
    dic_nomalised_bilibili['saved-session'] = dic_bilibili['saved-session'].copy()
    dic_nomalised_bilibili['account'] = dic_bilibili['account'].copy()
    if dic_nomalised_bilibili['account']['username']:
        pass
    else:
        username = input("# 输入帐号: ")
        password = input("# 输入密码: ")
        cf_bilibili.set('account', 'username', username)
        cf_bilibili.set('account', 'password', password)
        cf_bilibili.write(codecs.open(file, "w+", "utf8"))
        dic_nomalised_bilibili['account']['username'] = username
        dic_nomalised_bilibili['account']['password'] = password
    dic_bilibili_type = dic_bilibili['types']
    # str to int
    for i in dic_bilibili_type['int'].split():
        dic_nomalised_bilibili[i] = int(dic_bilibili['normal'][i])
    for i in dic_bilibili.keys():
        # print(i)
        if i[0:3] == 'dic':
            dic_nomalised_bilibili[i[4:]] = dic_bilibili[i]
    return dic_nomalised_bilibili




def load_user(file):
    cf_user = configparser.ConfigParser()
    cf_user.read_file(codecs.open(file, "r", "utf8"))
    dic_user = cf_user._sections
    return dic_user


def write2bilibili(dic):
    cf_bilibili = configparser.ConfigParser(interpolation=None)
    cf_bilibili.optionxform = str

    cf_bilibili.read_file(codecs.open("conf/bilibili.conf", "r", "utf8"))

    for i in dic.keys():
        cf_bilibili.set('saved-session', i, dic[i])

    cf_bilibili.write(codecs.open("conf/bilibili.conf", "w+", "utf8"))
