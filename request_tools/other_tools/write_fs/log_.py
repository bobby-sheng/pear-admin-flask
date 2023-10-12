#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import logging

# 创建Logger对象并进行基本配置
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# 创建控制台处理器并进行基本配置
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

# 创建文件处理器并进行基本配置
file_handler = logging.FileHandler('jira_example.txt', encoding="utf-8")
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

# 将处理器添加到Logger对象中
logger.addHandler(console_handler)
logger.addHandler(file_handler)
