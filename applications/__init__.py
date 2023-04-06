import os
from flask import Flask
from applications.common.script import init_script
from applications.config import BaseConfig
from applications.extensions import init_plugs
from applications.view import init_view


def create_app():
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    # 引入数据库配置
    app.config.from_object(BaseConfig)

    # 注册各种插件
    init_plugs(app)

    # 注册路由
    init_view(app)

    # 注册命令
    init_script(app)

    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        logo()

    return app


def logo():
    print('''
 _____                              _           _         ______ _           _    
|  __ \                    /\      | |         (_)       |  ____| |         | |   
| |__) |__  __ _ _ __     /  \   __| |_ __ ___  _ _ __   | |__  | | __ _ ___| | __
|  ___/ _ \/ _` | '__|   / /\ \ / _` | '_ ` _ \| | '_ \  |  __| | |/ _` / __| |/ /
| |  |  __/ (_| | |     / ____ \ (_| | | | | | | | | | | | |    | | (_| \__ \   < 
|_|   \___|\__,_|_|    /_/    \_\__,_|_| |_| |_|_|_| |_| |_|    |_|\__,_|___/_|\_\\

    ''')
