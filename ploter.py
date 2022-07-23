import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from pyecharts import options as opts
from pyecharts.charts import Kline

def init_data(stockcode,startdate,enddate):
    now = datetime.datetime.now()
    if startdate == "" and enddate == "":
        enddate = str(now.date())
        startdate = str((now - relativedelta(months=2)).date())   
    data = pd.read_csv("./data/StockData/" + stockcode + ".csv")
    return data,startdate,enddate

def GetDemo(stockcode,startdate,enddate,col):
    data,startdate,enddate = init_data(stockcode,startdate,enddate)
    data["Date"]= pd.to_datetime(data["Date"])
    data = data[(data.Date <= enddate) & (data.Date >= startdate)].set_index("Date")
        
    col = col.split(" ")
    #选中用户选择的列
    data = data.filter(col)

    return data

def kline(stockcode,startdate,enddate):
    data,startdate,enddate = init_data(stockcode,startdate,enddate)
    data = data[(data.Date <= enddate) & (data.Date >= startdate)]
    dates = pd.Series.tolist(data["Date"])
    data = data.iloc[:,1:5]
    data = data[["Open","Close","Low","High"]]
    dflist = []
    for i in range(data.shape[0]):
        row = pd.Series.tolist(data.iloc[i,:])
        dflist.append(row)
    #画图
    c = (
    Kline()
    .add_xaxis(dates)
    .add_yaxis(
        "",
        dflist,
        itemstyle_opts=opts.ItemStyleOpts(
            color="#FF6666",
            color0="#99CC66"
        ),
    )
    .set_global_opts(
        xaxis_opts=opts.AxisOpts(is_scale=True,
                                name = "Date"),
        yaxis_opts=opts.AxisOpts(
            is_scale=True,
            name = "Currency in USD",
            splitarea_opts=opts.SplitAreaOpts(
                is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
            ),
        ),
        datazoom_opts=[opts.DataZoomOpts(type_="inside")],
        title_opts=opts.TitleOpts(title="Candlestick Chart of "+ stockcode+ " from " + startdate + " to " + enddate),
    ))
    c.render('./templates/echart.html')