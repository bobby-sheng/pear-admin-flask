from flask import Blueprint, render_template, request
from applications.common.curd import get_one_by_id

from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Preview
from applications.models import PreviewLog
from applications.models import Preview_history

from sqlalchemy import desc

from request_tools.jenkins_deploy.jenkins_deploy_images import DeployImage
import json
from flask import Flask, render_template, request, Response
from request_tools.other_tools.write_fs import to_run
import os
# from flask_paginate import Pagination, get_page_args
from flask import Flask, request
bp = Blueprint('jira', __name__, url_prefix='/jira')
# app = Flask(__name__)
# PER_PAGE = 10

# 用户管理
@bp.get('/')
@authorize("system:jira:main")
def main():
    return render_template('system/jira/main.html')

# 处理生成log事件请求
@bp.post('/creat')
@authorize("system:jira:creat", log=True)
def generate_log():
    if os.path.exists('jira_example.txt'):
        with open('jira_example.txt', 'w'):
            pass
    try:
        to_run.gorun()
    except Exception as e:
        print(f"执行异常,{e}")
    with open('jira_example.txt', 'r', encoding="utf-8") as file:
        logs = file.read()
    return Response(logs, mimetype='text/plain')
