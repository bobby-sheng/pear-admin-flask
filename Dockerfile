FROM python:3.7-alpine

COPY . /app/

WORKDIR /app/

ENV TIME_ZONE Asia/Shanghai
ENV PIPURL "https://pypi.tuna.tsinghua.edu.cn/simple/ --trusted-host pypi.douban.com"

RUN apk update \
    && apk add --virtual mysqlclient-build gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-dev \
    && apk add --virtual system-build linux-headers libffi-dev \
    && apk add --no-cache jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
    && apk add --no-cache bash bash-doc bash-completion \
    && apk add --no-cache libxslt-dev tzdata g++
RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime
RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip \
    && pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt \
    && pip --no-cache-dir install  -i ${PIPURL} gunicorn 
RUN apk add mysql-client
RUN chmod +x start.sh 
RUN sed -i  's/MYSQL_HOST = "127.0.0.1"/MYSQL_HOST = "mysql"/'  applications/config.py
RUN sed -i  's/REDIS_HOST = "127.0.0.1"/REDIS_HOST = "redis"/'  applications/config.py


WORKDIR /app


CMD /bin/sh 
