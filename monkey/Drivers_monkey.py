#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/1/24 14:05
# @Author  : qingping.niu
# @File    : Drivers_monkey.py
# @desc    :
import time,os

from Utils.Devices_new import *
from PageObject.BasePage import BasePage
from monkey.monkey import Monkey
from Public.adbCommand import get_pid,kill_process

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

        d = base_page.get_driver()

        serial = run.get_device()['serial']
        model = run.get_device()['model']


        # cmd = cmd%(serial)
        # print('run monkey command:%s' % cmd)

        # d.shell(cmd)

        base_page.set_original_ime()
        base_page.identify()

        DriversMonkey.startMonkey(serial,model,cmd,d)

    @staticmethod
    def startMonkey(serial,model,cmd,cls):
        # 日志存放路径
        log_dir = 'F:\\mibctestFTP\\monkeyLog'
        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        full_path = os.path.join(log_dir, today)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        #组装文件及运行命令
        timeFile = time.strftime('%H%M%S', time.localtime(time.time()))
        monkeyLogFile = full_path + os.path.sep + model+'_Monkey_' + timeFile + '.txt'

        cmd = cmd % (serial)+'>'+monkeyLogFile
        print('run monkey command:%s' % cmd)
        subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        logcatLogFile = full_path + os.path.sep + model+'_Logcat_' + timeFile + '.txt'


        logcmd = "adb -s %s logcat -c && adb -s %s logcat -v time *:E >%s"%(serial,serial,logcatLogFile)
        print('logcat command:%s'%logcmd)
        subprocess.Popen(logcmd,shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        output, exit_code = cls.shell(["ps", "|grep", "logcat"])
        print("****"+output)
        pid = output.split()[1]
        print('----logcat pid=%s' % pid)

        # pid = get_pid(serial,'logcat')

        while True:
            time.sleep(30)
            try:
                m_session = cls.session('com.android.commands.monkey', attach=True)
                print(m_session._pid)
                if m_session._pid:
                    continue
                else:
                    break
            except:
                kill_process(serial, pid)
                break
        print("---------monkey finished and logcat process kill----------")


    def run(self,method=None,ip=None,command=None):
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
            pool.apply_async(self._run_monkey,args=(run,command,))

        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')
