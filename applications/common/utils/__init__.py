from . import user
from . import role
from . import power
from . import department
from . import console
from . import gen_captcha
from . import http
from . import mail
from . import rights
from . import upload
from . import validate
from flask import Flask

# 获取app应用实例，会被初始化插件时重新赋值
app = None  # type: Flask
