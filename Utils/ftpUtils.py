#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/11 13:38
# @Author  : qingping.niu
# @File    : ftpUtils.py
# @desc    :

from ftplib import FTP
from Utils.Log import Log
import os

host = "10.128.208.198"
port=2121
username = "anonymous"
password = "tcl@1234"


def connectFTP():
    ftp = FTP()  # 实例化FTP对象
    ftp.connect(host, port)
    ftp.login(username, password)  # 登录
    # ftp.getwelcome()  # 打印欢迎信息
    return ftp


def ftp_downloadFile(locatpath,romatepath):
    ftp = connectFTP()
    '''下载安装包并返回路径'''
    bufsize = 1024
    ftp.cwd(romatepath)  # 设置FTP目标路径
    list = ftp.nlst()  # 获取目录下的文件,获得目录列表
    files = []
    for name in list:
        files.append(name)

    targetfilename = list[len(list) - 2]  # 取最新的debug版本
    locatpath = os.path.join(locatpath, targetfilename)
    fp = open(locatpath, 'wb')
    ftp.retrbinary('RETR %s' % targetfilename, fp.write, bufsize)
    ftp.close()
    return locatpath