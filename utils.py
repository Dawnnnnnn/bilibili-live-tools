from bilibili import bilibili
import time
import datetime
import math

def adjust_for_chinese(str):
    SPACE = '\N{IDEOGRAPHIC SPACE}'
    EXCLA = '\N{FULLWIDTH EXCLAMATION MARK}'
    TILDE = '\N{FULLWIDTH TILDE}'

    # strings of ASCII and full-width characters (same order)
    west = ''.join(chr(i) for i in range(ord(' '), ord('~')))
    east = SPACE + ''.join(chr(i) for i in range(ord(EXCLA), ord(TILDE)))

    # build the translation table
    full = str.maketrans(west, east)
    str = str.translate(full).rstrip().split('\n')
    md = '{:^10}'.format(str[0])
    return md.translate(full)

def CurrentTime():
    currenttime = int(time.mktime(datetime.datetime.now().timetuple()))
    return str(currenttime)


def fetch_medal():
    print('{} {} {:^12} {:^10} {} {:^6} '.format(adjust_for_chinese('勋章'), adjust_for_chinese('主播昵称'), '亲密度', '今日的亲密度',
                                                 adjust_for_chinese('排名'), '勋章状态'))
    dic_worn = {'1': '正在佩戴', '0': '待机状态'}
    response = bilibili().request_fetchmedal()
    # print(response.json())
    json_response = response.json()
    if json_response['code'] == 0:
        for i in json_response['data']['fansMedalList']:
            print('{} {} {:^14} {:^14} {} {:^6} '.format(adjust_for_chinese(i['medal_name'] + '|' + str(i['level'])),
                                                         adjust_for_chinese(i['anchorInfo']['uname']),
                                                         str(i['intimacy']) + '/' + str(i['next_intimacy']),
                                                         str(i['todayFeed']) + '/' + str(i['dayLimit']),
                                                         adjust_for_chinese(str(i['rank'])),
                                                         dic_worn[str(i['status'])]))

def send_danmu_msg_andriod(msg, roomId):
    response = bilibili().request_send_danmu_msg_andriod(msg, roomId)
    print(response.json())

def send_danmu_msg_web(msg, roomId):
    response = bilibili().request_send_danmu_msg_web(msg, roomId)
    print(response.json())

def fetch_user_info():
    response = bilibili().request_fetch_user_info()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '查询用户信息')
    if (response.json()['code'] == 0):
        uname = response.json()['data']['userInfo']['uname']
        achieve = response.json()['data']['achieves']
        user_level = response.json()['data']['userCoinIfo']['user_level']
        silver = response.json()['data']['userCoinIfo']['silver']
        gold = response.json()['data']['userCoinIfo']['gold']
        user_next_level = response.json()['data']['userCoinIfo']['user_next_level']
        user_intimacy = response.json()['data']['userCoinIfo']['user_intimacy']
        user_next_intimacy = response.json()['data']['userCoinIfo']['user_next_intimacy']
        user_level_rank = response.json()['data']['userCoinIfo']['user_level_rank']
        billCoin = response.json()['data']['userCoinIfo']['coins']
        print('# 用户名', uname)
        print('# 银瓜子', silver)
        print('# 金瓜子', gold)
        print('# 硬币数', billCoin)
        print('# 成就值', achieve)
        print('# 等级值', user_level, '———>', user_next_level)
        print('# 经验值', user_intimacy)
        print('# 剩余值', user_next_intimacy - user_intimacy)
        arrow = int(user_intimacy * 30 / user_next_intimacy)
        line = 30 - arrow
        percent = user_intimacy / user_next_intimacy * 100.0
        process_bar = '[' + '>' * arrow + '-' * line + ']' + '%.2f' % percent + '%'
        print(process_bar)
        print('# 等级榜', user_level_rank)

def fetch_bag_list():
    response = bilibili().request_fetch_bag_list()
    temp = []
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), '查询可用礼物')
    for i in range(len(response.json()['data']['list'])):
        bag_id = (response.json()['data']['list'][i]['bag_id'])
        gift_id = (response.json()['data']['list'][i]['gift_id'])
        gift_num = str((response.json()['data']['list'][i]['gift_num'])).center(4)
        gift_name = response.json()['data']['list'][i]['gift_name']
        expireat = (response.json()['data']['list'][i]['expire_at'])
        left_time = (expireat - int(CurrentTime()))
        left_days = (expireat - int(CurrentTime())) / 86400
        print("# " + gift_name + 'X' + gift_num, '(在' + str(math.ceil(left_days)) + '天后过期)')
        if 0 < int(left_time) < 43200:   # 剩余时间少于半天时自动送礼
            temp.append([gift_id, gift_num, bag_id])
    return temp