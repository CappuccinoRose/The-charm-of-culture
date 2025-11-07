import logging  # 导入logging模块，用于日志记录

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# 写入txt文件
def set_txt_data(output_file,links):
    with open(output_file, 'w') as f:  # 打开文件用于写入
        for link in links:  # 遍历新链接列表
            f.write(link + '\n')  # 写入链接并换行