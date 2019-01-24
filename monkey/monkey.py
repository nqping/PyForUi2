#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 10:33
# @Author  : qingping.niu
# @File    : monkey.py
# @desc    :

import uiautomator2 as u2

class Monkey:

    def __init__(self,devices):
        self.device = devices

    def get_device(self):
        return self.device

    # def getInfo(self,ip,comd):
    #     d = u2.connect(ip)
    #     deviceinfo = d.device_info
    #
    #     serial = deviceinfo['serial']
    #     cmd = 'adb shell -s %s monkey -p com.tcl.joylockscreen -v 1000' %serial
    #
    #     output,exit_code = d.adb_shell("monkey -p com.tcl.joylockscreen -v 1000")
    #     print(output)
    #     print(exit_code)





if __name__=='__main__':
    monkey = Monkey()
    monkey.runMonkey('192.168.95.2')