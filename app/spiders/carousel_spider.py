from selenium.webdriver.support.ui import WebDriverWait  # 导入WebDriverWait类，用于等待页面元素加载
from selenium.webdriver.support import expected_conditions as EC  # 导入expected_conditions，用于定义等待条件
from selenium.webdriver.common.by import By  # 导入By类，用于指定元素定位方式
import logging  # 导入logging模块，用于日志记录
import re  # 导入re模块，用于正则表达式操作

from app.datas.data_writer.set_txt_data import set_txt_data
from app.spiders import init_my_browser

def replace_links(links):  # 定义替换链接的函数
    new_links = []  # 创建新链接列表
    for link in links:  # 遍历原始链接列表
        # 在多次失败后，只有这样操作链接地址才能不出错显示
        if '.jpg' in link:  # 如果链接包含'.jpg'
            base_link = link.split('.jpg')[0]  # 去除'.jpg'后的所有内容
            modified_link = base_link.replace('vcg/nowater800/new', 'vcg/800/new')  # 替换链接中的特定字符串
            re_modified_link = re.sub(r'(vcg)\d{2}', r'\g<1>00', modified_link)  # 使用正则表达式替换链接中的特定部分
            new_link = f"{re_modified_link}.jpg"  # 重新拼接成新的jpg格式的url
            new_links.append(new_link)  # 添加新链接到列表
         # 如果不包含'.jpg'，直接下一次循环
    return new_links  # 返回新链接列表

def get_srcs(my_browser, xpath, output_file):  # 定义获取图片链接并写入文件的函数
    try:
        elements = WebDriverWait(my_browser, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))  # 等待所有指定XPATH的元素加载完成
        links = [element.get_attribute('src') for element in elements if '.jpg' in element.get_attribute('src')]  # 获取所有包含'.jpg'的src属性值
        new_links = replace_links(links)  # 调用replace_links函数处理链接
        set_txt_data(output_file,new_links)
        logging.info('已存储')
    except Exception as e:
        logging.error(f"可惜， {e}")  # 记录错误日志
    finally:
        my_browser.quit()  # 关闭浏览器

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    url = 'https://www.vcg.com/creative-image/zhonghuachuantongwenhua/'  # 设置目标网页URL
    my_browser = init_my_browser()  # 初始化浏览器
    try:
        my_browser.get(url)  # 打开目标网页
        xpath = "//figure[@class='galleryItem']/a/img"  # 设置图片元素的XPATH
        output_file = '../datas/carousel.txt'  # 设置输出文件路径
        get_srcs(my_browser, xpath, output_file)  # 调用函数获取图片链接并写入文件
    except Exception as e:  # 捕获异常
        logging.error(f"可惜: {e}")  # 记录错误日志
    finally:
        # 确保浏览器在异常情况下也能关闭
        if my_browser:  # 如果浏览器实例存在
            my_browser.quit()  # 关闭浏览器

if __name__ == '__main__':
    main()
