#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/21 11:05
# @Author  : qingping.niu
# @File    : Drivers.py
# @desc    :

# from Public.Devices import *    # for循环 check_alive  比较慢
import os
import time

from PageObject.BasePage import BasePage
from Utils.Devices_new import *    # 多进程 check_alive ，Mac下需要配置  `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`到环境变量
from Utils.Log import Log
from Utils.Report import create_statistics_report,backup_report
from Utils.ReportPath import ReportPath
from Utils.RunCases import RunCases
from monkey.RunMaxim import RunMaxim
from Public.adbCommand import get_pid,kill_process
from Utils.MonkeyLogAnalyze import MonkeyLog


def check_devives(method='USB',devices_input=None):
    # 根据devices_input 获取android设备
    # method = ReadConfig().get_method().strip()
    if method == 'SERVER':
        # get ATX-Server Online devices
        # devices = ATX_Server(ReadConfig().get_server_url()).online_devices()
        print('Checking available online devices from ATX-Server...')
        devices = get_online_devices()
        print('\nThere has %s online devices in ATX-Server' % len(devices))
    elif method == 'IP':
        # get  devices from config devices list
        print('Checking available IP devices from config... ')
        devices = get_devices()
        print('\nThere has %s  devices alive in config IP list' % len(devices))
    elif method == 'USB':
        # get  devices connected PC with USB

        if len(devices_input) > 0:
            print('Console input devices....')
            print("****"+devices_input)
            devices = connect_devices_input(devices_input)

        else:
            print('Checking available USB devices connected on PC... ')
            devices = connect_devices()

        print('\nThere has %s  USB devices alive ' % len(devices))

    else:
        raise Exception('Config.ini method illegal:method =%s' % method)

    return devices



