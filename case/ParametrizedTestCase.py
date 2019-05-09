#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/6 11:24
# @Author  : qingping.niu
# @File    : ParametrizedTestCase.py
# @desc    : 重构TestCase构造方法增加param参数

import unittest

class ParametrizedTestCase(unittest.TestCase):
    """
    参数化测试用例,从此类继承
    """
    def __init__(self,methodName='runTest',param=None):
        super(ParametrizedTestCase,self).__init__(methodName)
        self.param = param

    @staticmethod
    def parametrize(testcase_class,param):
        """
        创建一个包含给定的子类，将参数“param”传递给它们
        """
        testloader = unittest.TestLoader()
        testnames = testloader.getTestCaseNames(testcase_class)
        suite = unittest.TestSuite()
        for name in testnames:
            suite.addTest(testcase_class(name,param))

        return suite

