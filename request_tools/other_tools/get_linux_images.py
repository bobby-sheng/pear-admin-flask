#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>

data = """cmdb:1.1.2
eventti:1.0.0
gway:1.0.0
httpd:1.1.0
inet-client:0.2.0
inet-client-java:0.0.1-0a5bd938c1e-12
inet-ngparser:0.1.0
inet-platform:1.4.0
inet-workflow:1.0.0
json-adaptor:1.0.4
logsystem:2.0.1
netc:1.8.0
netd:1.2.3
nginx:1.5.0
pipeline:bugfix-INET-125-8ee6940209a-2
policyinsight:bugfix-INET-251-d7321db3dc6-2
trigger:1.1.1

"""
from request_tools.models.model import IMages


class GetImages:

    def string_to_dict(self, input_string):
        data = {}
        lines = input_string.strip().split('\n')
        for line in lines:
            key, value = line.split(':')
            data[key.strip()] = value.strip()
        return data


if __name__ == '__main__':
    GetImages().string_to_dict(data)
