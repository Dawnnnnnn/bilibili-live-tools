# bilibili-live-tools

这是一个最近才开始做的python项目，只是为了学习点东西....,大概才做了一个星期



目前已完成：

    自动每日签到
    自动app端心跳领取直播经验
    自动pc端心跳领取直播经验
    自动领取每日银瓜子
    自动领取每日任务奖励
    双端观看直播五分钟
    火力全开双端抽奖
    小电视PC端抽奖
    自动领取每日包裹奖励
    分享直播间任务
目前未完成：

    app端登陆
    pc端登陆
    应援团自动签到
    
    

环境:python3.6

第三方库配置:


pip install requests


pip install aiohttp

使用 python xxx.py 运行

抽奖的脚本使用python main.py 执行

因为登陆的流程还没有写好，所以access_key和cookies需要自己获得,这里提供一个大佬的两个网站，方便用户获取这两个参数

https://api.kaaass.net/biliapi/docs/?file=03-%E7%94%A8%E6%88%B7%E7%9B%B8%E5%85%B3/001-Bilibili%E7%99%BB%E5%BD%95%EF%BC%88access_key%EF%BC%89



https://api.kaaass.net/biliapi/docs/?file=03-%E7%94%A8%E6%88%B7%E7%9B%B8%E5%85%B3/004-%E7%94%B1access_key%E7%94%9F%E6%88%90%E4%B8%BB%E7%AB%99cookie
(右上角有个测试接口看到了吗23333)

引用代码作者github:https://github.com/lyyyuna


因为作者十分的菜，所以希望有大佬改进代码，不然只能自己瞎鸡儿用了...目前还是单文件单功能的样子呢



