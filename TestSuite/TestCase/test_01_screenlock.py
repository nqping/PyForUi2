#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/26 14:32
# @Author  : qingping.niu
# @File    : test_01_screenlock.py
# @desc    : 上锁,解锁

import unittest

from PageObject.ScreenLockPage import ScreenLockPage
from Utils.Decorator import *


class TestScreenLock(unittest.TestCase,BasePage):
    @classmethod
    @setupclass
    def setUpClass(cls):
        cls.d.app_start("com.tcl.joylockscreen")
        # pass

    @classmethod
    @teardownclass
    def tearDownClass(cls):
        cls.d.app_stop("com.tcl.joylockscreen")

    @teststep
    def test_01_setPattern(self):
        ScreenLockPage().screenLock_click()
        ScreenLockPage().pattern_click()
        ScreenLockPage().draw_pattern(1,2,3,6,9)

        ScreenLockPage().screen_on_off()
        ScreenLockPage().screen_swipe_up()
        ScreenLockPage().unlock_pattern(1,2,3,6,9)
        ele = self.d(text="Settings")
        self.assertEqual(ele.get_text(), 'Settings')

    @teststep
    def test_02_setPin(self):
        ScreenLockPage().screenLock_click()
        ScreenLockPage().unlock_pattern(1, 2, 3, 6, 9)
        ScreenLockPage().pin_click()
        ScreenLockPage().draw_pin(1, 2, 3, 6)
        ScreenLockPage().screen_on_off()
        ScreenLockPage().screen_swipe_up()
        ScreenLockPage().unlock_pattern()

    @teststep
    def test_03_cleardata(self):
        ScreenLockPage().screenLock_click()
        ScreenLockPage().draw_pin(1, 2, 3, 6)
        ScreenLockPage().screen_swipe_up()










