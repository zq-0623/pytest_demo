#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/6/7 11:34
# @Author :天草柑橘
# @File : demo_fun.py.py
# @Software: PyCharm

# 读取config.yaml文件
import yaml

from commons.yaml_util import get_object_path

class DemoFun:

    def read_config_yaml(self, one_nodo, two_node):
        with open(get_object_path() + "/config.yaml", 'r', encoding='utf-8') as f:
            value = yaml.load(stream=f, Loader=yaml.FullLoader)
            return value[one_nodo][two_node]