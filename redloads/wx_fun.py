#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/5/17 16:02
# @Author :天草柑橘
# @File : wx_fun.py
# @Software: PyCharm
import random

import yaml

from commons.yaml_util import get_object_path


class WxFun:
    #获取随机数
    def get_randon_number(self,min,max):
        return random.randint(int(min),int(max))

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

