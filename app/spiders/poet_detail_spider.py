import logging
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from app.datas.data_reader.json_reader import get_json_data
from app.datas.data_writer.set_json_data import set_json_data
from app.spiders import init_my_browser

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_detail(browser, url):
    browser.get(url)
    details = {}
    max_retries = 3  # 设置最大重试次数
    retries = 0

    while retries < max_retries:# 允许寻找3次
        try:
            wait = WebDriverWait(browser, 10)
            # 作者
            author_info = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "author")))
            # 名字
            name = author_info.find_element(By.CLASS_NAME, "name").text
            # 朝代
            dynasty = author_info.find_element(By.CLASS_NAME, "dynasty").text
            # 作者简介
            description = author_info.find_element(By.CLASS_NAME, "desc").text
            # 再等等
            wait = WebDriverWait(browser, 30)
            # 作品
            works_div = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "works")))
            work_items = works_div.find_elements(By.CLASS_NAME, "work-item")
            if not work_items:
                raise ValueError("未获取到页面作品")

            works = {}
            for index, work_item in enumerate(work_items):
                title = work_item.find_element(By.CLASS_NAME, "title").text
                content = work_item.find_element(By.CLASS_NAME, "content").text
                author = work_item.find_element(By.CLASS_NAME, "author").text
                works[f'work{index + 1}'] = {'title': title, 'content': content, 'author': author}

            if not works:
                raise ValueError("哎呀呀，作品目录为空")

            details['name'] = name
            details['dynasty'] = dynasty
            details['description'] = description
            details['works'] = works

            time.sleep(random.uniform(5, 10))
            return details
        except (TimeoutException, ValueError) as e:
            logging.warning(f"尝试 {retries + 1} 次失败: {e}")
            retries += 1
            time.sleep(random.uniform(10, 15))
        except Exception as e:
            logging.error(f"可惜: {e}")
            return None

    logging.error("已经尝试三次仍然没有找到")
    return None

def main():
    data = get_json_data('../datas/poet.json')
    my_browser = init_my_browser()
    poet_data = []
    try:
        for item in data:
            link = item.get('link')
            if link:
                extracted_data = get_detail(my_browser, link)
                if extracted_data:
                    poet_data.append(extracted_data)
                    logging.info(f"数据来自{link}")
                else:
                    logging.warning(f"没有数据在 {link}")
                time.sleep(random.uniform(35, 66))
    except Exception as e:
        logging.error(f"可惜: {e}")
    finally:
        my_browser.quit()

    output_file = '../datas/poet_details.json'
    set_json_data(output_file, poet_data)

if __name__ == '__main__':
    main()

