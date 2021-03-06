#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 10:05
# @Author  : qingping.niu
# @File    : Devices_new.py
# @desc    :
'''
多进程check_alive
Mac下需要配置  `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`到环境变量，不然python会挂掉
'''
import re
import subprocess
from multiprocessing import Pool

import uiautomator2 as u2

from Config.ReadConfig import ReadConfig
from Utils import ATX_Server


def get_devices(test_ip):
    '''get the devices from Pubilc/Config.ini devices list
    return alive devices'''
    # devices_ip = ReadConfig().get_devices_ip()  #从文件读取
    devices_ip = test_ip #传入ip
    print('Start check devices from Config devices IP list: %s' % devices_ip)
    pool = Pool(processes=len(devices_ip))
    tmp_list = []
    for run in devices_ip:
        tmp_list.append(pool.apply_async(check_alive, args=(run,)))
    pool.close()
    pool.join()
    devices_list = []
    for i in tmp_list:
        if i.get():
            devices_list.append(i.get())
    return devices_list


def get_online_devices():
    '''get the devices from ATX-Server
    return alive devices'''
    devices = ATX_Server(ReadConfig().get_server_url()).online_devices()
    print('Start check %s  devices on ATX-Server' % len(devices))
    if devices:
        pool = Pool(processes=len(devices))
        tmp_list = []
        for run in devices:
            tmp_list.append(pool.apply_async(check_alive, args=(run,)))
        pool.close()
        pool.join()
        devices_list = []
        for i in tmp_list:
            if i.get():
                devices_list.append(i.get())
        return devices_list
    else:
        raise Exception('ATX-Server has no online device!!! ')


def connect_devices():
    '''get the devices USB connected on PC
    return alive devices'''
    output = subprocess.check_output(['adb', 'devices'])
    pattern = re.compile(
        r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    matches = pattern.findall(output.decode())
    valid_serials = [m[0] for m in matches if m[1] == 'device']

    if valid_serials:
        print('Start check %s devices connected on PC: ' % len(valid_serials))
        pool = Pool(processes=len(valid_serials))
        tmp_list = []
        for run in valid_serials:
            tmp_list.append(pool.apply_async(check_alive, args=(run,)))
        pool.close()
        pool.join()
        devices_list = []
        for i in tmp_list:
            if i.get():
                devices_list.append(i.get())
        return devices_list
    if len(valid_serials) == 0:
        print("No available android devices detected.")
        return []

def connect_devices_input(serialsList):
    '''get the devices USB connected on PC
    return alive devices'''
    # output = subprocess.check_output(['adb', 'devices'])
    # pattern = re.compile(
    #     r'(?P<serial>[^\s]+)\t(?P<status>device|offline)')
    # matches = pattern.findall(output.decode())
    valid_serials = serialsList

    if valid_serials:
        print('Start check %s devices connected on PC: ' % len(valid_serials))
        pool = Pool(processes=len(valid_serials))
        tmp_list = []
        for run in valid_serials:
            tmp_list.append(pool.apply_async(check_alive, args=(run,)))
        pool.close()
        pool.join()
        devices_list = []
        for i in tmp_list:
            if i.get():
                devices_list.append(i.get())
        return devices_list
    if len(valid_serials) == 0:
        print("No available android devices detected.")
        return []


def check_alive(device):
    if isinstance(device, dict):
        d = u2.connect(device['ip'])
        if d.agent_alive:
            d.healthcheck()
            if d.alive:
                print('%s is alive' % device['udid'])
                dict_tmp = d.device_info
                dict_tmp['ip'] = device['ip']
                return dict_tmp
            else:
                print('%s is not alive' % device['udid'])
                return None
        else:
            print('The device atx_agent %s  is not alive,please checkout!' % device['udid'])
            return None
    else:
        print('device===%s'%device)
        d = u2.connect(device)
        print('model----%s'%d.device_info['model'])
        if d.agent_alive:
            print('-----------------')
            d.healthcheck()
            if d.alive:
                if re.match(r"(\d+\.\d+\.\d+\.\d)", device):
                    dict_tmp = d.device_info
                    dict_tmp['ip'] = device
                    print('%s is alive' % device)
                else:
                    dict_tmp = d.device_info
                return dict_tmp
            else:
                print('%s is not alive' % device)
                return None
        else:
            print('The device atx_agent %s  is not alive,please checkout!' % device)
            return None





# if __name__ == '__main__':
    # devices_ip = get_devices()

    # devices = connect_devices()
    # devices = get_online_devices()
    # print(devices_ip)
    #
    # pool = Pool(processes=len(devices_ip))
    # tmp_list = []
    # for run in devices_ip:
    #     tmp_list.append(pool.apply_async(check_alive, args=(run,)))
    #     # alive_list.append(tmp)
    # pool.close()
    # pool.join()
    # print('All runs done........ ')
    # print(tmp_list)
    # for i in tmp_list:
    #     print(i.get())
    # print(get_devices())
    # print(get_online_devices())
    # print(connect_devices())