"""
初始化插件
"""
from flask import Flask
from .main import helloworld_blueprint

def event_enable():
    """当此插件被启用时会调用此处"""
    print("启用插件")


def event_disable():
    """当此插件被禁用时会调用此处"""
    print("禁用插件")

def event_init(app: Flask):
    """初始化完成时会调用这里"""
    app.register_blueprint(helloworld_blueprint)