import requests
from app.datas.data_reader.txt_reader import get_txt_data

# 本来要ip代理，这是处理ip的文件
def remove_invalid_proxies(filepath, invalid_proxies):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    with open(filepath, 'w') as file:
        for line in lines:
            if line.strip() not in invalid_proxies:
                file.write(line)

def test_proxy(proxy):
    proxy_dict = {
        "https": "https://" + proxy
    }
    try:
        response = requests.get('http://baidu.com', timeout=5, proxies=proxy_dict)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

if __name__ == "__main__":
    proxy_file = '../datas/ip.txt'
    proxys = get_txt_data(proxy_file)
    invalid_proxies = []
    for proxy in proxys:
        print(proxy)
        if test_proxy(proxy):
            print("行!")
        else:
            print("不行!")
            invalid_proxies.append(proxy)

    if invalid_proxies:
        remove_invalid_proxies(proxy_file, invalid_proxies)
        print("不可用的代理已从文件中删除。")
