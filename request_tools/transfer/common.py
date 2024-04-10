#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import os
from typing import Text
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

import yaml


def root_path():
    """ 获取 根路径 """
    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return path


def ensure_path_sep(path: Text) -> Text:
    """兼容 windows 和 linux 不同环境的操作系统路径 """
    if "/" in path:
        path = os.sep.join(path.split("/"))

    if "\\" in path:
        path = os.sep.join(path.split("\\"))

    return root_path() + path


def get_yaml_data(file_dir):
    if os.path.exists(file_dir):
        data = open(file_dir, 'r', encoding='utf-8')
        yaml_data = yaml.load(data, Loader=yaml.FullLoader)
        return yaml_data


def encrypt_password(key, password):
    if not key:
        raise Exception("key can not be none.")
    if not password:
        raise Exception("password can not be none.")
    aes_key = base64.b64decode(key)
    cipher = AES.new(aes_key, mode=AES.MODE_ECB)
    data = bytes(password, "utf-8")
    pad_data = pad(data, 16)
    encrypted_pass = base64.b64encode(cipher.encrypt(pad_data))
    return encrypted_pass.decode("utf-8")

