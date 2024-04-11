#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import jsonpath
import time
from .filelog import logger
from .move_template import Template
from .common import ensure_path_sep, get_yaml_data

Config = get_yaml_data(ensure_path_sep("\\transfer\\config.yaml"))


class Device(Template):

    def __init__(self):
        super().__init__()
        self.mapping = {
            1: "数据中心",
            2: "业务域",
            3: "设备"
        }
        self.dst_device_data_res = None
        self.sky_idc = None
        self.sky_biz_domain_id = None
        self.add_credential_id = None

    def add_credential(self):
        """
        新增连接凭证
        :return:
        """
        url = f"http://{Config.get('dst')['host']}{Config.get('add_device_credential')}"
        data = {"name": "device_move", "credentialType": "USER_PASSWORD", "password": "noj7o8Y9TFhGc9sZ4uaS2A==",
                "description": "device_move", "userName": "admin"}
        credential_res = self.dst_session.post(url, json=data).json()
        if "已经存在" in credential_res["message"]:
            logger.info("连接凭证已经存在，获取id！")
            list_url = f"http://{Config.get('dst')['host']}{Config.get('get_device_credential_list')}"
            credential_list_res = self.dst_session.get(list_url).json()
            credential_id = jsonpath.jsonpath(credential_list_res, "$.data.list.[?(@.name=='device_move')].id")[0]
        else:
            logger.info("新建连接凭证！")
            credential_id = jsonpath.jsonpath(credential_res, "$.data.id")[0]
        return credential_id

    def add_sky_idc(self, data, project_id):
        """
        新增数据中心获取id
        :param data:
        :param project_id: 基础架构id
        :return:
        """

        add_sky_idc_path = str(Config.get('add_sky_idc')).replace("project_id", project_id)
        url = f"http://{Config.get('dst')['host']}{add_sky_idc_path}"
        add_sky_idc_res = self.dst_session.post(url, json=data).json()
        assert add_sky_idc_res['code'] == 200
        logger.info(f"新增数据中心完成 {add_sky_idc_res['data']['id']}")
        return add_sky_idc_res['data']['id']

    def add_sky_biz_domain(self, data, sky_idc_id):
        """
        新增业务域，获取id
        :param sky_idc_id:
        :param data:
        :return:
        """

        add_sky_biz_domain_path = str(Config.get('add_sky_biz_domain')).replace("sky_idc_id", sky_idc_id)
        url = f"http://{Config.get('dst')['host']}{add_sky_biz_domain_path}"
        add_sky_biz_domain_res = self.dst_session.post(url, json=data).json()
        assert add_sky_biz_domain_res['code'] == 200, f"业务域新增失败{add_sky_biz_domain_res}"
        logger.info(f"新增业务域完成 {add_sky_biz_domain_res['data']['id']}")
        return add_sky_biz_domain_res['data']['id']

    def get_device_info(self, modelKey: str, device_id):
        """
        获取src防火墙设备详情
        :return:
        """
        logger.info("=================================开始新增设备！================================= ")
        logger.info(f"获取src设备 {device_id} 参数，和版本id")
        sky_firewall_res = ""
        if modelKey == "sky_firewall":
            url_path = str(Config.get('get_sky_firewall_info')).replace("device_id", device_id)
            url = f"http://{Config.get('src')['host']}{url_path}"
            sky_firewall_res = self.src_session.get(url).json()

        elif modelKey == "sky_loadbalancer":
            url_path = str(Config.get('get_sky_loadbalancer')).replace("sky_loadbalancer_id", device_id)
            url = f"http://{Config.get('src')['host']}{url_path}"
            sky_firewall_res = self.src_session.get(url).json()

        elif modelKey == "sky_switch_router":
            url_path = str(Config.get('get_sky_switch_router')).replace("sky_switch_router_id", device_id)
            url = f"http://{Config.get('src')['host']}{url_path}"
            sky_firewall_res = self.src_session.get(url).json()

        elif modelKey == "sky_gateway":
            url_path = str(Config.get('get_sky_gateway')).replace("get_sky_gateway_id", device_id)
            url = f"http://{Config.get('src')['host']}{url_path}"
            sky_firewall_res = self.src_session.get(url).json()

        src_res_data = jsonpath.jsonpath(sky_firewall_res, "$.data")[0]
        src_res_version_id = jsonpath.jsonpath(sky_firewall_res, "$.data.version")[0]
        return src_res_version_id, src_res_data

    def get_template_relation(self, src_version_id, template_relation):
        """
        获取src平台设备当前版本，找到dst关联的厂商、型号、版本id，返回出去
        :return:
        """
        dst_version_id = template_relation[src_version_id]["dst_id"]
        url_path = str(Config.get('version_template_info')).replace("version_id", dst_version_id)
        url = f"http://{Config.get('dst')['host']}{url_path}"
        res = self.dst_session.get(url).json()
        vendor = jsonpath.jsonpath(res, "$.data.vendorId")[0]
        device_type = jsonpath.jsonpath(res, "$.data.typeId")[0]
        version = jsonpath.jsonpath(res, "$.data.id")[0]
        assert version == dst_version_id, f"dst_id 与接口返回的version_id不一致{version},{dst_version_id}"
        logger.info("处理dst设备应该绑定的版本id")
        return vendor, device_type, version

    def handle_firewall_data(self, modelKey, device_info, vendor=None, device_type=None, version=None,
                             deviceGroup=None):
        """
        处理srt获取到的防火墙设备参数，进行处理新建需要的参数
        :return:
        """

        device_refined_info = ""
        if modelKey == "sky_firewall":
            keys_to_remove = ['id', 'deviceType', 'vendorName', 'vendorIcon', 'typeName', 'versionName', 'deviceGroup',
                              'deviceGroupName', 'credentialName', 'collectJobs', 'vendorSpecificSettings',
                              'deviceStateJobs', 'policyIdRange', 'haGroup', 'haGroupName', 'policyAnchor',
                              'natPolicyAnchor']
            refined_info = {k: v for k, v in device_info.items() if k not in keys_to_remove}
            refined_info['collectJobs'] = [
                {
                    "disabled": False,
                    "name": "连接状态检查",
                    "type": "REPEATED",
                    "value": "5",
                    "unit": "MINUTE",
                    "jobParam": None
                },
                {
                    "disabled": False,
                    "name": "配置采集",
                    "type": "REPEATED",
                    "value": "1",
                    "unit": "HOUR",
                    "jobParam": None
                },
                {
                    "disabled": False,
                    "name": "配置清理",
                    "type": "REPEATED",
                    "value": "1",
                    "unit": "DAY",
                    "jobParam": {
                        "sizeEnable": False,
                        "maxSize": "30",
                        "dayEnable": False,
                        "maxDay": "30",
                        "timeType": "DAY",
                        "routeConfig": {
                            "sizeEnable": False,
                            "maxSize": "30",
                            "dayEnable": False,
                            "maxDay": "30",
                            "timeType": "DAY"
                        }
                    }
                },
                {
                    "disabled": False,
                    "name": "路由采集",
                    "type": "REPEATED",
                    "value": "30",
                    "unit": "MINUTE",
                    "jobParam": None
                },
                {
                    "disabled": False,
                    "name": "策略命中数采集",
                    "type": "REPEATED",
                    "value": "1",
                    "unit": "DAY",
                    "jobParam": None
                }
            ]
            refined_info['collectType'] = "AUTOMATIC"
            refined_info['haGroup'] = []
            device_refined_info = refined_info
            logger.info(f"dst防火墙设备参数处理完成! {device_refined_info['name']}")
        elif modelKey == "sky_loadbalancer":
            keys_to_remove = ['id', 'deviceType', 'vendorName', 'vendorIcon', 'typeName', 'versionName', 'state',
                              'deviceGroupName',
                              'credentialName', 'vendorSpecificSettings', 'deviceStateJobs', 'confSetAddressRefType',
                              'singleObjectRefType', 'policyIdRange', 'workMode', 'haGroupName', 'collectJobs']
            refined_info = {k: v for k, v in device_info.items() if k not in keys_to_remove}
            refined_info['collectJobs'] = [
                {
                    "disabled": False,
                    "name": "连接状态检查",
                    "type": "REPEATED",
                    "value": "5",
                    "unit": "MINUTE",
                    "jobParam": None
                },
                {
                    "disabled": False,
                    "name": "配置采集",
                    "type": "REPEATED",
                    "value": "1",
                    "unit": "DAY",
                    "jobParam": None
                },
                {
                    "disabled": False,
                    "name": "配置清理",
                    "type": "REPEATED",
                    "value": "1",
                    "unit": "DAY",
                    "jobParam": {
                        "sizeEnable": False,
                        "maxSize": "30",
                        "dayEnable": False,
                        "maxDay": "30",
                        "timeType": "DAY",
                        "routeConfig": {
                            "sizeEnable": False,
                            "maxSize": "30",
                            "dayEnable": False,
                            "maxDay": "30",
                            "timeType": "DAY"
                        }
                    }
                }
            ]
            refined_info['collectType'] = "AUTOMATIC"
            refined_info['haGroup'] = []
            device_refined_info = refined_info
            logger.info(f"dst负载均衡设备参数处理完成! {device_refined_info['name']}")
        elif modelKey == "sky_switch_router":
            keys_to_remove = ['id', 'deviceType', 'vendorName', 'vendorIcon', 'typeName', 'versionName', 'state',
                              'deviceGroupName', 'credentialName', 'deviceStateJobs', 'confSetAddressRefType',
                              'singleObjectRefType', 'policyIdRange', ]
            refined_info = {k: v for k, v in device_info.items() if k not in keys_to_remove}
            refined_info['collectType'] = "AUTOMATIC"
            refined_info['collectJobs'] = [
                {
                    "disabled": False,
                    "name": "连接状态检查",
                    "type": "REPEATED",
                    "value": "5",
                    "unit": "MINUTE",
                    "jobParam": None
                },
                {
                    "disabled": False,
                    "name": "配置采集",
                    "type": "REPEATED",
                    "value": "1",
                    "unit": "DAY",
                    "jobParam": None
                },
                {
                    "disabled": False,
                    "name": "路由采集",
                    "type": "REPEATED",
                    "value": "30",
                    "unit": "MINUTE",
                    "jobParam": None
                },
                {
                    "disabled": False,
                    "name": "配置清理",
                    "type": "REPEATED",
                    "value": "1",
                    "unit": "DAY",
                    "jobParam": {
                        "sizeEnable": False,
                        "maxSize": "30",
                        "dayEnable": False,
                        "maxDay": "30",
                        "timeType": "DAY",
                        "routeConfig": {
                            "sizeEnable": False,
                            "maxSize": "30",
                            "dayEnable": False,
                            "maxDay": "30",
                            "timeType": "DAY"
                        }
                    }
                }
            ]
            device_refined_info = refined_info
            logger.info(f"dst路由交换设备参数处理完成! {device_refined_info['name']}")

        elif modelKey == "sky_gateway":
            keys_to_remove = ['id', 'deviceType', 'vendorName', 'vendorIcon', 'typeName', 'versionName',
                              'deviceGroupName',
                              'authoritySettings']
            refined_info = {k: v for k, v in device_info.items() if k not in keys_to_remove}
            device_refined_info = refined_info
            logger.info(f"dst虚拟网关设备参数处理完成! {device_refined_info['name']}")
        if vendor is not None:
            device_refined_info['vendor'] = vendor
        if device_type is not None:
            device_refined_info['type'] = device_type
        if version is not None:
            device_refined_info['version'] = version
        if deviceGroup is not None:
            device_refined_info['deviceGroup'] = deviceGroup
        device_refined_info['credential'] = self.add_credential_id

        # logger.info(f"新建设备使用参数 {json.dumps(device_refined_info)}")

        return device_refined_info

    def add_firewall(self, modelKey, data):
        """
        新增设备，获取id
        :param data:
        :param modelKey:
        :return:
        """
        if modelKey == "sky_firewall":
            add_sky_firewall_url = str(Config.get('add_sky_firewall'))
            url = f"http://{Config.get('dst')['host']}{add_sky_firewall_url}"
            add_firewall_res = self.dst_session.post(url, json=data).json()
            assert add_firewall_res['code'] == 200, f"新建设备失败{add_firewall_res}"
            logger.info(f"=================================新增防火墙完成！================================= {data['name']}")
            return add_firewall_res

        elif modelKey == "sky_loadbalancer":
            add_sky_loadbalancer_url = str(Config.get('add_sky_loadbalancer'))
            url = f"http://{Config.get('dst')['host']}{add_sky_loadbalancer_url}"
            add_sky_loadbalancer_res = self.dst_session.post(url, json=data).json()
            logger.info(add_sky_loadbalancer_res)
            assert add_sky_loadbalancer_res['code'] == 200, f"新建设备失败{add_sky_loadbalancer_res}"
            logger.info(f"=================================新增负载均衡完成！================================= {data['name']}")
            return add_sky_loadbalancer_res

        elif modelKey == "sky_switch_router":
            add_sky_switch_router_url = str(Config.get('add_sky_switch_router'))
            url = f"http://{Config.get('dst')['host']}{add_sky_switch_router_url}"
            add_sky_switch_router_res = self.dst_session.post(url, json=data).json()
            assert add_sky_switch_router_res['code'] == 200, f"新建设备失败{add_sky_switch_router_res}"
            logger.info(f"=================================新增路由交换完成！================================= {data['name']}")
            return add_sky_switch_router_res

        elif modelKey == "sky_gateway":
            sky_gateway_url = str(Config.get('add_sky_gateway'))
            url = f"http://{Config.get('dst')['host']}{sky_gateway_url}"
            sky_gateway_res = self.dst_session.post(url, json=data).json()
            assert sky_gateway_res['code'] == 200, f"新建设备失败{sky_gateway_res}"
            logger.info(f"=================================新增虚拟网关完成！================================= {data['name']}")
            return sky_gateway_res
        else:
            logger.info(f"不支持新增此类型号设备！ {data}")

    def get_cmdb_device_id(self, device_name, modelKey):
        """
        新建设备实时获取设备id，需要等到设备新建完成
        :return:
        """
        url_path = ""
        if modelKey == "sky_firewall":
            url_path = str(Config.get('get_cmdb_sky_firewall_id'))
        if modelKey == "sky_loadbalancer":
            url_path = str(Config.get('get_cmdb_sky_loadbalancer_id'))
        if modelKey == "sky_switch_router":
            url_path = str(Config.get('get_cmdb_sky_switch_router_id'))
        if modelKey == "sky_gateway":
            url_path = str(Config.get('get_cmdb_sky_gateway_id'))

        url = f"http://{Config.get('dst')['host']}{url_path}"
        data = {"name": device_name}
        cmdb_list_res = self.dst_session.post(url, json=data).json()
        assert cmdb_list_res['code'] == 200, f"CMDB列表查询失败{cmdb_list_res}"
        return cmdb_list_res

    def wiat_device_add(self, device_name, modelKey):
        """
        等待设备新建成功，有id返回，没有的话就等待2秒重新获取列表，等待30s，如果没有就报错。
        :return:
        """
        max_retries = 15  # 最大重试次数
        retries = 0
        device_get_id_path = f"$.data.list.[?(@.name=='{device_name}')].id"
        while retries < max_retries:
            cmdb_list_res = self.get_cmdb_device_id(device_name, modelKey)

            device_id = jsonpath.jsonpath(cmdb_list_res, device_get_id_path)
            if device_id:
                logger.info(f"=================================获取设备ID为 {device_id} =================================")
                return device_id[0]

            # 如果没有得到期望的值，等待两秒后进行下一次请求
            time.sleep(2)
            retries += 1

        # 达到最大重试次数仍然没有得到期望的值，可以选择抛出异常或者返回默认值
        raise Exception(f"==============={device_name}，{modelKey} 设备未获取到期望的值,请手动检查后重试脚本！！===============")

    def dst_fun(self, data, tag, dst_device_list):
        """
        目地址递归获取设备内容
        :return:
        """
        for child in data['child']:
            info_data = {
                "name": child["name"],
                "modelKey": child["modelKey"],
                "modelName": child["modelName"],
            }
            dst_device_list.append(info_data)
            self.dst_fun(child, tag + 1, dst_device_list)

    def dst_get_tree_data(self):
        """
        获取dst设备树，返回列表数据，以给到src判断是否存在重复数据，如果存在就不做新增动作，直接拿ip
        :return:
        """
        url = f"http://{Config.get('dst')['host']}{Config.get('get_device_tree_api')}"

        dst_device_data_res = self.dst_session.get(url).json()
        self.dst_device_data_res = dst_device_data_res

        dst_device_list = []
        for i in dst_device_data_res["data"]:
            self.dst_fun(i, 1, dst_device_list)
        return dst_device_list

    def src_fun(self, data, tag, dst_devices_list, project_id, template_relation, device_relation_list):
        """
        设备读写设备信息在dst环境新增
        :return:
        """
        # logger.info(self.dst_device_data_res)
        for child in data['child']:
            info_data = {
                "id": child["id"],
                "name": child["name"],
                "modelKey": child["modelKey"],
                "modelName": child["modelName"],
            }
            info_data_copy = info_data.copy()
            info_data_copy.pop("id")
            if tag == 1:
                if info_data_copy in dst_devices_list:
                    jsonpath_rule = f"$.data..[?(@.modelName=='{self.mapping[1]}' && @.name=='{info_data['name']}')].id"
                    sky_idc = jsonpath.jsonpath(self.dst_device_data_res, jsonpath_rule)[0]
                    logger.info(f"数据中心已存在，获取id {sky_idc} {info_data['name']}")
                else:
                    sky_idc = self.add_sky_idc({"name": info_data["name"], "desc": "move_devices"}, project_id)
                self.sky_idc = sky_idc
            elif tag == 2:
                if info_data_copy in dst_devices_list:
                    jsonpath_rule = \
                        f"$.data..child.[?(@.modelName=='{self.mapping[2]}' && @.name=='{info_data['name']}')].id"
                    sky_biz_domain_id = jsonpath.jsonpath(self.dst_device_data_res, jsonpath_rule)[0]
                    logger.info(f"业务域已存在，获取id {sky_biz_domain_id} {info_data['name']}")
                else:
                    sky_biz_domain_id = self.add_sky_biz_domain({"name": info_data["name"]}, self.sky_idc)
                self.sky_biz_domain_id = sky_biz_domain_id
                info_data["sky_idc"] = self.sky_idc
            else:
                # logger.info(self.mapping[tag], info_data_copy)
                if info_data_copy in dst_devices_list:
                    get_device_path = f"$..child[?(@.name=='{info_data['name']}' && @.modelKey=='{info_data['modelKey']}')].id"
                    device_id = jsonpath.jsonpath(self.dst_device_data_res, get_device_path)[0]
                    info_data["device_id"] = device_id
                    logger.info(f"[{info_data['name']}]:设备已存在，获取id: {device_id}")
                else:
                    if str(info_data["modelKey"]) == "sky_contrail":
                        logger.info("====================SND设备跳过====================")
                        continue

                    info_data["sky_biz_domain"] = self.sky_biz_domain_id
                    src_res_version_id, src_res_data = self.get_device_info(modelKey=info_data["modelKey"],
                                                                            device_id=info_data["id"])

                    vendor, device_type, version = self.get_template_relation(src_version_id=src_res_version_id,
                                                                              template_relation=template_relation)

                    add_device_data = self.handle_firewall_data(modelKey=info_data["modelKey"],
                                                                device_info=src_res_data,
                                                                vendor=vendor,
                                                                device_type=device_type,
                                                                version=version,
                                                                deviceGroup=self.sky_biz_domain_id)

                    if str(info_data["modelKey"]) == "sky_gateway":
                        self.add_firewall(modelKey=info_data["modelKey"],
                                          data=add_device_data)

                        device_id = self.wiat_device_add(device_name=info_data["name"],
                                                         modelKey=info_data["modelKey"])
                        info_data["device_id"] = device_id
                    elif add_device_data["protocol"]:
                        self.add_firewall(modelKey=info_data["modelKey"],
                                          data=add_device_data)

                        device_id = self.wiat_device_add(device_name=info_data["name"],
                                                         modelKey=info_data["modelKey"])
                        info_data["device_id"] = device_id
                    else:
                        logger.info(
                            f"========={self.mapping[tag]} 连接协议为空，为假设备，不新建====={info_data_copy}====================",
                        )
            device_relation_list.append(info_data)
            # logger.info(self.mapping[tag], info_data)
            self.src_fun(child, tag + 1, dst_devices_list, project_id, template_relation, device_relation_list)

    def read_write_devices(self, template_relation):
        """
        同步设备
        :return:
        """
        device_relation_list = []
        url = f"http://{Config.get('src')['host']}{Config.get('get_device_tree_api')}"
        self.add_credential_id = self.add_credential()
        src_device_data_res = self.src_session.get(url).json()
        dst_devices_list = self.dst_get_tree_data()
        for i in src_device_data_res["data"]:
            self.src_fun(i, 1, dst_devices_list, i["id"], template_relation, device_relation_list)
        # logger.info(device_relation_list)
        return device_relation_list

if __name__ == '__main__':
    Device().read_write_devices("aa")
