#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2022/4/15 17:01
# @Author :天草柑橘
# @File : test_phpwind.py
# @Software: PyCharm
import re

import allure
import pytest

from commons.parameterize_util import read_testcase_yaml
from commons.requests_util import RequestsUtil
from redloads.phpwind_fun import PhpwindFun


@allure.epic("接口自动化测试项目")  # 项目名称定制
@allure.feature('phpwind论坛')  # 模块名称定制
class TestPhpwind:

    @allure.story("访问phpwind论坛首页")
    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("./testcases/phpwind/index.yaml"))
    def test_phpwind_index(self,caseinfo):
        res = RequestsUtil(PhpwindFun()).standard_yaml(caseinfo)

    @allure.story("phpwind论坛登录接口")
    @pytest.mark.parametrize("caseinfo", read_testcase_yaml("./testcases/phpwind/login.yaml"))
    def test_phpwind_login(self,caseinfo):
        res = RequestsUtil(PhpwindFun()).standard_yaml(caseinfo)
