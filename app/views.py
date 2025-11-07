from flask import Flask, render_template,jsonify,request
import plotly.express as px
from app.datas.data_reader.txt_reader import get_txt_data
from app.datas.data_reader.json_reader import get_json_data

app = Flask(__name__)

# 配置首页
@app.route('/')
@app.route('/index')
def index():
    first_8_data = get_json_data('./datas/cloth.json')[:8]
    image_links = get_txt_data('./datas/carousel.txt')
    return render_template('index.html', links=image_links,cloth=first_8_data)

# 配置汉服展示
@app.route('/cloth')
def cloth():
    all_data = get_json_data('./datas/cloth.json')
    return render_template('cloth.html', cloth = all_data)

# 配置古籍展示
@app.route('/api/books', methods=['GET'])
def get_books():
    book_data = get_json_data('./datas/book.json')
    start = int(request.args.get('start', 0))
    end = int(request.args.get('end', len(book_data)))
    return jsonify(book_data[start:end])

@app.route('/book')
def book():
    return render_template('book.html')

# 配置诗人展示
@app.route('/poet')
def poet():
    poet = get_json_data('./datas/poet.json')
    return render_template('poet.html', poet = poet)

# 配置诗人详情
@app.route('/poet_detail/<poet_name>')
def poet_detail(poet_name):
    data = get_json_data('./datas/poet_details.json')
    poet_details = [item for item in data if item.get('name') == poet_name]
    if not poet_details:
        return render_template('404.html')  # 404页面
    return render_template('poet_detail.html', poet=poet_details)

# 配置珍稀宝阁
@app.route('/treasure')
def treasure():
    treasure = get_json_data('./datas/treasure.json')
    return render_template('treasure.html', treasure=treasure)

# 配置宝物详情
@app.route('/treasure-detail/<treasure_id>')
def treasure_detail(treasure_id):
    data = get_json_data('./datas/treasure_details.json')
    # 筛选出所有id与treasure_id相同的元素
    treasure_details = [item for item in data if item.get('id') == treasure_id]
    if not treasure_details:
        return render_template('404.html')  # 404页面
    return render_template('treasure_detail.html', treasure=treasure_details)

# 非物质文化遗产
@app.route('/heritage')
def heritage():
    heritage = get_json_data('./datas/heritage.json')
    return render_template('heritage.html', heritage = heritage)

# 非物质文化遗产详情
@app.route('/heritage_detail')
def heritage_detail():
    heritage_details = get_json_data('./datas/heritage_details.json')
    if not heritage_details:
        return render_template('404.html')  # 404页面
    return render_template('heritage_detail.html', heritage=heritage_details)

# 配置敦煌展示
@app.route('/e_dunhuang')
def e_dunhuang():
    dun_huang_data = get_json_data('./datas/dun_huang.json')
    return render_template('e_dunhuang.html',books = dun_huang_data )

# 配置统计展示
@app.route('/statistic')
def statistic():
    # 宝物
    treasure_data = get_json_data('./datas/treasure.json')
    treasure_list = []
    for item in treasure_data:
        p_value = item.get('p')
        if p_value:
            num, type = p_value.split('件/套')
            treasure = {
                'num': num,
                'type': type
            }
            treasure_list.append(treasure)

    # 非物质文化遗产
    heritage_data = get_json_data('./datas/heritage_details.json')
    # 处理 heritage_data，提取 time 字段的前四个字符
    for item in heritage_data:
        if 'time' in item and len(item['time']) >= 4:
            item['time'] = item['time'][:4]

    # 假设 get_json_data 是一个已经定义好的函数，用于获取诗人数据
    poet_data = get_json_data('./datas/poet_details.json')
    poet_list = []
    total_works = sum(len(item['works']) for item in poet_data if 'works' in item and item['works'])

    for item in poet_data:
        if 'works' in item and item['works']:
            works_num = len(item['works'])
            poet = item['name']
            rate = works_num / total_works if total_works else 0
            poet_list.append({'poet': poet, 'works_num': works_num, 'rate': rate})

    # 使用Plotly创建饼图
    fig = px.pie(poet_list, values='works_num', names='poet', title='诗人作品数量分布')
    # 生成图表的HTML代码
    poet_chart_html = fig.to_html(full_html=False)

    # 敦煌莫高窟
    dun_huang_data = get_json_data('./datas/dun_huang.json')
    # 统计每个朝代的数量
    dynasty_count = {}
    for item in dun_huang_data:
        dynasty = item['dynasty'][-2:]  # 提取最后两个字符
        if dynasty in dynasty_count:
            dynasty_count[dynasty] += 1
        else:
            dynasty_count[dynasty] = 1
    return render_template('statistic.html', treasure=treasure_list, heritage=heritage_data,
                           poet_chart_html=poet_chart_html,dynasty_count = dynasty_count )


if __name__ == '__main__':
    # 改个浪漫的端口号嘻嘻
    app.run(debug=True,port=1314)



