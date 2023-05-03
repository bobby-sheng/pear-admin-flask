#!/bin/sh
while ! flask db init ; do
  sleep 5 ;
done ;
flask db migrate && flask db upgrade && flask admin init
exec gunicorn -c gunicorn.conf.py "applications:create_app()"