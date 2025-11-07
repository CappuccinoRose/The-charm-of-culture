import logging  # 导入logging模块，用于日志记录
from urllib.parse import urljoin
from selenium.webdriver.common.by import By
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from app.datas.data_writer.set_json_data import set_json_data
from app.spiders import init_my_browser

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_dun_huang_data(browser, xpath):
    dun_huang_data = []
    # 获取页面源代码
    html_content = browser.page_source
    # 解析HTML
    tree = etree.HTML(html_content)
    # 使用XPath找到所有匹配的<div>元素
    items = tree.xpath(xpath)
    for item in items:
        # 提取名称
        name = item.xpath('.//h4/text()')[0].strip() if item.xpath('.//h4/text()') else ''
        # 提取图片链接
        img_link = item.xpath('.//a/img/@src')[0].strip() if item.xpath('.//a/img/@src') else ''
        # 图片访问全路径
        full_img_link = urljoin('https://',img_link)
        # 提取年代
        dynasty = item.xpath('.//ul[@class="time"]/li[1]/span/text()')[0].strip() if item.xpath(
            './/ul[@class="time"]/li[1]/span/text()') else ''

        # 将提取的数据存储在字典中
        data = {
            'name': name,
            'dynasty': dynasty,
            'img_link': full_img_link
        }
        # 将字典添加到列表中
        dun_huang_data.append(data)
        logging.info(f'存入{name}')
    return dun_huang_data

def main():
    my_browser = init_my_browser()  # 初始化浏览器
    dun_huang_data = []  # 初始化所有页面的图片数据列表
    try:
        url = 'https://www.e-dunhuang.com/section.htm'
        my_browser.get(url)
        # 设置显式等待
        wait = WebDriverWait(my_browser, 10)  # 10秒超时
        xpath = '//div[@class="clases-section"]/div[@class="container"]/div[@id="masonry"]/div[@class="trainee-grid wow zoomInLeft animated"]'  # 设置XPath以匹配目标元素
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # 等待元素出现
        dun_huang_data = get_dun_huang_data(my_browser, xpath)  # 获取当前页面的数据
    except TimeoutException:
        logging.error("显式等待超时，未找到指定元素")
    except Exception as e:  # 如果发生其他异常
        logging.error(f"可惜，发生错误: {e}")  # 记录错误信息
    finally:
        my_browser.quit()  # 无论是否发生异常，都关闭浏览器

    # 将所有页面的数据写入json文件
    output_file = '../datas/dun_huang.json'  # 设置输出文件路径
    set_json_data(output_file, dun_huang_data)

if __name__ == '__main__':
    main()