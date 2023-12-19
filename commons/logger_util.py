#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/5/18 15:01
# @Author :天草柑橘
# @File : logger_util.py.py
# @Software: PyCharm
import logging
import time
from builtins import int, str, Exception

from commons.yaml_util import get_object_path, read_config_yaml


class LoggerUtil:
    def create_log(self, logger_name='log'):
        # 创建一个日志对象
        self.logger = logging.getLogger(logger_name)
        # 设置全局的日志级别（从低到高：debug<info<warning<error<critical）
        self.logger.setLevel(logging.DEBUG)

        if not self.logger.handlers:
            # -------文件日志----------
            # 1.创建文件日志路径
            self.file_log_path = get_object_path() + "/logs/" + read_config_yaml("log", "log_name") + str(
                int(time.time())) + ".log"
            # 2.创建文件日志的控制器
            self.file_hander = logging.FileHandler(self.file_log_path, encoding='utf-8')
            # 3.创建文件日志的日志级别
            file_log_level = str(read_config_yaml("log", "log_level")).lower()
            if file_log_level == "debug":
                self.file_hander.setLevel(logging.DEBUG)
            elif file_log_level == "info":
                self.file_hander.setLevel(logging.INFO)
            elif file_log_level == "warning":
                self.file_hander.setLevel(logging.WARNING)
            elif file_log_level == "error":
                self.file_hander.setLevel(logging.ERROR)
            elif file_log_level == "critical":
                self.file_hander.setLevel(logging.CRITICAL)
            else:
                self.file_hander.setLevel(logging.DEBUG)
            # 4.创建文件日志格式
            self.file_hander.setFormatter(logging.Formatter(read_config_yaml("log", "log_format")))
            # 将文件日志的控制器加入到日志对象
            self.logger.addHandler(self.file_hander)
            # -------控制台日志----------
            # 1.创建控制台日志的控制器
            self.console_hander = logging.StreamHandler()
            # 2.创建控制台日志的日志级别
            console_log_level = str(read_config_yaml("log", "log_level")).lower()
            if console_log_level == "debug":
                self.console_hander.setLevel(logging.DEBUG)
            elif console_log_level == "info":
                self.console_hander.setLevel(logging.INFO)
            elif console_log_level == "warning":
                self.console_hander.setLevel(logging.WARNING)
            elif console_log_level == "error":
                self.console_hander.setLevel(logging.ERROR)
            elif console_log_level == "critical":
                self.console_hander.setLevel(logging.CRITICAL)
            else:
                self.console_hander.setLevel(logging.DEBUG)
            # 3.创建控制台日志格式
            self.console_hander.setFormatter(logging.Formatter(read_config_yaml("log", "log_format")))
            # 将控制台日志的控制器加入到日志对象
            self.logger.addHandler(self.console_hander)

        #返回包含有文件日志控制器和控制台控制器的日志对象
        return self.logger


#错误日志的输出
def error_log(message):
    LoggerUtil().create_log().error(message)
    raise Exception(message)


#信息日志的输出
def logs(message):
    LoggerUtil().create_log().info(message)