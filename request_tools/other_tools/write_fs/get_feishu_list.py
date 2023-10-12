#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import requests
import jsonpath
from jira import JIRA
from xpinyin import Pinyin
from request_tools.other_tools.write_fs.log_ import logger
from request_tools.other_tools.write_fs.model import URL, DATA, ISSUE_DATA, get_priority
import datetime


class LinkFeiShu_V2(object):

    def __init__(self):
        self.record_id_list = []
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + self.tenant_access_token()
        }

    def tenant_access_token(self):
        """获取引用tenant_access_token
        :return: tenant_access_token
        """
        data = {"app_id": DATA().app_id,
                "app_secret": DATA().app_secret}

        res = requests.post(URL().app_access_token, data=data).json()
        return res["app_access_token"]

    @staticmethod
    def new_time():
        two_days_ago = datetime.date.today() - datetime.timedelta(days=5)

        # 将2天前的日期转换为日期时间对象
        two_days_ago_datetime = datetime.datetime.combine(two_days_ago, datetime.datetime.min.time())

        # 获取2天前的时间戳（单位：秒）
        two_days_ago_timestamp = int(two_days_ago_datetime.timestamp())
        # 将 Unix 时间戳转换为毫秒级别的 JavaScript 时间戳
        javascript_timestamp = two_days_ago_timestamp * 1000
        return javascript_timestamp

    @staticmethod
    def py_name(i):
        py_name = Pinyin().get_pinyin(i).split("-")
        if len(py_name) > 2:
            flip_name = f"{py_name[1]}{py_name[2]}.{py_name[0]}"
        else:
            flip_name = f"{py_name[1]}.{py_name[0]}"
        return flip_name

    def get_info_list(self):
        """
        获取多维表格
        :return:
        """
        filter_data = "NOT%28CurrentValue.%5B%E9%97%AE%E9%A2%98%E6%8F%8F%E8%BF%B0%5D+%3D%22%22%29%26%26Curre" \
                      "ntValue.%5B%E7%A0%94%E5%8F%91Jira%E5%B7%A5%E5%8D%95%E9%93%BE%E6%8E%A5%5D+%3D%22%22%26%26C" \
                      "urrentValue.%5B%E9%97%AE%E9%A2%98%E7%8A%B6%E6%80%81%5D+%3D%22%E5%BE%85%E7%A1%AE%E8%AE%A4%22"
        url = f"""{URL().apps_url}{DATA().apps}/tables/{DATA().table}/records?filter={filter_data}&page_size=20&view_id={DATA().view}"""

        response = requests.request("GET", url, headers=self.headers, data="").json()
        print(response)
        feishu_data = []
        if "items" in response.get("data"):
            for i in response["data"]["items"]:
                data_items = i.get("fields")
                assignee_name = [n["name"] for n in data_items.get("问题处理人员")]
                dt_object = datetime.datetime.fromtimestamp(data_items.get("创建日期") / 1000)

                # 使用strftime方法将datetime对象转换为年月日格式
                formatted_date = dt_object.strftime('%Y-%m-%d')
                re_data = {"ctime": formatted_date,
                           "summary": data_items.get("问题描述"),
                           "priority": data_items.get("优先级"),
                           "labels": data_items.get("所属客户"),
                           "assignee": assignee_name,
                           "record_id": i.get("record_id"),
                           }
                feishu_data.append(re_data)
            return feishu_data, response.get("data").get("total")
        else:
            return [], 0

    def creat_jira(self, summary, assignee: list, description, priority, record_id):
        jira_cline = JIRA(server=URL().jira_server, basic_auth=(DATA().jira_username, DATA().jira_password))
        print(summary, assignee, description, priority, record_id)
        # 去除修复人中的张圣波
        if "张圣波" in assignee:
            assignee.pop(assignee.index("张圣波"))
        assignee_tow = assignee
        # 判断去除了张圣波之后，name字段是否为[]
        if not assignee_tow:
            raise ValueError(f"==={summary}===,未分配除张圣波以外的研发修复人，请添加其他修复人再执行才会创建")
        flip_name = self.py_name(assignee_tow[0])
        # 如果是熊敏的，解析到的需要增加一个g
        if flip_name == "min.xiong":
            flip_name = "ming.xiong"
        # 如果是庆中的，解析到的需要增加一个修改
        if flip_name == "qingzhong.ceng":
            flip_name = "qingzhong.zeng"
        if flip_name == "shiwen.cheng":
            flip_name = "awen.cheng"

        priority = get_priority(priority)
        issue_data = ISSUE_DATA(summary=str(summary),
                                assignee={'name': flip_name},
                                priority={'id': priority},
                                description=f"飞书连接：https://sky-cloud.feishu.cn/base/"
                                            f"{DATA().apps}?table={DATA().table}&view={DATA().view}&record={record_id}",
                                labels=[description])
        issa = jira_cline.create_issue(dict(issue_data))
        return issa

    def get_all_data(self, summary, assignee, description, priority, record_id):
        """
        根据record_id查询工单
        :param record_id:
        :return:
        """
        issa = self.creat_jira(summary, assignee, description, priority, record_id)
        url = f"""{URL().apps_url}{DATA().apps}/tables/{DATA().table}/records/{record_id}"""

        response = requests.request("GET", url, headers=self.headers, data="").json()
        data = jsonpath.jsonpath(response, "$..fields")
        for i in data:
            i["研发Jira工单链接"] = {"link": f"https://jira.sky-cloud.net/browse/{issa}",
                               "text": dict(i).get("问题描述")}
            payload = {"fields": i}

            url = f"""{URL().apps_url}{DATA().apps}/tables/{DATA().table}/records/{record_id}"""
            requests.request("PUT", url, headers=self.headers, json=payload).json()
            return f"jira新建成功，jira工单号为：{issa}"


if __name__ == '__main__':
    print(LinkFeiShu_V2().get_info_list())
