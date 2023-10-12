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


class LinkFeiShu(object):

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
        py_name = Pinyin().get_pinyin(i[3][0]).split("-")
        if len(py_name) > 2:
            flip_name = f"{py_name[1]}{py_name[2]}.{py_name[0]}"
        else:
            flip_name = f"{py_name[1]}.{py_name[0]}"
        return flip_name

    def get_info(self):
        """
        获取多维表格
        :return:
        """
        # AND(NOT(CurrentValue.[问题描述] =""),CurrentValue.[研发Jira工单链接] ="")
        filter_data = "AND%28NOT%28CurrentValue.%5B%E9%97%AE%E9%A2%98%E6%8F%8F%E8%BF%B0%5D+%3D%22%22%29%2C" \
                      "CurrentValue.%5B%E7%A0%94%E5%8F%91Jira%E5%B7%A5%E5%8D%95%E9%93%BE%E6%8E%A5%5D+%3D%22%22%29"
        url = f"""{URL().apps_url}{DATA().apps}/tables/{DATA().table}/records?filter={filter_data}&page_size=20&view_id={DATA().view}"""

        response = requests.request("GET", url, headers=self.headers, data="").json()
        print(response)
        try:
            assert int(jsonpath.jsonpath(response, "$.code")[0]) == 0

        except AssertionError as e:
            raise AssertionError("查询接口调用错误：", response)
        record_list = []
        for i in response.get("data").get("items"):
            fields_dict = i["fields"]
            fields_dict["record_id"] = i["record_id"]
            record_list.append({i["record_id"]: fields_dict})

        # 获取时间大于2天前的单
        all_bug_info = []
        for v in record_list:
            for k, vv in dict(v).items():
                if vv["创建日期"] > self.new_time():
                    all_bug_info.append(vv)
                    self.record_id_list.append({k: vv})
        print(all_bug_info)
        try:
            bug_info = [[i["问题描述"], i["优先级"], i["所属客户"], i["问题处理人员"], i["record_id"]] for i in all_bug_info]

        except KeyError as e:
            logger.error("工单缺失关键字段，请检查：问题描述、优先级、所属客户、问题处理人员是否填写")
            raise ValueError("工单缺失关键字段，请检查：问题描述、优先级、所属客户、问题处理人员是否填写")

        if not bug_info:
            logger.error("没有需要提交jira的工单")
            raise ValueError("没有需要提交jira的工单")
        print(bug_info)

        return bug_info

    def jira_create_issue(self):
        """
        新建jira故障单
        :return:
        """
        jira_cline = JIRA(server=URL().jira_server, basic_auth=(DATA().jira_username, DATA().jira_password))
        data = self.get_info()
        issa_list = []
        for i in data:
            print(i)
            # 去除修复人中的张圣波
            name = jsonpath.jsonpath(i, "$..name")
            if "张圣波" in name:
                name.pop(name.index("张圣波"))
            i[3] = name
            # 判断去除了张圣波之后，name字段是否为[]
            if not i[3]:
                logger.warning(f"==={i[0]}===,未分配除张圣波以外的研发修复人，请添加其他修复人再执行才会创建")
                continue
            flip_name = self.py_name(i)
            # 如果是熊敏的，解析到的需要增加一个g
            if flip_name == "min.xiong":
                flip_name = "ming.xiong"
            # 如果是庆中的，解析到的需要增加一个修改
            if flip_name == "qingzhong.ceng":
                flip_name = "qingzhong.zeng"

            if flip_name=="shiwen.cheng":
                flip_name="awen.cheng"

            priority = get_priority(i[1])
            issue_data = ISSUE_DATA(summary=str(i[0]),
                                    assignee={'name': flip_name},
                                    priority={'id': priority},
                                    description=f"飞书连接：https://sky-cloud.feishu.cn/base/"
                                                f"{DATA().apps}?table={DATA().table}&view={DATA().view}&record={i[4]}",
                                    labels=[i[2]])

            issa = jira_cline.create_issue(dict(issue_data))
            for s in self.record_id_list:
                for k, v in s.items():
                    if i[0] == v.get("问题描述"):
                        logger.info(f"写入问题：【{v.get('问题描述')},jira新建成功】，单号为：{str(issa)}")
                        issa_list.append([k, v, str(issa)])
        return issa_list

    def write_feishu(self):
        write_list = self.jira_create_issue()
        logger.info(f"写入{len(write_list)}个问题")
        for i in write_list:
            i[1].pop("record_id")

            i[1]["研发Jira工单链接"] = {"link": f"https://jira.sky-cloud.net/browse/{i.pop(2)}",
                                  "text": dict(i[1]).get("问题描述")}
            payload = {"fields": i[1]}

            url = f"""{URL().apps_url}{DATA().apps}/tables/{DATA().table}/records/{i[0]}"""
            response = requests.request("PUT", url, headers=self.headers, json=payload).json()
            print(response)


if __name__ == '__main__':
    LinkFeiShu().write_feishu()
