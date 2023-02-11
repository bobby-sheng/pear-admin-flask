from applications.dev import user
from applications.dev import role
from applications.dev import power
from applications.dev import department
from applications.dev import console
from flask import Flask

# 获取app应用实例，会被初始化插件时重新赋值
app = None  # type: Flask
