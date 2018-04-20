# bilibili-live-tools


项目又经过了一天的重构。差不多能当python课设交上去了(´；ω；`)

学业繁忙，准备弃坑咕咕咕(flag)，风暴初版已上传，不再更新后几版

//时隔多日打算学一下图形化，说不定会以这个项目作为样本(flag)


开放识别登录验证码接口:

        POST API:http://101.236.6.31:8080/code
        data = {"image":base64.b64decode(response.content)}
        1g1h1m学生机，慢点请求......

目前已完成：
------

        每日签到
        cookie过期刷新
        双端心跳领取经验
        领取银瓜子宝箱
        提交每日任务
        漫天花雨双端抽奖
        小电视PC端抽奖
        领取每日包裹奖励
        应援团签到
        获取心跳礼物
        获取总督开通奖励
        实物抽奖
        清空当日到期礼物
        根据亲密度赠送礼物
        银瓜子硬币双向兑换
        云端验证码识别


环境:
------  
        python3.6
  
    
修bug群:没了

因主项目追求稳定和兼容性,故删除了些个人认为不太实用的功能,保留下来了tools的一些常见基本功能,用于在服务器上长时间挂机。

另一个作者的项目分支: https://github.com/yjqiang/bilibili-live-tools
此分支为创新较多的版本,集成了弹幕姬等特性,作者也更新频繁,喜欢多尝试的用户可以使用该分支

感谢:https://github.com/lyyyuna

感谢:https://github.com/lkeme/BiliHelper

感谢:https://github.com/czp3009/bilibili-api

感谢:https://github.com/lzghzr/bilive_client


本项目采用MIT开源协议
