#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 10:33
# @Author  : qingping.niu
# @File    : monkey.py
# @desc    :

import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--d", required=True, help="ip")
    args = vars(ap.parse_args())
    tempip = args['ip']
    print("***"+tempip)