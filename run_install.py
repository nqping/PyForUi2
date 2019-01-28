#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 12:42
# @Author  : qingping.niu
# @File    : run_install.py
# @desc    : 安装应用

import uiautomator2 as u2

from ftplib import FTP
import os,subprocess,argparse

host = "10.128.208.198"
port=2121
username = "anonymous"
password = "tcl@1234"

ftp = FTP()  # 实例化FTP对象
ftp.connect(host,port)
ftp.login(username, password)  # 登录
ftp.getwelcome() #打印欢迎信息


def ftp_downloadFile(locatpath,romatepath):
    bufsize = 1024
    ftp.cwd(romatepath)#设置FTP目标路径
    list = ftp.nlst()# 获取目录下的文件,获得目录列表
    files = []
    for name in list:
        files.append(name)

    targetfilename =list[len(list) - 2] #取最新的debug版本
    locatpath =os.path.join(locatpath,targetfilename)
    fp = open(locatpath, 'wb')
    ftp.retrbinary('RETR %s' % targetfilename, fp.write, bufsize)
    ftp.close()
    return locatpath


def getDevices(ip):
    d = u2.connect(ip)
    device = d.device_info
    return device

def installApp(device,filepath):
    cmd ="adb -s %s install -r %s"%(device,filepath)
    output = subprocess.getoutput(cmd=cmd)
    print(output)

def clearDir(appPath):
    if os.path.isfile(appPath): #判断是否文件路径
        os.remove(appPath)

if __name__ =='__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", required=False, help="ip")
    ap.add_argument("-p", "--path", required=True, help="path")
    ap.add_argument("-r", "--remotepath", required=True, help="remotepath")
    args = vars(ap.parse_args())
    tempip = args['ip']
    localpath = args['path']
    romatepath = args['remotepath']

    device = getDevices(tempip[0])
    # localpath = 'F:/temp/packages'
    romatepath = "/AGL Video"
    if device != {}:
        appPath = ftp_downloadFile(localpath,romatepath)
        installApp(device['serial'],appPath)

