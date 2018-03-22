# bilibili-live-tools


项目又经过了一天的重构。差不多能当python课设交上去了(´；ω；`)

学业繁忙，准备弃坑咕咕咕(flag)，风暴初版已上传，不再更新后几版

//时隔多日打算学一下图形化，说不定会以这个项目作为样本(flag)


目前已完成：
------

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
        
更新说明
------

3.21:
        
    实物抽奖为实验性功能，只过滤了“测试”关键字，功能默认开启，风险在pull requests中有说明,
    如不想打开本功能，请用记事本编辑OnlineHeart.py文件的最后几行，将“self.draw_lottery()“这行删掉即可

3.22:
        
>   在 [Shadow-D](https://github.com/Shadow-D)大佬的指导下，重新写了父类，实现了输入一次账密通用cookie的功能，
    同时加上了获取pc端抽奖结果的功能
    
3.23:

    紧急修复部分账号PC端参与小电视抽奖异常的bug



环境:
------  
        python3.6

第三方库配置:
------

        pip install requests
        pip install rsa
        pip install aiohttp


使用方法：
------

       第一种:
             自行按照百度配置python运行环境,并安装所需第三方库,最后执行python run.py
       第二种:
             下载release中的exe版本,双击运行
             
         
        
    


引用代码作者github:https://github.com/lyyyuna

本项目采用MIT开源协议



