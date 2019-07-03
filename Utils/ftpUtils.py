#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/11 13:38
# @Author  : qingping.niu
# @File    : ftpUtils.py
# @desc    :

from ftplib import FTP
from Utils.Log import Log
import os
import re
import urllib3
import requests

host = "10.128.208.198"
port=2121
username = "anonymous"
password = "tcl@1234"

# log = Logger(logger='NetworkingProtocol').getlog()
log = Log()

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


def http_downloadFile(locatpath,url):
    '''
    http协议下载文件
    :param locatpath: 本地存储路径
    :param url: 网络文件路径
    :return: 本地完整体路径
    '''
    #网络路径拼装处理
    urllib3.disable_warnings() #忽略警告
    rs = requests.get(url,verify=False).text
    list = re.findall(r'<a.*?href="([^"]*)".*?>', rs)
    list.reverse() #反转
    dir = '%s%s' % (url, list[0])
    rs = requests.get(dir,verify=False).text
    apk_name = re.findall(r'<a.*?href="([^"].*\.apk)"', rs)
    full_url = '%s%s'%(dir,apk_name[0])
    log.i('目标apk %s:' % full_url)

    #判断本地目标目录是否存在
    if os.path.isdir(locatpath):
        pass
    else:
        os.makedirs(locatpath)

    locatpath = os.path.join(locatpath, apk_name[0])
    log.i('本地路径 %s:'%locatpath)

    r = requests.get(full_url,verify=False)
    with open(locatpath,'wb') as data:
        data.write(r.content)

    return locatpath







if __name__=='__main__':
    ftp = FTP()
    ftp.connect()
    ftp.cwd(' ftp = FTP()')