import shutil

from flask import Flask
from flask import Blueprint, render_template, request, jsonify, escape
from applications.common.utils.http import table_api, fail_api, success_api
import os
import json
import traceback
import importlib

import applications.common.utils
from applications.common.utils.rights import authorize

plugin_bp = Blueprint('plugin', __name__, url_prefix='/plugin')
PLUGIN_ENABLE_FOLDERS = []

def register_plugin_views(app: Flask):
    global PLUGIN_ENABLE_FOLDERS
    applications.common.utils.app = app  # 对app重新赋值 便于插件简单调用
    app.register_blueprint(plugin_bp)
    # 载入插件过程
    # plugin_folder 配置的是插件的文件夹名
    PLUGIN_ENABLE_FOLDERS = json.loads(app.config['PLUGIN_ENABLE_FOLDERS'])
    for plugin_folder in PLUGIN_ENABLE_FOLDERS:
        plugin_info = {}
        try:
            with open("plugins/" + plugin_folder + "/__init__.json", "r", encoding='utf-8') as f:
                plugin_info = json.loads(f.read())
            # 初始化完成事件
            try:
                getattr(importlib.import_module('plugins.' + plugin_folder), "event_init")(app)
            except AttributeError:  # 没有插件启用事件就不调用
                pass
            except BaseException as error:
                return fail_api(msg="Crash a error! Info: " + str(error))
            print(f" * Plugin: Loaded plugin: {plugin_info['plugin_name']} .")
        except BaseException as e:
            info = f" * Plugin: Crash a error when loading {plugin_info['plugin_name'] if len(plugin_info) != 0 else 'plugin'} :" + "\n"
            info += 'str(Exception):\t' + str(Exception) + "\n"
            info += 'str(e):\t\t' + str(e) + "\n"
            info += 'repr(e):\t' + repr(e) + "\n"
            info += 'traceback.format_exc():\n%s' + traceback.format_exc()
            print(info)


@plugin_bp.get('/')
@authorize("admin:plugin:main", log=True)
def main():
    """此处渲染管理模板"""
    return render_template('admin/plugin/main.html')


@plugin_bp.get('/data')
@authorize("admin:plugin:main", log=True)
def data():
    """请求插件数据"""
    plugin_name = escape(request.args.get("plugin_name"))
    all_plugins = []
    count = 0
    for filename in os.listdir("plugins"):
        try:
            with open("plugins/" + filename + "/__init__.json", "r", encoding='utf-8') as f:
                info = json.loads(f.read())

                if plugin_name is None:
                    if info['plugin_name'].find(plugin_name) == -1:
                        continue
          
                all_plugins.append(
                    {
                        "plugin_name": info["plugin_name"],
                        "plugin_version": info["plugin_version"],
                        "plugin_description": info["plugin_description"],
                        "plugin_folder_name": filename,
                        "enable": "1" if filename in PLUGIN_ENABLE_FOLDERS else "0"
                    }
                )
            count += 1
        except BaseException as error:
            print(filename, error)
            continue
    return table_api(data=all_plugins, count=count)


@plugin_bp.put('/enable')
@authorize("admin:plugin:enable", log=True)
def enable():
    """启用插件"""
    plugin_folder_name = request.json.get('plugin_folder_name')
    if plugin_folder_name:
        try:
            if plugin_folder_name not in PLUGIN_ENABLE_FOLDERS:
                PLUGIN_ENABLE_FOLDERS.append(plugin_folder_name)
                with open(".flaskenv", "r", encoding='utf-8') as f:
                    flaskenv = f.read()  # type: str
                pos1 = flaskenv.find("PLUGIN_ENABLE_FOLDERS")
                pos2 = flaskenv.find("\n", pos1)
                with open(".flaskenv", "w", encoding='utf-8') as f:
                    if pos2 == -1:
                        f.write(flaskenv[:pos1] + "PLUGIN_ENABLE_FOLDERS = " + json.dumps(PLUGIN_ENABLE_FOLDERS))
                    else:
                        f.write(
                            flaskenv[:pos1] + "PLUGIN_ENABLE_FOLDERS = " + json.dumps(PLUGIN_ENABLE_FOLDERS) + flaskenv[
                                                                                                               pos2:])
                # 启用插件事件
                try:
                    getattr(importlib.import_module('plugins.' + plugin_folder_name), "event_enable")()
                except AttributeError:  # 没有插件启用事件就不调用
                    pass
                except BaseException as error:
                    return fail_api(msg="Crash a error! Info: " + str(error))

        except BaseException as error:
            return fail_api(msg="Crash a error! Info: " + str(error))
        return success_api(msg="启用成功，要使修改生效需要重启程序。")
    return fail_api(msg="数据错误")


@plugin_bp.put('/disable')
@authorize("admin:plugin:enable", log=True)
def disable():
    """禁用插件"""
    plugin_folder_name = request.json.get('plugin_folder_name')
    if plugin_folder_name:
        try:
            if plugin_folder_name in PLUGIN_ENABLE_FOLDERS:
                PLUGIN_ENABLE_FOLDERS.remove(plugin_folder_name)
                with open(".flaskenv", "r", encoding='utf-8') as f:
                    flaskenv = f.read()  # type: str
                pos1 = flaskenv.find("PLUGIN_ENABLE_FOLDERS")
                pos2 = flaskenv.find("\n", pos1)
                with open(".flaskenv", "w", encoding='utf-8') as f:
                    if pos2 == -1:
                        f.write(flaskenv[:pos1] + "PLUGIN_ENABLE_FOLDERS = " + json.dumps(PLUGIN_ENABLE_FOLDERS))
                    else:
                        f.write(
                            flaskenv[:pos1] + "PLUGIN_ENABLE_FOLDERS = " + json.dumps(PLUGIN_ENABLE_FOLDERS) + flaskenv[
                                                                                                               pos2:])

                # 禁用插件事件
                try:
                    getattr(importlib.import_module('plugins.' + plugin_folder_name), "event_disable")()
                except AttributeError:  # 没有插件禁用事件就不调用
                    pass
                except BaseException as error:
                    return fail_api(msg="Crash a error! Info: " + str(error))

        except BaseException as error:
            return fail_api(msg="Crash a error! Info: " + str(error))
        return success_api(msg="禁用成功，要使修改生效需要重启程序。")
    return fail_api(msg="数据错误")


# 删除
@plugin_bp.delete('/remove/<string:plugin_folder_name>')
@authorize("admin:mail:remove", log=True)
def delete(plugin_folder_name):
    if plugin_folder_name in PLUGIN_ENABLE_FOLDERS:
        return fail_api(msg="您必须先禁用插件！")
    try:
        shutil.rmtree(os.path.abspath("plugins/" + plugin_folder_name))
        return success_api(msg="删除成功")
    except BaseException as error:
        return fail_api(msg="删除失败！原因：" + str(error))
