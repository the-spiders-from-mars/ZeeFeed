# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    User Data Manager
"""
from cloudant import Cloudant
from cloudant.adapters import Replay429Adapter

import config

__author__ = "freemso"


class UserDataManager:
    def __init__(self):
        self.client = Cloudant(config.CLOUDANT_USER_NAME, config.CLOUDANT_USER_PASS,
                               account=config.CLOUDANT_ACCOUNT_NAME, connect=True,
                               adapter=Replay429Adapter(retries=10, initialBackoff=0.01),
                               timeout=300)

