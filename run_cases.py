#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 16:28
# @Author  : qingping.niu
# @File    : run_cases.py
# @desc    :

import sys,argparse
sys.path.append('.')
from Utils.CaseStrategy import CaseStrategy
from Utils.Drivers import Drivers

if __name__ == '__main__':
    # back up old report dir 备份旧的测试报告文件夹到TestReport_backup下
    # backup_report()
    #获取jenkins传IP参数
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ip", required=True, help="ip")
    args = vars(ap.parse_args())
    test_ip = args['ip']

    cs = CaseStrategy()
    cases = cs.collect_cases(suite=True)
    Drivers().run(cases,[test_ip])

    # Generate zip_report file  压缩测试报告文件
    # zip_report()


