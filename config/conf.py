import time
import os

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ui元素对象库config.ini文件所在目录
CONF_PATH = os.path.join(ROOT_DIR, 'config', 'config.ini')
# 测试数据所在目录
DATA_Path = os.path.join(ROOT_DIR, 'data', 'tcData.xlsx')
# 上传数据
upload_data = os.path.join(ROOT_DIR, 'data', '.\\Upload\\files\\test.gif')
# 当前时间
CURRENT_TIME = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time()))
# 报告目录
cur_path = os.path.dirname(os.path.realpath(__file__))
report_path = os.path.join(cur_path, f'Report\\{CURRENT_TIME}')
