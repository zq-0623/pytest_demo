import json
from builtins import isinstance, range, len, int, float, open, dict
import yaml

# 读取测试用例yaml文件
from commons.yaml_util import get_object_path, read_data_yaml


def read_testcase_yaml(yaml_path):
    with open(get_object_path() + yaml_path, 'r', encoding='utf-8') as f:
        caseinfo = yaml.load(stream=f, Loader=yaml.FullLoader)
        #单纯复制修改参数的模式
        if len(caseinfo) >= 2:
            return caseinfo
        else:  # 有数据驱动的场合
            if "parameterize" in dict(*caseinfo).keys():
                new_caseinfo = ddt(*caseinfo)
                return new_caseinfo
            else:
                return caseinfo


def ddt(caseinfo):
    if "parameterize" in caseinfo.keys():
        caseinfo_str = json.dumps(caseinfo)
        for param_key, param_value in caseinfo["parameterize"].items():
            key_list = param_key.split("-")
            print("------key和value------")
            print(key_list,param_value)
            length_flag = True
            print("------data数据列表------")
            #规范yaml数据文件的写法
            data_list = read_data_yaml(param_value)
            for data in data_list:
                print(data)
                if len(data) != len(key_list):
                    length_flag = False
                    break
            # 替换值
            print("------替换值------")
            new_caseinfo = []
            if length_flag:
                for x in range(1, len(data_list)):  # 循环数据的行数
                    temp_caseinfo = caseinfo_str
                    for y in range(0, len(data_list[x])):  # 循环数据列
                        if data_list[0][y] in key_list:
                            # 替换原始的yaml里面的$ddt{}
                            # 数字类型去掉“”
                            if isinstance(data_list[x][y], int) or isinstance(data_list[x][y], float):
                                temp_caseinfo = temp_caseinfo.replace('"$ddt{'+data_list[0][y]+'}"',str(data_list[x][y]))
                            else:
                                temp_caseinfo = temp_caseinfo.replace("$ddt{"+data_list[0][y]+"}", str(data_list[x][y]))
                    print(temp_caseinfo)

                    new_caseinfo.append(json.loads(temp_caseinfo))
            return new_caseinfo
    else:
        return caseinfo
