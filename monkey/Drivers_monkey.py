#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 14:05
# @Author  : qingping.niu
# @File    : Drivers_monkey.py
# @desc    :

from Utils.Devices_new import *
from PageObject.BasePage import BasePage
from monkey.monkey import Monkey

class DriversMonkey(object):

    @staticmethod
    def _run_monkey(run,cmd):
        base_page = BasePage()
        base_page.set_driver(run.get_device()['serial'])
        # if 'ip' in run.get_device():
        #     base_page.set_driver(run.get_device()['ip'])
        # else:
        #     base_page.set_driver(run.get_device()['serial'])

        base_page.set_fastinput_ime()

        # d = base_page.get_driver()

        serial = run.get_device()['serial']


        cmd = cmd%(serial)
        print('run monkey command:%s' % cmd)

        # d.shell(cmd)

        base_page.set_original_ime()
        base_page.identify()
        subprocess.getoutput(cmd)

    @staticmethod
    def checkMonkeySession(res):
        print("callback==="+res)
        # cls = base_page.get_driver()
        #
        # cls.session("com.android.commands.monkey", attach=True)



    def run(self,method='USB',ip=None,command=None):
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
            if len(ip) > 0:
                # get  devices connected PC with USB
                print('Checking available USB devices connected on PC... ')
                devices = connect_devices_input(ip)
            else:
                # get  devices connected PC with USB
                print('Checking available USB devices connected on PC... ')
                devices = connect_devices()
            print('\nThere has %s  USB devices alive ' % len(devices))

        else:
            raise Exception('Config.ini method illegal:method =%s' % method)

        if not devices:
            print('There is no device found,test over.')
            return

        runs = []
        for i in range(len(devices)):
            runs.append(Monkey(devices[i]))

        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_monkey,args=(run,command,),callback=self.checkMonkeySession)

        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')
