#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>

import requests
from applications.config import BaseConfig
import os

os.environ['PYTHONHTTPSVERIFY'] = '0'


class DeployImage:

    def __init__(self):
        self.da = {"parameter": [{"name": "CMDBTAG", "value": "0"}, {"name": "EVENTTITAG", "value": "0"},
                                 {"name": "GWAYTAG", "value": "0"}, {"name": "HTTPDTAG", "value": "0"},
                                 {"name": "INET_CLIENTTAG", "value": "0"},
                                 {"name": "INET_CLIENT_JAVATAG", "value": "0"},
                                 {"name": "INET_NGPARSERTAG", "value": "0"}, {"name": "INET_PLATFORMTAG", "value": "0"},
                                 {"name": "INET_WORKFLOWTAG", "value": "0"}, {"name": "JSON_ADAPTORTAG", "value": "0"},
                                 {"name": "LOGSYSTEMTAG", "value": "0"}, {"name": "NETCTAG", "value": "0"},
                                 {"name": "NETDTAG", "value": "0"}, {"name": "NGINXTAG", "value": "0"},
                                 {"name": "PIPELINETAG", "value": "0"}, {"name": "TRIGGERTAG", "value": "0"},
                                 {"name": "POLICYINSIGHTTAG", "value": "0"},
                                 {"name": "HostIP", "value": "192.168.30.82"}]}

    def deploy_all(self, all_data: dict):
        if not all_data:
            return "无可部署镜像！"
        all_data.pop("previewId")
        all_data.pop("name")
        result = []
        for k, v in all_data.items():
            if v == "None" or v == "":
                v = "0"
            result.append({'name': k, 'value': v})
        deploy_all_data = self.da.copy()
        deploy_all_data["parameter"] = result

        json_data = {
            'json': f'{deploy_all_data}',
        }
        try:
            res = requests.post(
                url=BaseConfig.JENKINS_URL,
                data=json_data,
                auth=(BaseConfig.JENKINS_NAME, BaseConfig.JENKINS_TOKEN),
            )
            print(res.text)
            if "<!DOCTYPE html>" in res.text:
                return "false"
            else:
                return "ok"
        except:
            return "false"

    def deploy_one(self, one_data: dict):
        if not one_data:
            return "无可部署镜像！"
        deploy_one_data = self.da.copy()

        if one_data["image"] == "None" or one_data["image"] == "":
            one_data["image"] = "0"

        for i in deploy_one_data["parameter"]:
            if one_data["module"] == i["name"]:
                i["value"] = one_data["image"]
            if i["name"] == "HostIP":
                i["value"] = one_data["dev"]
        json_data = {
            'json': f'{deploy_one_data}',
        }

        try:
            res = requests.post(
                url=BaseConfig.JENKINS_URL,
                data=json_data,
                auth=(BaseConfig.JENKINS_NAME, BaseConfig.JENKINS_TOKEN),
            )
            print(res.text)
            if "<!DOCTYPE html>" in res.text:
                return "false"
            else:
                return "ok"
        except:
            return "false"


if __name__ == '__main__':
    DeployImage().deploy_one()
