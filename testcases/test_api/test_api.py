import json
import random
import re
import time

import allure
import pytest
import requests

from commons.yaml_util import read_yaml


@allure.epic("接口自动化测试项目")  # 项目名称定制
@allure.feature('测试模块')  # 模块名称定制
class TestApi:

    @allure.story("天草接口")  # 接口名称定制
    @allure.title("天草打印用例")  # 所有的接口用例使用一个标题
    @allure.severity(allure.severity_level.TRIVIAL)  # 严重程度
    @allure.link("接口访问地址")
    @allure.issue("bug连接")
    @allure.testcase("测试用例连接")
    def test_01_tian_cao(self):
        allure.dynamic.description("用例描述，此接口打印天草")  # 用例描述
        print("天草")
        #步骤
        for a in range(1, 6):
            with allure.step("执行第" + str(a) + "个步骤"):
                pass
        #附件
        allure.attach(body="接口地址：XX", name="接口地址", attachment_type=allure.attachment_type.TEXT)

    @allure.story("柑橘接口")
    @allure.title("柑橘打印用例")
    @pytest.mark.parametrize("name", read_yaml("./testcases/test_api/test_02.yaml"))
    def test_02_gan_ju(self,name):
        print(name)
