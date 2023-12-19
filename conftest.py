#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/4/19 11:37
# @Author :天草柑橘
# @File : conftest.py
# @Software: PyCharm
import pytest
from commons.yaml_util import clear_extract_yaml


@pytest.fixture(scope="session", autouse=True)
def clear_yaml():
    clear_extract_yaml()
