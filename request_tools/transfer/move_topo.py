#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import jsonpath
import json
from .filelog import logger
from .move_device import Device
from .common import ensure_path_sep, get_yaml_data

Config = get_yaml_data(ensure_path_sep("\\transfer\\config.yaml"))


class MoveTopo(Device):

    def __init__(self, device_relation):
        super().__init__()
        self.device_relation = device_relation
        self.dst_topo_data_list_id = []
        self.src_topo_data_list_id = []

    def dst_src_get_topo_data(self, k, res, dst_topo_data_list, src_topo_data_list):
        for dst_topo in res["data"]["list"]:
            dst_topo_data = {
                "name": dst_topo["name"],
                "type": dst_topo["type"],
                "description": dst_topo["description"],
            }
            if k == "dst":
                dst_topo_data_list.append(dst_topo_data)
                self.dst_topo_data_list_id.append({
                    "id": dst_topo["id"],
                    "name": dst_topo["name"],
                    "type": dst_topo["type"],
                    "description": dst_topo["description"],
                })
            else:
                src_topo_data_list.append(dst_topo_data)
                self.src_topo_data_list_id.append({
                    "id": dst_topo["id"],
                    "name": dst_topo["name"],
                    "type": dst_topo["type"],
                    "description": dst_topo["description"],
                })
        return dst_topo_data_list, src_topo_data_list

    def get_dst_topo_list(self):
        """
        获取源 目环境的拓扑列表，存储信息
        :return:
        """
        dst_topo_data_list = []
        src_topo_data_list = []
        url_path = str(Config.get('get_topo_list'))
        for k, v in {"dst": self.dst_session, "src": self.src_session}.items():
            url = f"http://{Config.get(k)['host']}{url_path}"
            res = v.get(url).json()
            assert res['code'] == 200, f"{k}拓扑列表接口获取失败{res}"
            count = res["data"]["allPage"]
            if count > 1:
                for c in range(count):
                    url = f"http://{Config.get(k)['host']}{url_path.replace('0', str(c))}"
                    res = v.get(url).json()
                    dst_topo_data_list, src_topo_data_list = self.dst_src_get_topo_data(k, res, dst_topo_data_list,
                                                                                        src_topo_data_list)

            else:
                dst_topo_data_list, src_topo_data_list = self.dst_src_get_topo_data(k, res, dst_topo_data_list,
                                                                                    src_topo_data_list)

        return dst_topo_data_list, src_topo_data_list

    def add_topo(self, topo_add_data):
        """
        新增拓扑
        :return:
        """
        url_path = str(Config.get('add_topo'))
        data = topo_add_data
        url = f"http://{Config.get('dst')['host']}{url_path}"
        res = self.dst_session.post(url, json=data).json()
        assert res['code'] == 200, f"拓扑保存失败{res}"
        return res["data"]["id"]

    def dst_save_topo(self, topo_add_data):
        """
        新增拓扑
        :return:
        """
        url_path = str(Config.get('add_topo'))
        data = topo_add_data
        url = f"http://{Config.get('dst')['host']}{url_path}"
        res = self.dst_session.put(url, json=data).json()
        assert res['code'] == 200, f"拓扑保存失败{res}"
        return res["data"]["id"]

    def add_dst_topo(self):
        """
        判断src拓扑是否在dst中存在，不存在就新建，存在就获取id。返回一个id关联表
        :return:
        """
        src_dst_topo_relation = []
        dst_topo_data_list, src_topo_data_list = self.get_dst_topo_list()

        for src_topo in self.src_topo_data_list_id:
            src_topo_cp = src_topo.copy()
            src_topo_cp.pop("id")
            if src_topo_cp in dst_topo_data_list:
                for compare_element in self.dst_topo_data_list_id:
                    if (src_topo['name'] == compare_element['name']) and (
                            src_topo['type'] == compare_element['type']) and (
                            src_topo['description'] == compare_element['description']):
                        logger.info(f"[{src_topo['name']}] 在dst环境存在，不新增，获取id {compare_element['id']}")
                        src_topo["dst_topo_id"] = compare_element['id']
                        src_dst_topo_relation.append(src_topo)
            else:
                dst_topo_id = self.add_topo(src_topo)
                src_topo["dst_topo_id"] = dst_topo_id
                src_dst_topo_relation.append(src_topo)
                logger.info(f"[{src_topo['name']}] ,新增，获取id")

        return src_dst_topo_relation

    def handle_topo_add(self, nodes_list: list, src_data_str: str):
        """
        处理src获取的参数数据，返回给到dst新增topo需要的数据
        :return:
        """

        device_id_map = {item['id']: item['device_id'] for item in self.device_relation if 'device_id' in item}
        for node in nodes_list:
            if device_id_map.get(node):
                src_data_str = src_data_str.replace(node, device_id_map.get(node))
            else:
                return False
        return src_data_str

    def read_write_topo(self):
        """
        获取src拓扑的详情，提取需要的参数
        :return:
        """
        src_dst_topo_relation = self.add_dst_topo()
        for src_topo_info in src_dst_topo_relation:
            url_path = str(Config.get('get_topo_info')).replace("src_topo_id", src_topo_info["id"])
            url = f"http://{Config.get('src')['host']}{url_path}"
            res = self.src_session.get(url).json()
            res_data = res.get("data")
            assert res['code'] == 200, f"dst环境拓扑报错失败{res}"
            if res_data.get("nodes") == []:
                logger.info(f"{src_topo_info['name']}  拓扑无内容node，不做处理")
                continue
            else:
                nodes_list = jsonpath.jsonpath(res_data, "$.nodes..id")
                network_nodes_list = jsonpath.jsonpath(res_data, "$.nodes.[?(@.type=='NETWORK')]..id")
                if network_nodes_list:
                    nodes_list = [x for x in nodes_list if x not in network_nodes_list]
                res_data["id"] = src_topo_info["dst_topo_id"]

                data_str = json.dumps(res_data)
                dst_add_topo_data = self.handle_topo_add(nodes_list=nodes_list, src_data_str=data_str)
                if dst_add_topo_data:
                    updated_data = json.loads(dst_add_topo_data)
                    self.dst_save_topo(updated_data)
                    logger.info(f"{src_topo_info['name']}  dst TOPO保存成功!")
                else:
                    logger.info(f"{src_topo_info['name']}  srcTOPO中存在已被删除设备节点，跳过不新增！")

