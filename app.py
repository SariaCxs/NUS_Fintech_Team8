import tushare as ts
from filter import Filter
from sorter import Sorter

from flask import Flask
import base64
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib as mpl

import ploter
from flask import (
    redirect, render_template, request, url_for
)
import pandas as pd
from pandas_datareader import data
import json
from util.getInvestType import InvestSurvey
app = Flask(__name__)
#更新静态文件，否则echart无法加载
app.config['TEMPLATES_AUTO_RELOAD'] = True

CODE_LIST = pd.read_csv("./data/Runes_clean.csv")['Rune']
with open('./data/classification.json','r',encoding='utf8')as fp:
    CLASSIFICATION = json.load(fp)


filter = Filter()
sorter = Sorter()
filter = Filter()
survey_helper = InvestSurvey()
CODE_SIFT = []



data = {}
daily_data = []
survey_args = ['goal','loss','hold']
is_fetch = 0

@app.route('/',methods=['GET'])
def main():
    return render_template('main.html')

@app.route("/survey",methods=['GET','POST'])
def survey():
    global survey_helper
    if request.method == 'POST':
        answers = []
        for arg in survey_args:
            answers.append(int(request.form.get(arg)))
        type, score = survey_helper.getType(answers)
        return redirect(url_for('recommend', type=type,score=score))

    return render_template('survey.html')


@app.route('/recommend',methods=['GET','POST'])
def recommend():
    global data
    type = request.args.get('type')
    score = request.args.get('score')
    #fetch data according to type
    result = []
    for code in CLASSIFICATION[int(score)][str(score)]:
        result.append(df2dic(code,data[code]))
    cols = [key for key in result[0].keys()]
    return render_template('recommend.html', type=type, stocks=result, cols=cols)


@app.route('/select',methods=['GET','POST'])
def select_stock():
    #get 显示当日数据 列表存储
    result = daily_data
    global data
    if request.method == 'POST':
        #根据args进行判断
        global filter
        filter_indicators = {}
        for ind in filter.indicator_pool.keys():
            if request.form.get(ind.upper()) == '1':
                filter_indicators[ind] = request.form.get(ind.lower())
        code = filter.filt(filter_indicators)
        result = toFormat(code,data)
        #result = sorter.sort(data,'Close')
    if len(result)>0:
        cols = [key for key in result[0].keys()]
    else:
        cols = []

    return render_template('select.html',stocks=result,cols=cols)


@app.route('/search', methods=('GET', 'POST'))
def search():
    if request.method == 'POST':
        stockcode = request.form['stockcode']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        col = request.form['col']
        # 接受用户参数传入
        if startdate > enddate or stockcode =="":
            return render_template('404.html')
        return redirect(url_for('search_result', stockcode=stockcode, startdate=startdate, enddate=enddate, col=col))
    return render_template('search.html')


# 可视化结果
@app.route('/search_result', methods=('GET', 'POST'))
def search_result():
    stockcode = request.args.get('stockcode')
    startdate = request.args.get('startdate')
    enddate = request.args.get('enddate')
    col = request.args.get('col')
    #动态可视化
    if col == "":
        ploter.kline(stockcode,startdate,enddate)
        return render_template('echart_result.html')
    jsfig = ploter.ochl(stockcode,startdate,enddate,col)
    return render_template('plotly_result.html',jsfig = jsfig)
    # data = ploter.GetDemo(stockcode, startdate, enddate, col)
    # col = col.split(" ")
    # # 静态可视化
    # plt.switch_backend('agg') 
    # plt.clf() # 关掉上一次请求时的图片
    # style.use('ggplot')
    # mpl.rc('figure', dpi=120)
    # for each_col in col:
    #     plt.plot(data[each_col], label=each_col)
    # plt.legend()
    # plt.title("The Search Result of " + stockcode)
    # plt.xlabel("Date")
    # plt.ylabel("Currency in USD")

    # # 将画出的图推给前端
    # buffer = BytesIO()
    # plt.savefig(buffer)
    # plot_data = buffer.getvalue()
    # imb = base64.b64encode(plot_data)  # 对plot_data进行编码
    # ims = imb.decode()
    # imd = "data:image/png;base64," + ims
    # return render_template('get_result.html', img=imd)

#echart获取
@app.route('/echart', methods=('GET', 'POST'))
def echart():
    return render_template('echart.html')

#联系我们
@app.route('/contact', methods=('GET', 'POST'))
def contact():
    return render_template('contact.html')

@app.before_request
def if_fetch():
    global is_fetch
    if is_fetch == 0:
        fetch_data()
        is_fetch = 1

def parse_user_type(answers):
    type = ['Cautious', 'steady', 'active','aggressive']
    return type[0]




def df2dic(code,df):
    dic = {}
    dic['code'] = code
    for col in df:
        dic[col] = df.iloc[-1,:][col]
    return dic


def fetch_data():
    global data
    global daily_data
    data = {}
    daily_data = []
    for stock in CODE_LIST[:]:
        try:
            STOCK_DATA = pd.read_csv("./data/StockData/" + stock + ".csv")
            STOCK_DATA = STOCK_DATA.iloc[-60:].round(2)
            data[stock] = STOCK_DATA
            daily_data.append(df2dic(stock,STOCK_DATA))

        except:
            pass
    daily_data = toFormat(data.keys(),data)

#取code中每支股票的第一行，转换成前端的输出格式
def toFormat(code,df):
    result = []
    for stock in code:
        dic = {}
        dic['code'] = stock
        data = df[stock]
        for col in data:
            dic[col] = data.iloc[-1, :][col]
        result.append(dic)
    return result



if __name__ == "__main__":
    app.run(port=5000)
    

