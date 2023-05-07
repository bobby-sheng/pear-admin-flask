FROM pearadminflask/python3.7-flask:pillow

COPY . /app/

WORKDIR /app/

ENV TIME_ZONE Asia/Shanghai

RUN echo "${TIME_ZONE}" > /etc/timezone \
    && ln -sf /usr/share/zoneinfo/${TIME_ZONE} /etc/localtime
RUN pip --no-cache-dir install  -i ${PIPURL} --upgrade pip \
    && pip --no-cache-dir install  -i ${PIPURL} -r requirements.txt \
    && pip --no-cache-dir install  -i ${PIPURL} gunicorn 
RUN apk add mysql-client
RUN chmod +x start.sh 
RUN sed -i  's/MYSQL_HOST = "127.0.0.1"/MYSQL_HOST = "mysql"/'  applications/config.py
RUN sed -i  's/REDIS_HOST = "127.0.0.1"/REDIS_HOST = "redis"/'  applications/config.py

CMD /bin/sh 