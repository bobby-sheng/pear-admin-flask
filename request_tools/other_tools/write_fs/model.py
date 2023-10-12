#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
from typing import Text, Dict, Optional, List
from pydantic import BaseModel


class URL(BaseModel):
    apps_url: str = "https://open.feishu.cn/open-apis/bitable/v1/apps/"
    app_access_token: str = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    jira_server: str = 'https://jira.sky-cloud.net/'


class DATA(BaseModel):
    app_id: str = "cli_a4b79e12a6a5d00e"
    app_secret: str = "3WcrK7L00kTX0Z68O4dfjJHBaGXEHcvh"
    jira_username: str = "shenbo.zhang"
    jira_password: str = "zhangshenbo#2023"
    apps: str = "OLbSbGZvraOZ9GsEWJXclpwInzh"
    table: str = "tbldtje49iRghPbC"
    view: str = "vewXxBNTOK"


class ISSUE_DATA(BaseModel):
    project: Dict[str, int] = {'key': 'INET'}
    issuetype: Dict[str, int] = {'name': '故障'}
    summary: Optional[str]
    assignee: Optional[dict]
    reporter: Optional[dict] = {'name': "shenbo.zhang"}
    description: Optional[str]
    labels: Optional[list]
    priority: Optional[dict]
    customfield_10101: str = 'INET-90'


def get_priority(priority):
    if priority == "紧急-P0":
        return "1"
    elif priority == "高-P1":
        return "2"
    elif priority == "中-P2":
        return "3"
    else:
        return "4"
