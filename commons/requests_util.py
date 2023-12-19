import json
import re
import traceback
import jsonpath
import requests
from commons.logger_util import error_log, logs
from commons.yaml_util import read_config_yaml, write_extract_yaml


class RequestsUtil:
    # 通过session会话去关联。session默认的情况下回自动的关联cookie
    session = requests.session()

    def __init__(self, obj):
        self.obj = obj

    # 规范YAML测试用例
    def standard_yaml(self, caseinfo):
        try:
            caseinfo_key = caseinfo.keys()
            # 判断一级关键字是否包括有：base_url,name,request,valiedate
            if "name" in caseinfo_key and "base_url" in caseinfo_key and "request" in caseinfo_key and "validate" in caseinfo_key:
                # 判断request下面是否包含：method,url
                request_keys = caseinfo['request'].keys()
                if "method" in request_keys and "url" in request_keys:
                    print("YAML基本架构检查通过")
                    # pop() 方法删除字典给定键 key 及对应的值
                    name = caseinfo.pop("name")
                    base_url = caseinfo.pop("base_url")
                    method = caseinfo['request'].pop("method")
                    url = caseinfo['request'].pop("url")
                    # 发送请求
                    res = self.send_request(name,method, base_url + url, **caseinfo['request'])
                    result_text = res.text
                    result_code = res.status_code
                    result_json = ""
                    try:
                        result_json = res.json()
                    except Exception as e:
                        print("extract返回的结果不是JSON格式,不能使用jsonpath提取")
                    # 提取值并且写入extarct.yaml文件
                    if "extract" in caseinfo.keys():
                        for key, value in caseinfo["extract"].items():
                            if "(.*?)" in value or "(.+?)" in value:  # 正则表达式
                                zz_value = re.search(value, result_text)
                                if zz_value:
                                    extract_value = {key: zz_value.group(1)}
                                    write_extract_yaml(extract_value)
                            else:  # jsonpath
                                js_value = jsonpath.jsonpath(result_json, value)
                                if js_value:
                                    extract_value = {key: js_value[0]}
                                    write_extract_yaml(extract_value)
                    # 断言
                    self.assert_result(caseinfo['validate'], result_json, result_code)
                else:
                    print("在request下必需包含：method,url")
            else:
                print("一级关键字必须要包含：name,request,validate")
        except Exception as e:
            error_log("规范YAML测试用例standard_yaml异常：%s" % str(traceback.format_exc()))

    # 替换值的方法
    # Qa1(替换url,params,data,jsom,headers)
    # Qa2(string,int,float,list,dict)
    def replace_value(self, data):
        if data:
            # 保存数据类型
            data_type = type(data)
            # 判断数据类型
            if isinstance(data, dict) or isinstance(data, list):
                str_data = json.dumps(data)
            else:
                str_data = str(data)
            # 替换
            for cs in range(1, str_data.count('${') + 1):
                if "${" in str_data and "}" in str_data:
                    start_index = str_data.index("${")
                    end_index = str_data.index("}", start_index)
                    old_value = str_data[start_index:end_index + 1]
                    # 反射：通过字类的对象和方法符串调用方法
                    func_name = old_value[2:old_value.index('(')]
                    args_value1 = old_value[old_value.index('(') + 1:old_value.index(')')]
                    if args_value1 != "":
                        if "," in args_value1:
                            args_value2 = args_value1.split(',')
                            new_value = getattr(self.obj, func_name)(*args_value2)
                            print(new_value)
                        else:
                            print("func_name", func_name)
                            new_value = getattr(self.obj, func_name)(args_value1)
                    else:
                        new_value = getattr(self.obj, func_name)
                    # 数字类型去掉“”
                    if isinstance(new_value, int) or isinstance(new_value, float):
                        str_data = str_data.replace('"' + old_value + '"', str(new_value))
                    else:
                        str_data = str_data.replace(old_value, str(new_value))
            # 还原数据类型
            if isinstance(data, dict) or isinstance(data, list):
                data = json.loads(str_data)
            else:
                data = data_type(str_data)
        return data

    # 统一请求封装
    def send_request(self, name, method, url, **kwargs):
        try:
            logs("--------接口测试开始--------")
            # 基础路径拼接
            url = self.replace_value(url)
            # 请求头和参数替换
            for key, value in kwargs.items():
                if key in ['params', 'data', 'json', 'headers']:
                    kwargs[key] = self.replace_value(value)
                    print(kwargs[key])
                elif key == "files":
                    for file_key, file_path in value.items():
                        value[file_key] = open(file_path, 'rb')
            # 输入信息日志
            logs("请求名称：%s" % name)
            logs("请求方式：%s" % method)
            logs("请求路径：%s" % url)
            if "headers" in kwargs.keys():
                logs("请求头：%s" % kwargs["headers"])
            if "params" in kwargs.keys():
                logs("请求params参数：%s" % kwargs["params"])
            elif "data" in kwargs.keys():
                logs("请求data参数：%s" % kwargs["data"])
            elif "json" in kwargs.keys():
                logs("请求json参数：%s" % kwargs["json"])
            if "files" in kwargs.keys():
                logs("请求files参数：%s" % kwargs["files"])
            # 请求
            rep = RequestsUtil.session.request(method, url, **kwargs)
            return rep
        except Exception as e:
            error_log("发送请求send_request异常：%s" % str(traceback.format_exc()))

    def assert_result(self, yq_result, sj_result, result_code):
        try:
            logs("预期结果：%s" % yq_result)
            logs("实际结果：%s" % json.loads(json.dumps(sj_result).replace(r"\\","\\")))
            all_flag = 0
            for yq in yq_result:
                for key, value in yq.items():
                    if key == "equals":
                        flag = self.equals_assert(value, sj_result, result_code)
                        all_flag = all_flag + flag
                    elif key == "contains":
                        flag = self.contains_assert(value, sj_result)
                        all_flag = all_flag + flag
                    elif key == "greater_than":
                        flag = self.greater_than_assert(value, sj_result)
                        all_flag = all_flag + flag
                    else:
                        print("框架暂不支持此断言方式")
            assert all_flag == 0
            logs("接口测试成功")
            logs("--------接口测试结束--------\n")
        except Exception as e:
            logs("接口测试失败")
            logs("--------接口测试结束--------\n")
            error_log("断言assert_result异常：%s" % str(traceback.format_exc()))

    # 相等断言
    def equals_assert(self, value, sj_restul, result_code):
        flag = 0
        for assert_key, assert_value in value.items():
            if assert_key == "status_code":
                if assert_value != result_code:
                    flag = flag + 1
                    print("断言失败：返回的状态码不等于%s" % assert_value)
            else:
                lists = jsonpath.jsonpath(sj_restul, '$..%s' % assert_key)
                if lists:
                    if assert_value not in lists:
                        flag = flag + 1
                        print("断言失败" + assert_key + "不等于" + str(assert_value))
                    else:
                        flag = flag + 1
                        print("断言失败:返回的结果中不存在:" + assert_key)
            return flag

    # 包含断言
    def contains_assert(self, value, sj_result):
        flag = 0
        if str(value) not in str(sj_result):
            flag = flag + 1
            print("断言失败:返回的结果中不包含：" + value)
        return flag

    # 大于断言
    def greater_than_assert(self, value, sj_result):
        flag = 0
        (assert_key, assert_value), = value.items()
        sj_value = (jsonpath.jsonpath(sj_result, '$..%s' % assert_key))[0]
        if assert_value >= sj_value:
            flag = flag + 1
            print("大于断言失败")
        return flag
