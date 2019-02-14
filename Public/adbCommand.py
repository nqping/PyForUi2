#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/13 15:08
# @Author  : qingping.niu
# @File    : adbCommand.py
# @desc    :

import subprocess

def get_pid(devices,grepname):
    '''获取进程PID'''
    cmd = 'adb -s %s shell ps |findstr %s' % (devices,grepname)
    output = subprocess.getstatusoutput(cmd)
    if output[0] == 1:
        pid = None
    else:
        pid = output[1].split()[1]
    # print('%s pid=%s'%(grepname,pid))
    return pid

def kill_process(devices,pid):
    #获取android系统版本
    killcmd = 'adb -s %s shell kill %s'%(devices,pid)
    subprocess.getoutput(killcmd)


