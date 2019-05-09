#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/18 13:44
# @Author  : qingping.niu
# @File    : case.py
# @desc    : 运行monkey相关的一些用例

from Utils.Decorator import *
from case.ParametrizedTestCase import ParametrizedTestCase

class myCase(ParametrizedTestCase,BasePage):

    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_stop_all()


    @testcase
    def test_install_login(self):
        '''
        将本地apk安装包push到设备指定目录下
        '''
        self.local_install(self.param)


