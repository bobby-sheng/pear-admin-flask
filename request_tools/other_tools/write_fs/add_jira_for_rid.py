#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
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
    issuetype: Dict[str, int] = {'name': '故障'}
    summary: Optional[str]
    assignee: Optional[dict]
    reporter: Optional[dict] = {'name': "shenbo.zhang"}
    description: Optional[str]
    labels: Optional[list]
    priority: Optional[dict]
    customfield_10101: str = 'INET-90'


class addJiraData:
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
        priority_data = {'紧急-P0': "1", '高-P1': "2", '中-P2': "3", '低-P3': "4", }
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

        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/OLbSbGZvraOZ9GsEWJXclpwInzh/tables/tbldtje49iRghPbC/records/{self.record_id}"
        response = requests.request("GET", url, headers=self.headers, data="").json()
        priority = self.get_priority(jsonpath.jsonpath(response, "$.data.record.fields.优先级")[0])
        assignee = jsonpath.jsonpath(response, "$.data.record.fields.问题处理人员..name")
        summary = jsonpath.jsonpath(response, "$.data.record.fields.问题描述")[0]
        labels = jsonpath.jsonpath(response, "$.data.record.fields.所属客户")[0]

        if "张圣波" in assignee:
            assignee.pop(assignee.index("张圣波"))
        if not assignee:
            raise ValueError(f"==={assignee}===,未分配除张圣波以外的研发修复人，请添加其他修复人再执行才会创建")
        flip_name = self.py_name(assignee[0])
        return summary, labels, priority, flip_name, response


    def creat_jira(self):
        jira_cline = JIRA(server='https://jira.sky-cloud.net/', basic_auth=('shenbo.zhang', 'zhangshenbo#2023'))
        issue_data = ISSUE_DATA(summary=str(self.summary),
                                assignee={'name': self.flip_name},
                                priority={'id': self.priority},
                                description=f"飞书连接：https://sky-cloud.feishu.cn/base/"
                                            f"OLbSbGZvraOZ9GsEWJXclpwInzh?table=tbldtje49iRghPbC&view=vewXxBNTOK&record={self.record_id}",
                                labels=[self.description])
        issa = jira_cline.create_issue(dict(issue_data))
        return issa

    def write_feishu(self):
        issa_id = self.creat_jira()
        data = jsonpath.jsonpath(self.response, "$..fields")
        for i in data:
            i["研发Jira工单链接"] = {"link": f"https://jira.sky-cloud.net/browse/{issa_id}",
                               "text": dict(i).get("问题描述")}
            i["问题状态"] = "研发处理中"
            payload = {"fields": i}

            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/OLbSbGZvraOZ9GsEWJXclpwInzh/tables/tbldtje49iRghPbC/records/{self.record_id}"""
            requests.request("PUT", url, headers=self.headers, json=payload).json()
            return f"jira新建成功，jira工单号为：{issa_id}"


if __name__ == '__main__':
    a = addJiraData('rec89ia9oX')
    print(a.write_feishu())
