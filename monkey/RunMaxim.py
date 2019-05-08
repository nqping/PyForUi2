#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,time
import unittest


class RunMaxim:
    def __init__(self, device=None,apkinfo=None):
        # self.log_dir = 'F:\\mibctestFTP\\monkeyLog'
        # self.test_report_root = './MaximReport'

        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        self.test_report_root = os.path.join('F:\\mibctestFTP\\monkeyLog',today)
        packagename = apkinfo['package']
        print("******************************")

        self.device = device

        if not os.path.exists(self.test_report_root):
            os.mkdir(self.test_report_root)

        #带包包的路径
        self.test_report_path = os.path.join(self.test_report_root,packagename)
        # self.test_report_path = os.path.join(self.test_report_root, self.device['model'].replace(':', '_').replace(' ', '')+'_'+self.device['serial'])

        if not os.path.exists(self.test_report_path):
            os.mkdir(self.test_report_path)

    def get_path(self):
        return self.test_report_path

    def get_device(self):
        return self.device

    def run_cases(self, cases):
        runner = unittest.TextTestRunner()
        runner.run(cases)




