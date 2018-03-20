# bilibili-live-tools

项目经过了一天的重构，能够运行一个文件实现大多数功能了，就是需要输入好多遍账号密码.....(会修复的，flag)

学业繁忙，准备弃坑咕咕咕，风暴初版已上传，不再更新后几版

//时隔多日打算学一下图形化，说不定会以这个项目作为样本(flag)

目前已完成：

        每日签到
        双端心跳领取经验
        领取银瓜子宝箱
        提交每日任务
        漫天花雨双端抽奖
        小电视PC端抽奖
        领取每日包裹奖励
        应援团签到
        实物抽奖(实验性)
        获取心跳礼物(实验性)
        节奏风暴领取(单文件实验性)


环境:
    
        python3.6

第三方库配置:

        pip install requests
        pip install rsa
        pip install aiohttp

更新说明(3.21):

        实物抽奖为实验性功能，只过滤了“测试”关键字，功能默认开启，风险在pull requests中有说明,
        如不想打开本功能，请用记事本编辑OnlineHeart.py文件的最后几行，将“self.draw_lottery()“这行删掉即可

使用方法：

        python run.py
    
        然后输入好几遍账号密码就行了233333

引用代码作者github:https://github.com/lyyyuna

本项目采用MIT开源协议




