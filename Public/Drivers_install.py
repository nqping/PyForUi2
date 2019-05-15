#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/11 15:48
# @Author  : qingping.niu
# @File    : Drivers_install.py
# @desc    :

import os,time
from Utils.Devices_new import *
from Utils.Log import Log
from monkey.monkey import Monkey
from PageObject.BasePage import BasePage
import apkutils


class DriversInstall(object):
    @staticmethod
    def _install_app(run, apkPath):
        log = Log()

        # apk_info = get_apk_info(apkPath)
        base_page = BasePage()
        device = run.get_device()

        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        base_page.set_fastinput_ime()

        d = base_page.get_driver()
        #安装应用
        file_name = os.path.basename(apkPath)
        dst = '/sdcard/' + file_name
        print('start push apk.......')
        d.push(apkPath, dst)
        print('start install apk ............')
        d.shell(['pm', 'install', '-r', dst],stream=True)
        # d.shell(['rm', dst])
        # time.sleep(60)

        base_page.set_original_ime()
        base_page.identify()
        time.sleep(45)
        print('delete apk ...............')
        d.shell(['rm', dst])

    # @staticmethod
    # def get_apk_info(apkpath):
    #     print(apkpath)
    #     tmp = apkutils.APK(apkpath).get_manifest()
    #     info = {}
    #     info['versionCode'] = str(tmp.get('@android:versionCode'))
    #     info['versionName'] = str(tmp.get('@android:versionName'))
    #     info['package'] = str(tmp.get('@package'))
    #     print("安装包信息:%s"%info)
    #     return info

    def run(self, method=None, ip=None, apkPath=None):
        if method == 'SERVER':
            print('Checking available online devices from ATX-Server...')
            devices = get_online_devices()
            print('\nThere has %s online devices in ATX-Server' % len(devices))

        elif method == 'IP':
            # get  devices from config devices list
            print('Checking available IP devices from config... ')
            devices = get_devices(ip)
            print('\nThere has %s  devices alive in config IP list' % len(devices))
        elif method == 'USB':
            if len(ip)>0:
                #get devices connected by input
                print('Checking available USB devices connected on Input ')
                devices = connect_devices_input(ip)
            else:
                # get  devices connected PC with USB
                print('Checking available USB devices connected on PC... ')
                devices = connect_devices()
            print('\nThere has %s  USB devices alive ' % len(devices))

        else:
            raise Exception('input method illegal:method =%s' % method)

        if not devices:
            print('There is no device found,test over.')
            return

        runs = []
        for i in range(len(devices)):
            runs.append(Monkey(devices[i]))

        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._install_app, args=(run, apkPath,))

        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')