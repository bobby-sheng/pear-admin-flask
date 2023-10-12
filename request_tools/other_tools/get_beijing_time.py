#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import requests
from datetime import datetime


def get_time():
    # 使用百度提供的时间API获取北京时间
    response = requests.get('http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp')
    # 获取返回的时间戳
    timestamp = response.json()['data']['t']
    # 将时间戳转换为datetime对象
    dt = datetime.fromtimestamp(int(timestamp) / 1000.0)
    return dt
