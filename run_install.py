#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 12:42
# @Author  : qingping.niu
# @File    : run_install.py
# @desc    : 安装应用

import uiautomator2 as u2
import argparse
from Utils.ftpUtils import ftp_downloadFile
from Public.Drivers_install import DriversInstall

if __name__ =='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", required=False, help="ip")
    ap.add_argument("-p", "--path", required=True, help="path")
    ap.add_argument("-m","--method",required=True, help="method")
    args = vars(ap.parse_args())
    tempip = args['ip']
    ftpDst = args['path']
    method = args['method']
    ips = tempip.split(',')

    # ips=['192.168.95.4','192.168.95.3']
    # # print(ip[0])
    # path = "F:\\temp\\packages\\download"
    # romatepath="/AGL Video"
    # apkPath = ftp_downloadFile(path,romatepath)

    # tempip = '192.168.95.4,192.168.95.3'  # 192.168.95.4
    # method = 'IP'
    # ftpDst = '/AGL Video'
    # ip = tempip.split(',')

    locatpath = 'F:\\temp\\packages\\download'
    apkPath = ftp_downloadFile(locatpath, ftpDst)

    DriversInstall().run(method=method,ip=ips,apkPath=apkPath)

