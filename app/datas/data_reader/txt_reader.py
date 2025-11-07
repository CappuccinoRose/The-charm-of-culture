from flask import current_app

# 读取txt文件
def get_txt_data(filename):
    try:
        with open(filename, 'r') as file:
            image_links = file.readlines()  # 读取文件的所有行，并存储到列表中
        return [link.strip() for link in image_links]  # 返回一个新列表，包含去除每行首尾空格的链接
    except FileNotFoundError:  # 如果文件不存在，则捕获FileNotFoundError异常
        current_app.logger.error(f"File {filename} not found.")  # 使用Flask应用的logger记录错误信息
        return []
    except Exception as e:  # 如果发生其他类型的异常，则捕获并记录
        current_app.logger.error(f"可惜 {e}")  # 使用Flask应用的logger记录错误信息
        return []

