#!/usr/bin/env python3.10.6
# -*- coding: utf-8 -*-
# Author: Bobby Sheng <Bobby@sky-cloud.net>
import logging
import time
from .common import ensure_path_sep

# create logger
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# create FileHandler
filehandler = logging.FileHandler(ensure_path_sep("\\transfer\\transfer.log"), mode='w')
filehandler.setLevel(logging.INFO)

# create StreamFilehandler
streamhandler = logging.StreamHandler()
streamhandler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter.datefmt = "%Y-%m-%d %H:%M:%S"

filehandler.setFormatter(formatter)
streamhandler.setFormatter(formatter)

logger.addHandler(filehandler)
logger.addHandler(streamhandler)
