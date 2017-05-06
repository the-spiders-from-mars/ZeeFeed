# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    OpenWhisk python action
"""

__author__ = "freemso"

def main(args):
    # parse args to get input
    sources = args.get("sources", ["https://daringfireball.net/feeds/main"])

    for source in sources:

