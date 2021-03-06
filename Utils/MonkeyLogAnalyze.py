#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 17:00
# @Author  : qingping.niu
# @File    : MonkeyLogAnalyze.py
# @desc    : Monkey日志分析
import linecache
import os,re
from Utils.commonUtils import write_file,write_file_mkdir

keyword=['FATAL EXCEPTION','// CRASH:','ANR in','Failure starting']

# rsDir = os.path.join(".")
# tempPath = os.path.join('.',"temp.txt")

class MonkeyLog(object):


    @staticmethod
    def crash_analyze(logPath=None,crashLogPath=None,model=None,version=None,currentTime=None):

        monkeyCrash = crashLogPath + os.path.sep + model + "_monkeyCrash_" + version + "_"+ currentTime + ".txt"

        try:
            fp = open(logPath, 'r')
            data = fp.read();
            #正则表达式过滤crash日志
            crash_block = re.compile(r'^// CRASH:.*?^\//\s+^// backtrace:.*?^\//\s+^ANR in.*?\//\s$', re.MULTILINE | re.DOTALL)
            crash_detail = crash_block.findall(data)

            if len(crash_detail) > 0:
                write_file_mkdir(crashLogPath, monkeyCrash, crash_detail)
            else:
                print("******未发现CARSH**********")
        except Exception as e:
            print(e)


    @staticmethod
    def logcat_analyze(logPath,crashLogPath=None,model=None,version=None,currentTime=None):
        '''

        :param logPath: 原始日志路径
        :param crashLogPath: 分析结果路径
        :param model: 设备型号
        :param version: 应用版本
        :param currentTime: 时间戳
        :return:
        '''
        pid=0;
        crashType=""
        crashCount=0
        crashDetail=[]

        logcatCrash= crashLogPath + os.path.sep + model + "_logcatCrash_" + version + "_" + currentTime + ".txt"

        try:
            with open(logPath, 'r',encoding='utf-8') as data:
                lines = data.readlines()
                for row, line in enumerate(lines, 1):
                    if re.findall('AndroidRuntime',line):
                        crashDetail.append(line)

            # 将carsh日志写入文件
            if len(crashDetail) > 0:
                write_file_mkdir(crashLogPath, logcatCrash, crashDetail)
            else:
                print("******logcat日志未发现CARSH***********")
        except Exception as e:
            print(e)


# if __name__=='__main__':
#     pass
#
#     MonkeyLog.logcat_analyze('F:\\mibctestFTP\\monkeyLog\\5059D_RU_Logcat_v7.0.1.9.0611.1.txt',
#                    'F:\\temp\\','test','v7.0.1.9.0603.1','141')
#     # MonkeyLog.crash_analyze("F:\\mibctestFTP\\monkeyLog\\monkeylog.txt",'F:\\temp\\','5045D','201-21','1111')

    # dna = 'GTGTAATGCGAGAGAGAGAGAAGTGCTGTGTAGCTGATGCGCTAGTTTCGCGCTAGAGAGTGTAAAATTGGAGAGTGTAGTAGTGTA'
    # motif = 'GTGTA'
    # l = []
    #
    #
    # matches = re.finditer('(?=GTGTA)', dna)
    # for match in matches:
    #     loc = match.start() + 1
    #     l.append((loc, loc + len(motif) - 1))
    # print(l)
