import logging
import random
import time
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from app.datas.data_reader.json_reader import get_json_data
from app.datas.data_writer.set_json_data import set_json_data
from app.spiders import init_my_browser

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_detail(browser, xpath, url):
    # 定义从指定URL获取数据的函数
    browser.get(url)
    details = []  # 初始化存储详细数据的列表
    try:
        # 设置显式等待，等待指定XPath的元素出现
        wait = WebDriverWait(browser, 10)  # 设置10秒的超时时间
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        # 使用XPath找到包含所需数据的所有div元素
        cultural_divs = browser.find_elements(By.XPATH, xpath)
        for cultural_div in cultural_divs:
            # 提取四个属性数据
            name = cultural_div.get_attribute('cultural-name')
            number = cultural_div.get_attribute('cultural-number')
            category = cultural_div.get_attribute('cultural-category')
            dynasty = cultural_div.get_attribute('cultural-dynasty')
            # 获取URL中的category参数
            parsed_url = urlparse(url)
            category_id = parse_qs(parsed_url.query).get('category', [None])[0]
            details.append({
                'id': category_id,
                'name': name,
                'code': number,
                'category': category,
                'dynasty': dynasty
            })

            # 添加随机间隔时间，以模拟真实用户行为
            time.sleep(random.uniform(2, 5))
        return details
    except TimeoutException:
        logging.error("显式等待超时，未找到指定元素")
    except Exception as e:
        logging.error(f"可惜 {e}")
        return None

def main():
    data = get_json_data('../datas/treasure.json')
    my_browser = init_my_browser()  # 初始化浏览器
    treasure_data = []  # 初始化存储爬取数据的列表
    try:
        for item in data:
            link = item.get('link')  # 获得我需要爬取的每个url
            if link:
                # 暂时只拿到div标签及其属性即可
                xpath = '//div[@class="table"]'
                extracted_data = get_detail(my_browser, xpath, link)
                if extracted_data:
                    treasure_data.extend(extracted_data)  # 使用extend而不是append
                    logging.info(f"从 {link} 提取到数据")
                else:
                    logging.warning(f"从 {link} 未提取到数据")
                # 添加访问下一个页面随机间隔时间
                time.sleep(random.uniform(20,25 ))
    except Exception as e:
        logging.error(f"可惜， {e}")
    finally:
        my_browser.quit()  # 关闭浏览器

    # 将爬取的数据写入treasure_details.json文件
    output_file = '../datas/treasure_details.json'
    set_json_data(output_file, treasure_data)

if __name__ == '__main__':
    main()
