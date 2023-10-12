#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
from request_tools.other_tools.write_fs import update_document
from request_tools.other_tools.write_fs import get_feishu_list

def gorun():
    update_document.LinkFeiShu().write_feishu()


def get_info():
    feishu_data, total = get_feishu_list.LinkFeiShu_V2().get_info_list()
    return feishu_data, total


def get_all_info(summary=None, assignee=None, description=None, priority=None, record_id=None):
    res = get_feishu_list.LinkFeiShu_V2().get_all_data(summary=summary, assignee=assignee, description=description,
                                                       priority=priority, record_id=record_id)
    return res



if __name__ == '__main__':
    get_info()
