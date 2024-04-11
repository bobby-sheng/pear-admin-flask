#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import jsonpath
from .filelog import logger
from .move_device import Device
from .common import ensure_path_sep, get_yaml_data

Config = get_yaml_data(ensure_path_sep("\\transfer\\config.yaml"))


class MoveConfig(Device):

    def __init__(self, device_relation):
        super().__init__()
        self.device_relation = device_relation

    def get_src_config(self, config_type, device_name, device_id):
        """
        获取源环境的设备路由配置文件，没有就打印设备信息没有配置。不做下一步动作。
        如果存在配置文件，获取配置文件详情接口，获取dst的上传配置接口参数
        :return:
        """
        if config_type == "config":
            get_config_url_path = 'get_device_config_list'
            get_config_info_url_path = 'get_device_config_info'
        else:
            get_config_url_path = 'get_device_config_route_list'
            get_config_info_url_path = 'get_device_config_route_info'

        url_path = str(Config.get(get_config_url_path)).replace("device_id", device_id)
        url = f"http://{Config.get('src')['host']}{url_path}"
        res = self.src_session.get(url).json()
        assert res['code'] == 200, f"读取{config_type}模版列表失败{res}"
        if jsonpath.jsonpath(res, "$.data.count")[0] == 0:
            logger.info(f"设备 [{device_name}] {config_type}配置为空，跳过")
            config_route_raw = "NO CONFIG!"
        else:
            config_route_id = jsonpath.jsonpath(res, "$.data.list[0]..id")[0]
            route_url_path = str(Config.get(get_config_info_url_path)).replace("config_id", config_route_id)
            url = f"http://{Config.get('src')['host']}{route_url_path}"
            route_res = self.src_session.get(url).json()
            assert route_res['code'] == 200, f"获取{config_type}详情失败{route_res}"
            config_route_raw = jsonpath.jsonpath(route_res, "$.data.raw")[0]
        return config_route_raw

    def dst_add_config(self, config_type, modelKey, device_name, device_id, config_raw):
        """
        目的接口上传配置文件并且设置为当前
        :return:
        """
        if config_type == "config":
            add_config_url_path = 'add_device_config'
            add_config_info_url_path = 'choose_device_config'
            api_marker = "config_id"
        else:
            add_config_url_path = 'add_device_config_route'
            add_config_info_url_path = 'choose_device_config_route'
            api_marker = "route_id"
        dst_add_config_url = str(Config.get(add_config_url_path))

        url = f"http://{Config.get('dst')['host']}{dst_add_config_url}"
        data = {"deviceId": device_id,
                "deviceType": modelKey,
                "raw": config_raw,
                "source": "admin",
                "updatedAt": "1705043703342"
                }
        dst_add_config_res = self.dst_session.post(url, json=data).json()
        assert dst_add_config_res['code'] == 200, f"目的环境上传配置文件失败{dst_add_config_res}"
        dst_add_config_id = jsonpath.jsonpath(dst_add_config_res, "$.data.id")[0]

        choose_device_config_path = str(Config.get(add_config_info_url_path)).replace("device_id", device_id).replace(
            api_marker, dst_add_config_id)
        choose_device_config_url = f"http://{Config.get('dst')['host']}{choose_device_config_path}"
        choose_device_config_res = self.dst_session.patch(choose_device_config_url).json()
        assert choose_device_config_res['code'] == 200, f"目的环选择当前配置文件失败{choose_device_config_res}"
        logger.info(f"[{device_name},{device_id}] 设备上传{config_type}配置文件成功")

    def sky_firewall_add_config(self, up_type, device_data):
        """
        防火墻等存在路由和配置的设备上传方法
        :return:
        """
        if up_type != "sky_loadbalancer":
            for i in ["config", "route_config"]:
                config_route_raw = self.get_src_config(config_type=i,
                                                       device_id=device_data['id'],
                                                       device_name=device_data['name'])
                if "NO CONFIG!" == config_route_raw:
                    return False
                else:
                    self.dst_add_config(config_type=i,
                                        modelKey=device_data["modelKey"],
                                        device_id=device_data["device_id"],
                                        config_raw=config_route_raw,
                                        device_name=device_data['name'])
        else:
            config_route_raw = self.get_src_config(config_type="config",
                                                   device_id=device_data['id'],
                                                   device_name=device_data['name'])
            if "NO CONFIG!" == config_route_raw:
                return False
            else:
                self.dst_add_config(config_type="config",
                                    modelKey=device_data["modelKey"],
                                    device_id=device_data["device_id"],
                                    config_raw=config_route_raw,
                                    device_name=device_data['name'])

    def read_write_config(self):
        """
        读取src设备配置文件，上传到dst环境对应的设备中
        :return:
        """
        for i in self.device_relation:
            if "device_id" in i:
                self.sky_firewall_add_config(i["modelKey"], i)

