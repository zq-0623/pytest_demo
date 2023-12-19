#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/6/7 11:42
# @Author :天草柑橘
# @File : test_demo.py
# @Software: PyCharm
import allure
import pytest

from commons.parameterize_util import read_testcase_yaml
from commons.requests_util import RequestsUtil
from commons.yaml_util import read_yaml
from redloads.demo_fun import DemoFun


@allure.epic("接口自动化测试项目")  # 项目名称定制
@allure.feature('DEMO案例')  # 模块名称定制
class TestPhpwind:

    @allure.story("获取一言名句")
    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("./testcases/demo/sentences.yaml"))
    def test_sentences(self,caseinfo):
        res = RequestsUtil(DemoFun()).standard_yaml(caseinfo)
