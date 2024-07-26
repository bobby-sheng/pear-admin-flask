#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import ipaddress
import random


def generate_ips(subnet, num_ips):
    ipss = []
    try:
        network = ipaddress.ip_network(subnet)
        ips = [str(ip) for ip in network.hosts()]
        for i in range(num_ips):
            ipss.append(random.choice(ips))
        return ipss
    except ValueError as e:
        return str(e)


def random_ip(num_ips):
    ipc = []
    for _ in range(num_ips):
        ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
        ipc.append(ip)
    return ipc
