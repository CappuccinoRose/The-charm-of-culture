from urllib.parse import urlparse, urljoin, parse_qs
from lxml import etree
import logging  # 导入logging模块，用于日志记录
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app.datas.data_writer.set_json_data import set_json_data
from app.spiders import init_my_browser

def get_heritage_data(browser, xpath, url):
    heritage_data = []
    try:
        browser.get(url)
        # 等待 JavaScript 加载完成
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        # 获取页面源代码
        html_content = browser.page_source
        # 解析 HTML
        tree = etree.HTML(html_content)
        # 使用 XPath 找到所有匹配的元素
        items = tree.xpath(xpath)
        for item in items:
            # 获取我想要的
            link = item.xpath('@href')[0]
            # 解析URL
            parsed_url = urlparse(url)
            # 重新组合scheme和netloc以获取域名
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            # 确保全路径
            full_link = urljoin(base_url, link)
            # 查找 '#' 符号并截取其之前的部分
            full_link_without_fragment = full_link.split('#')[0]
            # 解析URL
            parsed_url = urlparse(full_link_without_fragment)
            # 获取查询参数中的 'tid'
            tid = parse_qs(parsed_url.query).get('tid', [None])[0]
            # 获得相对src
            src = item.xpath('.//img/@src')[0]
            # 确保全路径
            full_src = urljoin(base_url, src)
            p = ''.join(item.xpath('.//div[@class="p"]/text()')).strip()

            data = {
                'id': tid,
                'link': full_link,
                'src': full_src,
                'p': p
            }
            heritage_data.append(data)
            logging.info(f"加入数据：tid={tid}")
    except Exception as e:
        logging.error(f"发生错误：{e}")
    return heritage_data

def main():
    my_browser = init_my_browser()
    heritage_data = []
    try:
        url = 'https://www.ihchina.cn/index.html/'
        my_browser.get(url)
        xpath = '//div[@class="book"]//a[@class="link"]'
        heritage_data = get_heritage_data(my_browser, xpath, url)
    except Exception as e:
        logging.error(f"发生错误：{e}")
    finally:
        my_browser.quit()
        # 文件写入咯
    output_file = '../datas/heritage.json'
    set_json_data(output_file, heritage_data)

if __name__ == '__main__':
    main()
