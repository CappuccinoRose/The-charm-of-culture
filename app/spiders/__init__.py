from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


def init_my_browser():
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument(f"user-agent={UserAgent().random}")

        my_browser = webdriver.Chrome(options=chrome_options)
        return my_browser
    except WebDriverException as e:
        print(f"浏览器初始化失败: {e}")
        return None