class Drivers:
    @staticmethod
    def _run_cases(run, cases):

        log = Log()
        log.set_logger(run.get_device()['model'], run.get_path() + '/' + 'client.log')
        log.i('udid: %s', run.get_device()['udid'])

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:
            # run cases
            base_page.set_fastinput_ime()

            run.run(cases)

            base_page.set_original_ime()
            base_page.identify()
        except AssertionError as e:
            log.e('AssertionError, %s', e)

    def run(self, cases,test_ip):
        # 根据method 获取android设备
        method = ReadConfig().get_method().strip()
        if method == 'SERVER':
            # get ATX-Server Online devices
            # devices = ATX_Server(ReadConfig().get_server_url()).online_devices()
            print('Checking available online devices from ATX-Server...')
            devices = get_online_devices()
            print('\nThere has %s online devices in ATX-Server' % len(devices))
        elif method == 'IP':
            # get  devices from config devices list
            print('Checking available IP devices from config... ')
            devices = get_devices(test_ip)
            print('\nThere has %s  devices alive in config IP list' % len(devices))
        elif method == 'USB':
            # get  devices connected PC with USB
            print('Checking available USB devices connected on PC... ')
            devices = connect_devices()
            print('\nThere has %s  USB devices alive ' % len(devices))

        else:
            raise Exception('Config.ini method illegal:method =%s' % method)

        if not devices:
            print('There is no device found,test over.')
            return

        # generate test data data.json 准备测试数据
        # generate_test_data(devices)

        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        runs = []
        for i in range(len(devices)):
            runs.append(RunCases(devices[i]))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_cases,
                             args=(run, cases,))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')
        # ChromeDriver.kill()

        #  Generate statistics report  生成统计测试报告 将所有设备的报告在一个HTML中展示
        create_statistics_report(runs)

    @staticmethod
    def _run_maxim(run, cases, command, actions, widget_black, apkinfo):
        log = Log()
        log.set_logger(run.get_device()['model'], os.path.join(run.get_path(), 'client.log'))
        log.i('udid: %s', run.get_device()['udid'])

        #取出包名和版本信息
        packagename = apkinfo['package']
        versionname = apkinfo['versionName']

        log.i('packagename: %s, versionname: %s',packagename,versionname)

        # set cls.path, it must be call before operate on any page
        path = ReportPath()
        path.set_path(run.get_path())

        # set cls.driver, it must be call before operate on any page
        base_page = BasePage()
        if 'ip' in run.get_device():
            base_page.set_driver(run.get_device()['ip'])
        else:
            base_page.set_driver(run.get_device()['serial'])

        try:

            #创建日志存储路径
            model = run.get_device()['model']
            serial = run.get_device()['serial']
            currentTime = time.strftime('%H%M%S', time.localtime(time.time()))
            monkeyFile = run.get_path() + os.path.sep + model + '_Monkey_' + versionname+'_'+currentTime+'.txt'
            logcatFile = run.get_path() + os.path.sep + model + '_Logcat_' + versionname+'_'+currentTime+'.txt'

            # run cases
            base_page.d.shell('logcat -c')  # 清空logcat
            if cases:
                run.run_cases(cases)


            #格式化monkey命令
            # command = command+ '>/sdcard/monkeyLog 2>&1'
            command = command % (serial) + '>' + monkeyFile + ' 2>&1'
            log.i('monkey_command: %s',command)
            #执行monkey命令
            subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # base_page.d.shell(command)
            #执行logcat命令
            logcmd = "adb -s %s logcat -v time *:E >%s" % (serial, logcatFile)
            subprocess.Popen(logcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # # base_page.d.shell(logcmd)
            # #
            time.sleep(5)

            output, exit_code = base_page.d.shell(["ps", "|grep", "logcat"])
            #
            log.i('logcat pid: %s',output)
            pid = output.split()[1]

            while True:
                time.sleep(30)
                try:
                    m_session = base_page.d.session('com.android.commands.monkey', attach=True)
                    if m_session._pid:
                        continue
                    else:
                        break
                except:
                    kill_process(serial, pid)
                    break
            log.i('**** monkey finished and logcat process kill sucess ****')

            # base_page.d.app_start('jp.mmasashi.turnWiFiOnAndEnjoyYouTube')
            # log.i('start ATX services sucess')

            # print(run.get_path())
            # base_page.d.pull('/data/anr/',run.get_path()+"\\")
            # base_page.d.shell('adb pull /data/anr %s '%run.get_path())

            anrPath = os.path.join(run.get_path(),model)

            log.i('anrpath==%s '%anrPath)


            if not os.path.exists(anrPath):
                os.mkdir(anrPath)


            anrCmd = 'adb -s %s pull /data/anr %s' %(serial,anrPath)
            subprocess.Popen(anrCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log.i('pull /data/anr logs success')

            # 跑完monkey分析日志
            crashLogPath = os.path.join(run.get_path(),'Crash')

            MonkeyLog.crash_analyze(monkeyFile, crashLogPath,model,versionname,currentTime)
            # MonkeyLog.logcat_analyze(logcatFile, crashLogPath,model,versionname,currentTime)



            # Maxim().run_monkey(monkey_shell=command, actions=actions, widget_black=widget_black)
            #
            # base_page.d.shell('logcat -d > /sdcard/logcat.log')
            # time.sleep(1)
            # base_page.d.pull('/sdcard/logcat.log', os.path.join(path.get_path(), 'logcat.log'))
            # base_page.d.pull('/sdcard/monkeyerr.txt', os.path.join(path.get_path(), 'monkeyerr.txt'))
            # base_page.d.pull('/sdcard/monkeyout.txt', os.path.join(path.get_path(), 'monkeyout.txt'))

            base_page.set_original_ime()
            base_page.identify()


        except AssertionError as e:
            log.e('AssertionError, %s', e)


    def run_maxim(self,cases=None,devices_input=None,command=None,apkinfo=None,actions=None,widget_black=False):
        # start_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

        devices = check_devives(devices_input=devices_input)

        if not devices:
            print('There is no device found,test over.')
            return
        print('Starting Run test >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        runs = []
        for i in range(len(devices)):
            runs.append(RunMaxim(device=devices[i],apkinfo=apkinfo))

        # run on every device 开始执行测试
        pool = Pool(processes=len(runs))
        for run in runs:
            pool.apply_async(self._run_maxim,
                             args=(run, cases, command, actions, widget_black,apkinfo,))
        print('Waiting for all runs done........ ')
        pool.close()
        pool.join()
        print('All runs done........ ')
        # backup_report('./MaximReport', './MaximReport_History', start_time)






# if __name__ == '__main__':
    # print(ATX_Server(ReadConfig().get_url()).online_devices())
    #
    # print(get_devices())
    # print(ReadConfig().get_atx_server('method'))
