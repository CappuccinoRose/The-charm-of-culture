import pandas as pd
import requests
import time
import random
from fake_useragent import UserAgent
import logging

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 请求头
def generate_headers():
    # 生成随机请求头
    ua = UserAgent()
    return {
        'User-Agent': ua.random,
        'Referer': f'https://www.ihchina.cn/project.html?tid=1'
    }

# 定义获取数据的函数
def get_ajax_data(page, province='', rx_time='', type='', cate='', keywords='', category_id='16', limit='10'):
    params = {
        'province': province,
        'rx_time': rx_time,
        'type': type,
        'cate': cate,
        'keywords': keywords,
        'category_id': category_id,
        'limit': limit,
        'p': page,  # 页数
    }
    url = "https://www.ihchina.cn/getProject.html"
    headers = generate_headers()
    response = requests.get(url, params=params, headers=headers)
    return response.json() if response.status_code == 200 else None

# 按照源代码设置的文字格式存储对象
def extract_data(index,item):
    """提取数据并返回字典"""
    return {
        'index': index,
        'project_index': item.get('auto_id', ''),
        'code': item.get('num', ''),
        'name': item.get('title', ''),
        'type': item.get('type', ''),
        'time': item.get('rx_time', '').replace('</br>',''),
        'category': item.get('cate', ''),
        'province': item.get('province', ''),
        'protect_unit': item.get('protect_unit', ''),
    }

def main():
    data = []
    page = 1
    index = 0
    while True:
        json_data = get_ajax_data(page=page)
        if json_data and 'list' in json_data:
            for item in json_data['list']:
                # 打印看看数据
                print(item)
                index += 1
                data.append(extract_data(index,item))
            time.sleep(random.uniform(2, 5))  # 添加随机延迟时间
                # 页码不增加
        else:
            break  # 没有更多数据，退出循环
    df = pd.DataFrame(data)
    print(df)
    df.to_json(f'../datas/heritage_details.json', orient='records', force_ascii=False, indent=4)

if __name__ == "__main__":
    main()
