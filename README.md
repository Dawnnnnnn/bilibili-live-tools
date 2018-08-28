# bilibili-live-tools


同级项目开坑: https://github.com/Dawnnnnnn/bilibili-tools

开放识别登录验证码接口:

        POST API:http://47.95.255.188:5000/code
        data = {"image":base64.b64decode(response.content)}
        1g1h1m学生机，慢点请求......

目前已完成：
------

        每日签到
        cookie过期刷新
        双端心跳领取经验
        领取银瓜子宝箱
        提交每日任务
        C位抽奖
        摩天大楼全站抽奖
        小电视PC端抽奖
        领取每日包裹奖励
        应援团签到
        获取心跳礼物
        获取全站上船奖励
        实物抽奖
        清空当日到期礼物
        根据亲密度赠送礼物
        银瓜子硬币双向兑换
        云端验证码识别


环境:
------  
        python3.6


使用方法:
------

        看Wiki

        ---

        Docker快速启动

        docker run -itd --rm -e USER_NAME=你的B站账号 -e USER_PASSWORD=你的B站密码 zsnmwy/bilibili-live-tools

        -it  # 不后台
        -itd # 后台


因主项目追求稳定和兼容性,故删除了些个人认为不太实用的功能,保留下来了tools的一些常见基本功能,用于在服务器上长时间挂机。

另一个作者的项目分支: https://github.com/yjqiang/bilibili-live-tools
此分支为创新较多的版本,集成了弹幕姬等特性,作者也更新频繁,喜欢多尝试的用户可以使用该分支

感谢:https://github.com/lyyyuna

感谢:https://github.com/lkeme/BiliHelper

感谢:https://github.com/czp3009/bilibili-api

感谢:https://github.com/lzghzr/bilive_client


本项目采用MIT开源协议
