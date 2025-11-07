import logging  # 导入logging模块，用于日志记录
import random
import time
from selenium.webdriver.common.by import By  # 导入By类，用于指定元素定位方式

from app.datas.data_writer.set_json_data import set_json_data
from app.spiders import init_my_browser


def get_image_data(my_browser, xpath):  # 定义获取图片数据的函数
    image_elements = my_browser.find_elements(By.XPATH, xpath)  # 使用XPath找到所有匹配的图片元素
    image_data = []  # 初始化图片数据列表
    for element in image_elements:  # 遍历所有图片元素
        title = element.get_attribute('alt')  # 获取元素的alt属性作为标题
        src = element.get_attribute('src')  # 获取元素的src属性作为图片链接
        image_data.append({'title': title, 'src': src})  # 将标题和链接作为字典添加到列表
    return image_data  # 返回图片数据列表

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    my_browser = init_my_browser()  # 初始化浏览器
    image_data_all_pages = []  # 初始化所有页面的图片数据列表
    try:
        for page_number in range(1, 14):  # 遍历页面编号从1到13
            url = f'https://hanfusong.com/galleryt/page/{page_number}'  # 构造页面URL
            my_browser.get(url)  # 打开页面
            xpath = '//img[@class="thumb"]'  # 设置XPath以匹配图片元素
            image_data = get_image_data(my_browser, xpath)  # 获取当前页面的图片数据
            image_data_all_pages.extend(image_data)  # 将当前页面的图片数据添加到总数据列表
            logging.info(f"从 第{page_number}页 拿到汉服摄影图信息")  # 记录日志信息
            # 添加随机间隔时间,避免爬取太快
            time.sleep(random.uniform(5, 10))
    except Exception as e:
        logging.error(f"可惜，{e}")  # 记录错误信息
    finally:
        my_browser.quit()  # 无论是否发生异常，都关闭浏览器

    # 将所有页面的图片数据写入json文件
    output_file = '../datas/cloth.json'  # 设置输出文件路径
    set_json_data(output_file,image_data_all_pages)

if __name__ == '__main__':
   main()
