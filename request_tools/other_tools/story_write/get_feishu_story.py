#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import requests
from urllib.parse import quote
import datetime
import jsonpath


class StoryToJira:
    def __init__(self):
        self.read_apps_url = "https://open.feishu.cn/open-apis/bitable/v1/apps/"
        self.apps = "bascnt1hXiErmr5yYGXzu7gnkGb"
        self.table = "tblBUGXLlPbhQpRP"
        self.view = "vewMnpNgGD"
        self.token_api_id = "cli_a4b79e12a6a5d00e"
        self.token_app_secret = "3WcrK7L00kTX0Z68O4dfjJHBaGXEHcvh"
        self.token_url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + self.tenant_access_token()
        }

    def tenant_access_token(self):
        """获取引用tenant_access_token
        :return: tenant_access_token
        """
        data = {"app_id": self.token_api_id,
                "app_secret": self.token_app_secret}

        res = requests.post(self.token_url, data=data).json()
        return res["app_access_token"]

    def get_story_info_list(self):
        """
        获取多维表格
        :return:
        """

        filter_data = "NOT%28CurrentValue.%5B%E9%9C%80%E6%B1%82%E7%8A%B6%E6%80%81%5D.contains%28%22%E5%B7%B2%E5%AE%8C%E6%88%90%22%2C%22%E6%8B%92%E7%BB%9D%22%2C%22%E7%A0%94%E5%8F%91%E4%BA%A4%E4%BB%98%22%2C%22%E6%8A%80%E6%9C%AF%E9%AA%8C%E6%94%B6%22%29%29%26%26CurrentValue.%5BJira%5D%3D%22%22"
        url = f"""{self.read_apps_url}{self.apps}/tables/{self.table}/records?filter={filter_data}&page_size=1000&view_id={self.view}"""

        response = requests.request("GET", url, headers=self.headers, data="").json()
        feishu_data = []
        if "items" in response.get("data"):
            for i in response["data"]["items"]:

                data_items = i.get("fields")
                try:
                    assignee_name = [n["name"] for n in data_items.get("负责人")]
                except:
                    assignee_name = None
                try:
                    put_name = [n["en_name"] for n in data_items.get("提出人")]
                except:
                    break
                dt_object = datetime.datetime.fromtimestamp(data_items.get("提出日期") / 1000)

                # 使用strftime方法将datetime对象转换为年月日格式
                formatted_date = dt_object.strftime('%Y-%m-%d')
                re_data = {"ctime": formatted_date,
                           "summary": data_items.get("需求标题"),
                           "put_name": put_name,
                           "priority": data_items.get("优先级"),
                           "release": data_items.get("需求分类"),
                           "labels": data_items.get("客户"),
                           "assignee": assignee_name,
                           "record_id": i.get("record_id"),
                           "status": data_items.get("需求状态"),
                           "number": data_items.get("需求编号"),
                           }
                feishu_data.append(re_data)
            return feishu_data, response.get("data").get("total")
        else:
            return [], 0


if __name__ == '__main__':
    print(StoryToJira().get_story_info_list()[1])
