#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/22 14:56
# @Author  : qingping.niu
# @File    : ScreenLockPage.py
# @desc    : 锁屏设置(图案,password,PIN)

from PageObject.BasePage import BasePage
from Utils.Decorator import *

class ScreenLockPage(BasePage):

    @teststep
    def wait_page(self):
        try:
            if self.d(text='Settings').wait(timeout=10):
                pass
            else:
                raise Exception('Not in HomePage')
        except Exception:
            raise Exception('Not in HomePage')


    @teststep
    def screenLock_click(self):
        self.d(scrollable=True).scroll.to(text=u"Screen lock")
        self.d(text=u"Screen lock").click()

    @teststep
    def pattern_click(self):
        self.d(text=u"Pattern").click()

    @teststep
    def draw_pattern(self,*number):
        dict = {}
        pointList = []
        self.d(className="android.view.ViewGroup").wait(timeout=10)
        for elem in self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").all():
            index = elem.attrib.get("index")
            position = elem.center()
            index = int(index)+1
            dict.update({index: position})

        for i in number:
            point = dict[i]
            pointList.append(point)

        self.d.swipe_points(pointList,0.2)
        self.d.xpath("//android.widget.TextView[@text='Draw pattern again to confirm']").wait(timeout=10)
        # self.d(className="android.view.ViewGroup").wait(timeout=10)
        self.d.swipe_points(pointList,0.2)

    @teststep
    def screen_on_off(self):
        self.d.screen_off()
        status = self.d.info.get('screenOn') #屏幕状态
        self.d.screen_on()

    @teststep
    def screen_swipe_up(self):
        self.swipe_up()

    @teststep
    def unlock_pattern(self,*number):

        pointList = []
        # self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").wait(timeout=10)
        for elem in self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").all():
            index = elem.attrib.get("index")
            position = elem.center()
            index = int(index)+1
            dict.update({index: position})

        for i in number:
            point = dict[i]
            pointList.append(point)

        self.d.swipe_points(pointList,0.2)

    @teststep
    def pin_click(self):
        self.d(text=u"PIN").click()

    @teststep
    def draw_pin(self,*number):
        """ PIN 顺序是打乱的,需自定义调整顺序"""
        pointList = []
        dict = ScreenLockPage.getPinLockid()
        for i in number:
            point = dict[i]
            pointList.append(point)

        self.d.swipe_points(pointList,0.2)
        self.d(text="Enter PIN again to confirm").wait(timeout=10)
        self.d.swipe_points(pointList, 0.2)

    @teststep
    def unlock_pin(self,*number):
        self.d(className="android.view.ViewGroup").wait(timeout=10)
        dict = ScreenLockPage().getPinLockid()
        pointList = []
        for i in number:
            point = dict[i]
            pointList.append(point)

        self.d.swipe_points(pointList,0.2)

    @classmethod
    def getPinLockid(self):
        """ 拼接Pin顺序"""
        dict = {}
        for elem in self.d.xpath("//android.view.ViewGroup/android.widget.ImageView").all():
            index = elem.attrib.get("index")
            position = elem.center()
            index = int(index)+1
            if index == 2:
                dict.update({4: position})
            elif index == 3:
                dict.update({2: position})
            elif index == 4:
                dict.update({3: position})
            elif index == 6:
                dict.update({7: position})
            elif index == 7:
                dict.update({0: position})
            elif index == 8:
                dict.update({6: position})
            elif index == 9:
                dict.update({8: position})
            elif index == 10:
                dict.update({9: position})
            else:
                dict.update({index: position})

        return dict














