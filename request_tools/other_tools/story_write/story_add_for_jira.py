#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import requests
from pydantic import BaseModel
from typing import Dict, Optional
import jsonpath
from xpinyin import Pinyin
from jira import JIRA


class ISSUE_DATA(BaseModel):
    project: Dict[str, int] = {'key': 'INET'}
    issuetype: Dict[str, int] = {'name': '故事'}
    summary: Optional[str]
    assignee: Optional[dict]
    reporter: Optional[dict] = {'name': "yu.yang"}
    description: Optional[str]
    priority: Optional[dict]


class StoryaddJiraData:
    def __init__(self, record_id):
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + self.tenant_access_token()
        }
        self.record_id = record_id
        self.summary, self.description, self.priority, self.flip_name, self.response = self.check_records()

    def tenant_access_token(self):
        """获取引用tenant_access_token
        :return: tenant_access_token
        """
        data = {"app_id": 'cli_a4b79e12a6a5d00e',
                "app_secret": '3WcrK7L00kTX0Z68O4dfjJHBaGXEHcvh'}

        res = requests.post(url="https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal", data=data).json()
        return res["app_access_token"]

    @classmethod
    def get_priority(cls, priority):
        priority_data = {'高 - P0': "2", '中 - P1': "3", '低 - P2': "4", }
        return priority_data.get(priority)

    @staticmethod
    def py_name(i):
        py_name = Pinyin().get_pinyin(i).split("-")
        if len(py_name) > 2:
            flip_name = f"{py_name[1]}{py_name[2]}.{py_name[0]}"
        else:
            flip_name = f"{py_name[1]}.{py_name[0]}"
        if flip_name == "min.xiong":
            flip_name = "ming.xiong"
        # 如果是庆中的，解析到的需要增加一个修改
        if flip_name == "qingzhong.ceng":
            flip_name = "qingzhong.zeng"
        # 如果是世文的，解析到的需要增加一个修改
        if flip_name == "shiwen.cheng":
            flip_name = "awen.cheng"
        return flip_name

    def check_records(self):
        """
        根据records_id查询数据
        :return:
        """

        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/bascnt1hXiErmr5yYGXzu7gnkGb/tables/tblBUGXLlPbhQpRP/records/{self.record_id}"
        response = requests.request("GET", url, headers=self.headers, data="").json()
        priority = self.get_priority(jsonpath.jsonpath(response, "$.data.record.fields.优先级")[0])
        summary = jsonpath.jsonpath(response, "$.data.record.fields.需求描述")[0]
        description = jsonpath.jsonpath(response, "$.data.record.fields.需求详细描述（可附文档）")
        if description is False:
            description = ""
        jira = jsonpath.jsonpath(response, "$.data.record.fields.Jira")
        if jira:
            raise ValueError("此工单已存在jira，请刷新重试!}")
        else:
            flip_name = self.py_name("杨雨")
            return summary, description, priority, flip_name, response

    def creat_jira(self):
        jira_cline = JIRA(server='https://jira.sky-cloud.net/', basic_auth=('shenbo.zhang', 'zhangshenbo#2023'))
        issue_data = ISSUE_DATA(summary=str(self.summary).replace("\n", ""),
                                assignee={'name': self.flip_name},
                                priority={'id': self.priority},
                                reporter={'name': self.flip_name},
                                description=f"*工单描述:* {self.description}\n\n"
                                            f"*飞书工单连接:* https://sky-cloud.feishu.cn/base/bascnt1hXiErmr5yYGXzu7gnkGb?table=tblBUGXLlPbhQpRP&view=vewMnpNgGD&record={self.record_id}\n\n")
        issa = jira_cline.create_issue(dict(issue_data))
        return issa

    def write_feishu(self):
        issa_id = self.creat_jira()
        data = jsonpath.jsonpath(self.response, "$..fields")
        for i in data:
            i["Jira"] = {"link": f"https://jira.sky-cloud.net/browse/{issa_id}",
                         "text": f"https://jira.sky-cloud.net/browse/{issa_id}"}
            payload = {"fields": i}

            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/bascnt1hXiErmr5yYGXzu7gnkGb/tables/tblBUGXLlPbhQpRP/records/{self.record_id}"""
            requests.request("PUT", url, headers=self.headers, json=payload).json()
            return f"jira新建成功，jira工单号为：{issa_id}"


if __name__ == '__main__':
    a = StoryaddJiraData('recOk64dGM')
    print(a.check_records())
# "rec2XFWBQ8"
