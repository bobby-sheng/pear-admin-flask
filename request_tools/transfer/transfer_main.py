#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import yaml
import logging
from .move_device import Device
from .move_config import MoveConfig
from .move_topo import MoveTopo
from .common import ensure_path_sep, get_yaml_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def transfer_main(new_data, transfer_action):
    Config = get_yaml_data(ensure_path_sep("\\transfer\\config.yaml"))

    Config['src'].update(new_data['src'])
    Config['dst'].update(new_data['dst'])

    with open(ensure_path_sep("\\transfer\\config.yaml"), 'w') as file:
        yaml.dump(Config, file, default_flow_style=False)

    return new_data, transfer_action, Config
    # if transfer_action == 1:
    #     logging.info("=====================同步模版===========================")
    #     Device().read_write_template()
    # elif transfer_action == 2:
    #     logging.info("=====================同步模版与设备===========================")
    #     template_relation = Device().read_write_template()
    #     Device().read_write_devices(template_relation)
    # elif transfer_action == 3:
    #     logging.info("=====================同步模版、设备、配置===========================")
    #     template_relation = Device().read_write_template()
    #     device_relation = Device().read_write_devices(template_relation)
    #     MoveConfig(device_relation).read_write_config()
    # elif transfer_action == 4:
    #     logging.info("=====================同步模版、设备、拓扑===========================")
    #     template_relation = Device().read_write_template()
    #     device_relation = Device().read_write_devices(template_relation)
    #     MoveTopo(device_relation).read_write_topo()
    # elif transfer_action == 5:
    #     logging.info("=====================同步所有，模版、设备、配置、拓扑=====================")
    #     template_relation = Device().read_write_template()
    #     device_relation = Device().read_write_devices(template_relation)
    #     MoveConfig(device_relation).read_write_config()
    #     MoveTopo(device_relation).read_write_topo()
    # else:
    #     logging.info("=====================请输入正确的数字，详情请看help=====================")
