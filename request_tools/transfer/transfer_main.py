#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import yaml
from .filelog import logger
from .move_device import Device
from .move_config import MoveConfig
from .move_topo import MoveTopo
from .common import ensure_path_sep, get_yaml_data


def transfer_main(new_data, transfer_action):
    Config = get_yaml_data(ensure_path_sep("\\transfer\\config.yaml"))
    if transfer_action is None:
        filedata = "请选择有效的动作！"
        return filedata

    Config['src'].update(new_data['src'])
    Config['dst'].update(new_data['dst'])

    with open(ensure_path_sep("\\transfer\\config.yaml"), 'w') as file:
        yaml.dump(Config, file, default_flow_style=False)

    if transfer_action == 1:
        logger.info("=====================同步模版===========================")
        Device().read_write_template()
    elif transfer_action == 2:
        logger.info("=====================同步模版与设备===========================")
        template_relation = Device().read_write_template()
        Device().read_write_devices(template_relation)
    elif transfer_action == 3:
        logger.info("=====================同步模版、设备、配置===========================")
        template_relation = Device().read_write_template()
        device_relation = Device().read_write_devices(template_relation)
        MoveConfig(device_relation).read_write_config()
    elif transfer_action == 4:
        logger.info("=====================同步模版、设备、拓扑===========================")
        template_relation = Device().read_write_template()
        device_relation = Device().read_write_devices(template_relation)
        MoveTopo(device_relation).read_write_topo()
    elif transfer_action == 5:
        logger.info("=====================同步所有，模版、设备、配置、拓扑=====================")
        template_relation = Device().read_write_template()
        device_relation = Device().read_write_devices(template_relation)
        MoveConfig(device_relation).read_write_config()
        MoveTopo(device_relation).read_write_topo()
    else:
        logger.info("=====================请输入正确的数字，详情请看help=====================")

    with open(ensure_path_sep("\\transfer\\transfer.log"), 'r') as f:
        filedata = f.read()
    return filedata
