#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 10:52
# @Author  : qingping.niu
# @File    : test_02_feedback.py
# @desc    :
import unittest

from PageObject.FeedbackPage import FeedbackPage
from PageObject.BasePage import BasePage
from Utils.Decorator import *


class TestFeedback(unittest.TestCase,BasePage):
    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_start("com.tcl.joylockscreen")
        # pass

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop("com.tcl.joylockscreen")

    @testcase
    def test_01_submitFeedback(self):
        FeedbackPage().feedback_click()
        FeedbackPage().inputContent("这个是测试使用请忽略")
        FeedbackPage().submit()
        toast = self.get_toast_message()
        assert "Thanks for your feedback" in toast
        print("提交后返回toast信息:\n%s"%toast)
        self.assertIn('Thanks for your feedback', toast)



