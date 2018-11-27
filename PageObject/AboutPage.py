#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/22 15:40
# @Author  : qingping.niu
# @File    : AboutPage.py
# @desc    : 关于我们页面

from PageObject import BasePage
from Utils.Decorator import *

class AboutPage(BasePage):

    @teststep
    def about_click(self):
        self.d(text=u"About").click()


