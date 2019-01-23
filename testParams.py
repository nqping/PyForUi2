#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/23 15:00
# @Author  : qingping.niu
# @File    : testParams.py
# @desc    :
import argparse

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "-ip", required=True, help="ip")
    args = vars(ap.parse_args())

    print(args['ip'])