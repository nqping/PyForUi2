#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 11:29
# @Author  : qingping.niu
# @File    : run_monkey.py
# @desc    :

import argparse
from monkey.Drivers_monkey import DriversMonkey


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", required=False, help="ip")
    ap.add_argument("-m","--method", required=True,help="method")
    ap.add_argument("-c","--command",required=False, help="command")
    args = vars(ap.parse_args())
    tempip = args['ip']
    method = args['method']
    command = args['command']

    # tempip=['192.168.95.4','192.168.95.2'] #192.168.95.4
    # method = 'IP'
    # command = 'monkey -p com.tcl.joylockscreen -v 1000'

    DriversMonkey().run(method=method,ip=tempip,command=command)



