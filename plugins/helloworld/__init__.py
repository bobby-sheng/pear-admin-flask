"""
初始化插件
"""
import os

from flask import Flask
from .main import helloworld_blueprint

# 获取插件所在的目录（结尾没有分割符号）
dir_path = os.path.dirname(__file__).replace("\\", "/")
folder_name = dir_path[dir_path.rfind("/") + 1:]  # 插件文件夹名称

def event_enable():
    """当此插件被启用时会调用此处"""
    print(f"启用插件，dir_path: {dir_path} ; folder_name: {folder_name}")


def event_disable():
    """当此插件被禁用时会调用此处"""
    print(f"禁用插件，dir_path: {dir_path} ; folder_name: {folder_name}")

def event_init(app: Flask):
    """初始化完成时会调用这里"""
    app.register_blueprint(helloworld_blueprint)