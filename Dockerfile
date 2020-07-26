FROM python:3.7-alpine
MAINTAINER Dawnnnnnn <1050596704@qq.com>

ENV LIBRARY_PATH=/lib:/usr/lib \
    USER_NAME='' \
    USER_PASSWORD=''

WORKDIR /app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
	echo "Asia/Shanghai" > /etc/timezone && \
	apk del tzdata && \
    apk add --no-cache build-base git && \
    git clone https://github.com/Dawnnnnnn/bilibili-live-tools.git /app && \
    pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    rm -r /var/cache/apk && \
    rm -r /usr/share/man

ENTRYPOINT git pull && \
            pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/ && \
            sed -i ''"$(cat conf/bilibili.conf -n | grep "username =" | awk '{print $1}')"'c '"$(echo "username = ${USER_NAME}")"'' conf/bilibili.conf && \
            sed -i ''"$(cat conf/bilibili.conf -n | grep "password =" | awk '{print $1}')"'c '"$(echo "password = ${USER_PASSWORD}")"'' conf/bilibili.conf && \
            python ./run.py