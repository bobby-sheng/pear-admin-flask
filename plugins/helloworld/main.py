from applications.dev import *

from flask import render_template, Blueprint

import os
import psutil

# 获取插件所在的目录（结尾没有分割符号）
dir_path = os.path.dirname(__file__).replace("\\", "/")
folder_name = dir_path[dir_path.rfind("/") + 1:]  # 插件文件夹名称

# 创建蓝图
helloworld_blueprint = Blueprint('hello_world', __name__, template_folder='templates', static_folder="static",
                       url_prefix="/hello_world")

@helloworld_blueprint.route("/")
def index():
    return render_template("helloworld_index.html")

