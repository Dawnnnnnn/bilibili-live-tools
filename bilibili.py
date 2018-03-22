class bilibili():
    appkey = '1d8b6e7d45233436'
    actionKey = 'appkey'
    build = '520001'
    device = 'android'
    mobi_app = 'android'
    platform = 'android'
    app_secret = '560c52ccd288fed045859ed18bffd973'
    access_key = ""
    cookie = ""
    pcheaders = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'accept-encoding': 'gzip, deflate',
        'Host': 'api.live.bilibili.com',
        'cookie': cookie
    }
    appheaders = {
        "User-Agent": "bili-universal/6570 CFNetwork/894 Darwin/17.4.0",
        "Accept-encoding": "gzip",
        "Buvid": "000ce0b9b9b4e342ad4f421bcae5e0ce",
        "Display-ID": "146771405-1521008435",
        "Accept-Language": "zh-CN",
        "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
        "Connection": "keep-alive",
        "Host": "api.live.bilibili.com",
        'cookie': cookie
    }
    _CIDInfoUrl = 'http://live.bilibili.com/api/player?id=cid:'
    _ChatPort = 2243
    _protocolversion = 1
    _reader = 0
    _writer = 0
    connected = False
    _UserCount = 0
    _ChatHost = 'livecmt-2.bilibili.com'
    _roomId = int(3108569)
    activity_raffleid_list = []
    activity_roomid_list = []
    activity_time_list = []
    TV_raffleid_list = []
    TV_roomid_list = []
    TV_time_list = []


