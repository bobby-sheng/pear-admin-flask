#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
from flask import Blueprint, render_template, redirect

from applications.common.utils.rights import authorize

bp = Blueprint('mitmweb', __name__, url_prefix='/mitmweb')


# app = Flask(__name__)
# PER_PAGE = 10

# 用户管理
@bp.get('/')
@authorize("system:mitmweb:main")
def main():
    return redirect('http://192.168.10.160:8081/')


