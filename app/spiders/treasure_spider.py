from urllib.parse import urlparse, parse_qs
import logging  # 导入logging模块，用于日志记录
from selenium.webdriver.common.by import By
from urllib.parse import urljoin  # 导入urljoin用于拼接URL
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from app.datas.data_writer.set_json_data import set_json_data
from app.spiders import init_my_browser

def get_treasure_data(browser, xpath, base_url):
    treasure_data = []
    # 获取页面源代码
    html_content = browser.page_source
    # 解析HTML
    tree = etree.HTML(html_content)
    # 使用XPath找到所有匹配的<li>元素
    items = tree.xpath(xpath)
    for item in items:
        # 提取页面链接
        link = item.xpath('.//a/@href')[0]
        # 确保链接是完整的URL
        full_link = urljoin(base_url, link)
        # 提取图片链接
        treasure_link = item.xpath('.//a/img/@src')[0]
        # 提取文字描述
        text_description = ''.join(item.xpath('.//a/p/span/strong/text() | .//a/p/span/text() | .//a/p/text()')).strip()
        # 获取URL中的category参数
        parsed_url = urlparse(full_link)
        category_id = parse_qs(parsed_url.query).get('category', [None])[0]
        # 将提取的数据存储在字典中
        data = {
            'id': category_id,
            'link': full_link,  # 完整的页面链接
            'src': treasure_link,
            'p': text_description
        }
        # 将字典添加到列表中
        treasure_data.append(data)
    return treasure_data

def main():
    my_browser = init_my_browser()  # 初始化浏览器
    treasure_data = []  # 初始化所有页面的图片数据列表
    try:
        url = 'https://zm-digicol.dpm.org.cn/'  # 构造页面URL
        my_browser.get(url)

        # 设置显式等待
        wait = WebDriverWait(my_browser, 10)  # 10秒超时
        xpath = '//div[@class="list"]//li[a/@href and a/img/@src and a/p/span/strong and a/p/span and a/p]'  # 设置XPath以匹配图片元素
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # 等待元素出现

        treasure_data = get_treasure_data(my_browser, xpath, url)  # 获取当前页面的图片数据
    except TimeoutException:
        logging.error("显式等待超时，未找到指定元素")
    except Exception as e:  # 如果发生其他异常
        logging.error(f"可惜， {e}")  # 记录错误信息
    finally:
        my_browser.quit()  # 无论是否发生异常，都关闭浏览器

    # 将所有页面的图片数据写入json文件
    output_file = '../datas/treasure.json'  # 设置输出文件路径
    set_json_data(output_file, treasure_data)

if __name__ == '__main__':
    main()
