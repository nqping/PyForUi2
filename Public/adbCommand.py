#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/13 15:08
# @Author  : qingping.niu
# @File    : adbCommand.py
# @desc    :

import subprocess,os

def get_pid(devices,grepname):
    '''获取进程PID'''
    cmd = 'adb -s %s shell ps |findstr %s' % (devices,grepname)
    output = os.popen(cmd).read()
    pid = None
    if output != "":
        pid = output.split()[1]

    return pid

def kill_process(devices,pid):
    #获取android系统版本
    killcmd = 'adb -s %s shell kill %s'%(devices,pid)
    subprocess.getoutput(killcmd)



if __name__=='__main__':
    pid = get_pid('a96cd66d', 'logcat')
    print(pid)