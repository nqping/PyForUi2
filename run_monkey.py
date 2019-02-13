#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 11:29
# @Author  : qingping.niu
# @File    : run_monkey.py
# @desc    :

import subprocess
import argparse

import uiautomator2 as u2
from monkey.Drivers_monkey import DriversMonkey
from Utils.ftpUtils import ftp_downloadFile


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", required=False, help="ip")
    ap.add_argument("-m","--method", required=True,help="method")
    ap.add_argument("-c","--command",required=False, help="command")
    args = vars(ap.parse_args())
    tempip = args['ip']
    method = args['method']
    command = args['command']

    ips=[]
    if tempip:
        ips = tempip.split(',')

    # method='USB'
    # ips=['HQJNHEKBK7UGJ78S']
    # command="monkey -p com.video.agl -v 10000 > /sdcard/monkey_log.txt"

    DriversMonkey().run(method=method,ip=ips,command=command)
    print('start export monkey log-------')
    if len(ips) > 0:
        for i in ips:
            subprocess.getoutput('adb -s %s pull /sdcard/monkey_log.txt F:\\temp\\packages\\log'%i)








