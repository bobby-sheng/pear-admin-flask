#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import json
from flask import Blueprint, render_template, request
from applications.common.utils.http import success_api, fail_api
from applications.common.utils.rights import authorize
from request_tools.transfer.transfer_main import transfer_main

bp = Blueprint('tools', __name__, url_prefix='/tools')


@bp.get('/')
@authorize("system:tools:main")
def main():
    return render_template('system/tools/main.html')


@bp.route('/transfer_main_todo', methods=['POST'])
@authorize("system:tools:main")
def transfer_main_todo():
    """
    信息同步任务
    """
    data = json.loads(request.get_data())
    new_data = {
        'src': {
            'host': data["srcip"],
            'username': data["srcuser"],
            'password': data["srcpw"]
        },
        'dst': {
            'host': data["dstip"],
            'username': data["dstuser"],
            'password': data["dstpw"]
        }
    }
    data = transfer_main(new_data, data["interest"])
    return success_api(msg="提交成功", data=data)
