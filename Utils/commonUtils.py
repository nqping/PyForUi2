#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 15:14
# @Author  : qingping.niu
# @File    : commonUtils.py
# @desc    :

import apkutils,os
from Utils.Log import Log

log = Log()

def write_file(localFile,data):
    '''

    :param localFile: 本地文件路径
    :param data: 写入数据
    :return:
    '''

    if not os.path.exists(localFile):
        os.mknod(localFile)

    with open(localFile,'w',encoding='utf-8') as file:
        for i in data:
            file.write(i)
        # file.write(str(data))


def write_file_mkdir(crashLogPath,localFile,data):
    """
    需要创建目录
    :param crashLogPath:
    :param localFile:
    :param data:
    :return:
    """

    if not os.path.exists(crashLogPath):
        os.makedirs(crashLogPath)

    log.i('carsh file path: %s ',localFile)
    with open(localFile,'w',encoding='utf-8') as file:
        for i in data:
            file.write(i)


def get_apk_info(path):
    '''
    获取安装包versionName,versionCode,package 等信息
    :param apk_path: apk文件本地路径
    :return: info[]
    '''
    tmp = apkutils.APK(path).get_manifest()
    info = {}
    info['versionCode'] = str(tmp.get('@android:versionCode'))
    info['versionName'] = str(tmp.get('@android:versionName'))
    info['package'] = str(tmp.get('@package'))
    return info
