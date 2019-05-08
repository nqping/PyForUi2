#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 19:45
# @Author  : qingping.niu
# @File    : FeedbackPage.py
# @desc    : 用户反馈

from PageObject.BasePage import BasePage
from Utils.Decorator import *


class FeedbackPage(BasePage):

    @teststep
    def feedback_click(self):
        self.d(scrollable=True).scroll.toEnd()
        self.d(text=u"Feedback").click()

    @teststep
    def inputContent(self,sendText):
        self.d(resourceId="com.tcl.joylockscreen:id/feedback_content").set_text(sendText)
        self.d(resourceId="com.tcl.joylockscreen:id/contact_information").set_text("qingping.niu@tcl.com")

    @teststep
    def submit(self):
        self.d(resourceId="com.tcl.joylockscreen:id/submit").click()

