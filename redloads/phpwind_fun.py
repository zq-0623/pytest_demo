#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/6/2 14:34
# @Author :天草柑橘
# @File : phpwind_fun.py
# @Software: PyCharm
import random

import yaml

from commons.yaml_util import get_object_path


class PhpwindFun:
    # 读取extract.yaml文件
    def read_extract_yaml(self,key):
        with open(get_object_path() + "/extract.yaml", 'r', encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[key]

    # 读取config.yaml文件
    def read_config_yaml(self, one_nodo, two_node):
        with open(get_object_path() + "/config.yaml", 'r', encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[one_nodo][two_node]