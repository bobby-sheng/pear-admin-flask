#!/bin/sh
sleep 5 #等MySQL启动
flask db init && flask db migrate && flask db upgrade && flask admin init
exec gunicorn -c gunicorn.conf.py "applications:create_app()"
while true; do
    echo '发生错误'
    sleep 100
done
