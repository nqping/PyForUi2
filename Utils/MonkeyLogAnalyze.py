#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 17:00
# @Author  : qingping.niu
# @File    : MonkeyLogAnalyze.py
# @desc    : Monkey日志分析
import linecache
import os
import re
from Utils.fileUtils import write_file

keyword=['FATAL EXCEPTION','// CRASH:','ANR in']

# rsDir = os.path.join(".")
# tempPath = os.path.join('.',"temp.txt")

class MonkeyLog(object):


    @staticmethod
    def crash_analyze(logPath,carshFilePath):
        print('monkey log path:%s'+logPath)
        print('monkey log analyze file:%s'%carshFilePath)
        packagename = [] #包名

        lines_name = []
        lines_message = []
        endline_name=[]
        crashType=[]

        data = linecache.getlines(logPath)
        detail = []  # crash详情
        for row, line in enumerate(data, 1):

            if line.startswith(r'// CRASH:'):
                lines_name.append(row)
                detail.append("===========================================================\n")
                detail.append(line)
                detail.append(data[row + 1])
                detail.append(data[row + 2])
                detail.append(data[row + 3])
                detail.append(data[row + 4])
                detail.append(data[row + 5])
                packagename.append(line.split(' ')[2].replace('\n', ''))
            if line.startswith(r'// Long Msg:'):
                crashType.append(' '.join(line.split(' ')[3:]).replace('\n', ''))

            if line.startswith(r'// 	at '):
                detail.append(line)


        if len(detail) >0:
            write_file(carshFilePath,detail)

    @staticmethod
    def logcat_analyze(logPath,rsFilePath):
        '''
        分析logcat命令产生的日志
        :param logPath: logcat日志路径
        :return: pid,crashType,crashDetail
        '''
        pid=0;
        crashType=""
        crashCount=0
        crashDetail=[]

        with open(logPath,'r',encoding='utf-8') as data:
            lines = data.readlines()
            #获取总共多少个crash
            for row, line in enumerate(lines, 1):
                if line.find(keyword[0]) >0:
                    crashCount+=1
                    pid = line[line.find("(")+1 : line.find(")")]
                    print(pid)
                    line = lines[row+3]
                    crashType=line[line.find('java.lang.'):len(line)]
                    print(crashType)

            for line in lines:
                if pid in line:
                    crashDetail.append(line)

            # 将carsh日志写入文件
            if len(crashDetail) > 0 :
                write_file(rsFilePath,crashDetail)



if __name__=='__main__':


    # logcat_fata_analyze("f:\\temp\\monkeylog.txt")
    MonkeyLog.crash_analyze("F:\\mibctestFTP\\monkeyLog\\20190312\\5052D_Monkey_170206.txt",'F:\\mibctestFTP\\monkeyLog\\20190312\\monkeyCrash.txt')
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
