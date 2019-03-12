#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 15:14
# @Author  : qingping.niu
# @File    : fileUtils.py
# @desc    :


def write_file(localFile,data):
    '''

    :param localFile: 本地文件路径
    :param data: 写入数据
    :return:
    '''
    with open(localFile,'w',encoding='utf-8') as file:
        for i in data:
            file.write(i)
        # file.write(str(data))