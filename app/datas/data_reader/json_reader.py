import json

# 读取json文件
def get_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)