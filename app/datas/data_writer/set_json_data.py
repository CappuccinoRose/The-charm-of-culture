import json
import logging  # 导入logging模块，用于日志记录

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 写入json文件
def set_json_data(output_file, data):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:  # 打开文件准备写入
            json.dump(data, f, ensure_ascii=False, indent=4)  # 将数据写入文件，格式化为JSON
        logging.info(f"文件 '{output_file}' 写入成功。")  # 输出提示信息
    except Exception as e:
        logging.error(f"写入文件 '{output_file}' 时发生错误：{e}")  # 如果发生错误，记录错误信息