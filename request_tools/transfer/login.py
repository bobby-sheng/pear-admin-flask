#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import requests
import logging
from .common import ensure_path_sep, get_yaml_data, encrypt_password

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
Config = get_yaml_data(ensure_path_sep("\\transfer\\config.yaml"))


class Login:
    def __init__(self):
        self.src_session, self.dst_session = self.first_login()
    @staticmethod
    def first_login():
        """
        环境登录获取token
        :return:
        """
        src_session = requests.session()
        dst_session = requests.session()
        for i in ["src", "dst"]:
            src_url = f"http://{Config.get(i)['host']}/api/sky-platform/auth/user/v2/login"
            data = {
                "username": Config.get(i)['username'],
                "password": encrypt_password("H05BLZeHIH2f0e+QMq10TQ==", password=Config.get(i)['password'])
            }
            headers = {'Content-Type': 'application/json'}
            # 请求登录接口
            if i == "src":
                src_json = src_session.post(url=src_url, json=data, headers=headers, verify=True).json()
                assert src_json["code"] == 200, "src登录失败"
                logging.info("=====src环境登录成功！=====")
            else:
                dsr_json = dst_session.post(url=src_url, json=data, headers=headers, verify=True).json()
                assert dsr_json["code"] == 200, "dst登录失败"
                logging.info("=====dst环境登录成功！=====")

        return src_session, dst_session
