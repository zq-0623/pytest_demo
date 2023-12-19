import os
import time

import pytest

from commons.yaml_util import read_extract_yaml

if __name__ == '__main__':
    pytest.main()
    times=time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
    os.system("allure generate ./temps -o ./reports/reports_"+times+" --clean")