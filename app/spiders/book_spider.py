import logging
import time
import random
from urllib.parse import urljoin
from selenium.common import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree

from app.datas.data_writer.set_json_data import set_json_data
from app.spiders import init_my_browser

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def extract_item_data(item, base_url):
    """提取单个书籍项目的数据"""
    try:
        img_link = item.xpath('.//div[@class="pic"]/img/@src')
        title = item.xpath('.//div[@class="tt"]/text()')
        text_description = item.xpath('.//div[@class="txt"]/text()')
        permission = item.xpath('.//div[@class="txt1"]/text()')

        return {
            'src': urljoin(base_url, img_link[0]) if img_link else None,
            'title': title[0].strip() if title else "",
            'text_description': text_description[0].strip() if text_description else "",
            'permission': permission[0].strip() if permission else ""
        }
    except Exception as e:
        logger.error(f"提取单个项目数据时出错: {e}")
        return None


def get_book_data(browser, xpath, base_url):
    """从页面提取所有书籍数据"""
    try:
        html_content = browser.page_source
        tree = etree.HTML(html_content)
        items = tree.xpath(xpath + '/li')

        if not items:
            logger.warning(f"未找到匹配的书籍项目，XPath: {xpath}")
            return []

        book_data = []
        for item in items:
            data = extract_item_data(item, base_url)
            if data:
                book_data.append(data)

        # 添加随机延迟（在所有项目处理完成后）
        time.sleep(random.uniform(1, 3))
        return book_data

    except Exception as e:
        logger.error(f"解析页面时出错: {e}")
        return []


def main():
    my_browser = None
    try:
        my_browser = init_my_browser()
        if not my_browser:
            logger.error("浏览器初始化失败")
            return

        url = 'http://read.nlc.cn/thematDataSearch/toGujizt'
        logger.info(f"开始访问: {url}")
        my_browser.get(url)

        wait = WebDriverWait(my_browser, 10)
        xpath = '//div[@class="m_middle"]//ul[@class="YMH2019_New_GJZTJS_List1"]'

        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        book_data = get_book_data(my_browser, xpath, url)

        if book_data:
            output_file = '../datas/book.json'
            set_json_data(output_file, book_data)
            logger.info(f"成功提取并保存 {len(book_data)} 条书籍数据到 {output_file}")
        else:
            logger.warning("未提取到任何书籍数据")

    except TimeoutException:
        logger.error("页面加载超时，未找到指定元素")
    except WebDriverException as e:
        logger.error(f"浏览器操作出错: {e}")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
    finally:
        if my_browser:
            my_browser.quit()
            logger.info("浏览器已关闭")


if __name__ == '__main__':
    main()


