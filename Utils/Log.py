#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/20 10:05
# @Author  : qingping.niu
# @File    : Log.py
# @desc    : 日志配置

import logging

class Log:
    @classmethod
    def set_logger(cls, udid, file):
        logger = logging.getLogger('ATX')
        logger.setLevel(logging.INFO)

        fh = logging.FileHandler(file)
        fh.setLevel(logging.INFO)

        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s'
                                      + ' - %s' % udid
                                      + ' - %(levelname)s'
                                      + ' - %(message)s')

        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        cls.logger = logger

    def d(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def i(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def w(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def c(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def e(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)
