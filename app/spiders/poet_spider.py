import logging  # 导入logging模块，用于日志记录
from selenium.webdriver.common.by import By
from lxml import etree
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from app.datas.data_writer.set_json_data import set_json_data
from app.spiders import init_my_browser

def get_poet_data(browser, xpath):
    poet_data = []
    # 获取页面源代码
    html_content = browser.page_source
    # 解析HTML
    tree = etree.HTML(html_content)
    # 使用XPath找到所有匹配的<div class="author">元素
    items = tree.xpath(xpath)
    for item in items:
        # 诗人链接
        link = item.xpath('.//a/@href')[0]
        # 诗人名字
        poet = item.xpath('.//a/text()')[0]
        data = {
            'link': link,
            'poet': poet
        }
        # 将字典添加到列表中
        poet_data.append(data)
    return poet_data

def main():
    my_browser = init_my_browser()  # 初始化浏览器
    poet_data = []  # 初始化所有页面的图片数据列表
    try:
        url = 'http://www.xcz.im/library/'  # 构造页面URL
        my_browser.get(url)
        # 设置显式等待
        wait = WebDriverWait(my_browser, 10)  # 10秒超时
        # 修正XPath表达式，确保它匹配<div class="author">元素
        xpath = "//div[@data-v-6841b5a0 and @class='authors']//div[@data-v-6841b5a0 and @class='author']"
        # 设置显式等待条件
        wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # 等待元素出现

        poet_data = get_poet_data(my_browser, xpath)  # 获取当前页面的图片数据
    except TimeoutException:
        logging.error("显式等待超时，未找到指定元素")
    except Exception as e:  # 如果发生其他异常
        logging.error(f"发生错误： {e}")  # 记录错误信息
    finally:
        my_browser.quit()  # 无论是否发生异常，都关闭浏览器

    # 将所有页面的图片数据写入json文件
    output_file = '../datas/poet.json'  # 设置输出文件路径
    set_json_data(output_file, poet_data)

if __name__ == '__main__':
    main()
